import streamlit as st
import argparse
import os
import sys
import logging
import json
import pandas as pd
import threading
import shutil
from glob import glob
from modules.quantylab.rltrader import settings
from modules.quantylab.rltrader import data_manager


# selectbox에 사용될 옵션 리스트
mode_list = ['train', 'test', 'update', 'predict']
rl_method_list = ['dqn', 'pg', 'ac', 'a2c', 'a3c', 'monkey']
net_list = ['dnn', 'lstm', 'cnn', 'monkey']
backend_list = ['pytorch', 'tensorflow', 'plaidml']
v3_data = os.listdir('/app/Data/v3')
v3_data = [i.replace(".csv", "") for i in v3_data ]
v3_data = sorted(v3_data)


# selectbox를 이용하여 파라미터 입력 받기
mode = "test"
col1, col2 = st.columns(2)
data_upload = col1.file_uploader('테스트 데이터 업로드', type='csv')
data_v3 = col2.selectbox('또는 기본 제공 데이터 사용.', v3_data)
name = st.text_input('이름 설정', value='')
stock_code = name
model = st.selectbox('저장된 모델 선택', glob("/app/models/*.mdl"))
backend = "pytorch"

df = pd.read_csv(f"/app/Data/v3/{data_v3}.csv")
if data_upload is not None:
    df = pd.read_csv(data_upload)
df = df.sort_values(by='Date').reset_index(drop=True) 
try:
    df['Date'] = df['Date'].str.replace('-', '')
except:
    pass
start_date = df['Date'].iloc[0]
end_date = df['Date'].iloc[-1]
start_date = st.text_input('테스트 시작일', value=start_date)
end_date = st.text_input('테스트 종료일', value=end_date)
balance = st.number_input('시작 자금', value=100000000)

# argparse를 사용하여 파라미터 저장
args = argparse.Namespace(mode=mode, name=name, stock_code=stock_code, backend=backend, start_date=start_date,
                          end_date=end_date, 
                          balance=balance)

init_button = st.button('모델 테스트 시작')

if init_button:
    # 학습기 파라미터 설정
    st.success('테스트 시작. 좌측의 log page에서 테스트 진행 상황을 확인하세요.')
    shutil.rmtree("/app/output")
    os.makedirs("/app/output")
    output_name = f'{args.mode}_{args.name}_{args.rl_method}_{args.net}'
    learning = args.mode in ['train', 'update']
    reuse_models = args.mode in ['test', 'update', 'predict']
    value_network_name = f'{args.name}_{args.rl_method}_{args.net}_value.mdl'
    policy_network_name = f'{args.name}_{args.rl_method}_{args.net}_policy.mdl'
    start_epsilon = 1 if args.mode in ['train', 'update'] else 0
    num_epoches = 1000 if args.mode in ['train', 'update'] else 1
    num_steps = 5 if args.net in ['lstm', 'cnn'] else 1
    risk = args.risk

    # Backend 설정
    os.environ['RLTRADER_BACKEND'] = args.backend
    if args.backend == 'tensorflow':
        os.environ['KERAS_BACKEND'] = 'tensorflow'
    elif args.backend == 'plaidml':
        os.environ['KERAS_BACKEND'] = 'plaidml.keras.backend'
        
    # 출력 경로 생성
    output_path = os.path.join(settings.BASE_DIR, 'output', output_name)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
        
    # 파라미터 기록
    params = json.dumps(vars(args))
    with open(os.path.join(output_path, 'params.json'), 'w') as f:
        f.write(params)
        
    # 모델 경로 준비
    # 모델 포멧은 TensorFlow는 h5, PyTorch는 pickle
    value_network_path = os.path.join(settings.BASE_DIR, 'models', value_network_name)
    policy_network_path = os.path.join(settings.BASE_DIR, 'models', policy_network_name)
    
    # 로그 기록 설정
    log_path = os.path.join(output_path, f'{output_name}.log')
    if os.path.exists(log_path):
        os.remove(log_path)
    logging.basicConfig(format='%(message)s')
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename=log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.info(params)
    
    # Backend 설정, 로그 설정을 먼저하고 RLTrader 모듈들을 이후에 임포트해야 함
    from modules.quantylab.rltrader.learners import ReinforcementLearner, DQNLearner, PolicyGradientLearner, ActorCriticLearner, A2CLearner, A3CLearner
    
    common_params = {}
    list_stock_code = []
    list_chart_data = []
    list_training_data = []
    list_min_trading_price = []
    list_max_trading_price = []


    # 차트 데이터, 학습 데이터 준비
    chart_data, training_data = data_manager.load_data(
        df, args.start_date, args.end_date)
    
    print('chart_data length : ', len(chart_data))
    print('training_data length : ', len(training_data))
    

    assert len(chart_data) >= num_steps
    
    # 최소/최대 단일 매매 금액 설정
    min_trading_price = int(100000*(1+risk))
    max_trading_price = int(10000000*(1+risk))
    
    # 공통 파라미터 설정
    common_params = {'rl_method': args.rl_method, 
        'net': args.net, 'num_steps': num_steps, 'lr': args.lr,
        'balance': args.balance, 'num_epoches': num_epoches, 
        'discount_factor': args.discount_factor, 'start_epsilon': start_epsilon,
        'output_path': output_path, 'reuse_models': reuse_models}

    # 강화학습 시작
    learner = None
    if args.rl_method != 'a3c':
        common_params.update({'stock_code': stock_code,
            'chart_data': chart_data, 
            'training_data': training_data,
            'min_trading_price': min_trading_price, 
            'max_trading_price': max_trading_price})
        if args.rl_method == 'dqn':
            learner = DQNLearner(**{**common_params, 
                'value_network_path': value_network_path})
        elif args.rl_method == 'pg':
            learner = PolicyGradientLearner(**{**common_params, 
                'policy_network_path': policy_network_path})
        elif args.rl_method == 'ac':
            learner = ActorCriticLearner(**{**common_params, 
                'value_network_path': value_network_path, 
                'policy_network_path': policy_network_path})
        elif args.rl_method == 'a2c':
            learner = A2CLearner(**{**common_params, 
                'value_network_path': value_network_path, 
                'policy_network_path': policy_network_path})
        elif args.rl_method == 'monkey':
            common_params['net'] = args.rl_method
            common_params['num_epoches'] = 10
            common_params['start_epsilon'] = 1
            learning = False
            learner = ReinforcementLearner(**common_params)
        
    else:
        list_stock_code.append(stock_code)
        list_chart_data.append(chart_data)
        list_training_data.append(training_data)
        list_min_trading_price.append(min_trading_price)
        list_max_trading_price.append(max_trading_price)

    if args.rl_method == 'a3c':
        learner = A3CLearner(**{
            **common_params, 
            'list_stock_code': list_stock_code, 
            'list_chart_data': list_chart_data, 
            'list_training_data': list_training_data,
            'list_min_trading_price': list_min_trading_price, 
            'list_max_trading_price': list_max_trading_price,
            'value_network_path': value_network_path, 
            'policy_network_path': policy_network_path})
        
    assert learner is not None

    if args.mode in ['train', 'test', 'update']:
        thread = threading.Thread(target=learner.run(learning=learning))
        thread.start()
        thread.join()
        if args.mode in ['train', 'update']:
            thread = threading.Thread(target=learner.save_models())
            thread.start()
            thread.join()
    elif args.mode == 'predict':
        thread = threading.Thread(target=learner.predict())
        thread.start()
        thread.join()
        
    