import pandas as pd
import os
from tqdm import tqdm
from modules import public_stock
from natsort import natsorted
from glob import glob
import ray
ray.init(num_cpus=10)


#별도 = [매출액,영업이익,영업이익(발표기준),당기순이익,자산총계,부채총계,자본총계,자본금,부채비율,유보율,영업이익률,순이익률,ROA,ROE,EPS(원),BPS(원),DPS(원),PER,PBR,발행주식수,배당수익률]
재무_별도 = ['매출액','영업이익','영업이익(발표기준)','당기순이익','자산총계','부채총계','자본총계','자본금','부채비율','유보율','영업이익률','순이익률','ROA','ROE','EPS(원)','BPS(원)','DPS(원)','PER','PBR','발행주식수','배당수익률']
#연결 = [매출액,영업이익,영업이익(발표기준),당기순이익,지배주주순이익,비지배주주순이익,자산총계,부채총계,자본총계,지배주주지분,비지배주주지분,자본금,부채비율,유보율,영업이익률,지배주주순이익률,ROA,ROE,EPS(원),BPS(원),DPS(원),PER,PBR,발행주식수,배당수익률]
재무_연결 = ['매출액','영업이익','영업이익(발표기준)','당기순이익','지배주주순이익','비지배주주순이익','자산총계','부채총계','자본총계','지배주주지분','비지배주주지분','자본금','부채비율','유보율','영업이익률','지배주주순이익률','ROA','ROE','EPS(원)','BPS(원)','DPS(원)','PER','PBR','발행주식수','배당수익률']
#포괄_별도 = [매출액,매출원가,매출총이익,판매비와관리비,영업이익,영업이익(발표기준),금융수익,금융원가,기타수익,기타비용,"종속기업,공동지배기업및관계기업관련손익",세전계속사업이익,법인세비용,계속영업이익,중단영업이익,당기순이익]
포괄_별도 = ['매출액','매출원가','매출총이익','판매비와관리비','영업이익','영업이익(발표기준)','금융수익','금융원가','기타수익','기타비용','종속기업,공동지배기업및관계기업관련손익','세전계속사업이익','법인세비용','계속영업이익','중단영업이익','당기순이익']
#포괄_연결 = 매출액,매출원가,매출총이익,판매비와관리비,영업이익,영업이익(발표기준),금융수익,금융원가,기타수익,기타비용,"종속기업,공동지배기업및관계기업관련손익",세전계속사업이익,법인세비용,계속영업이익,중단영업이익,당기순이익,지배주주순이익,비지배주주순이익
포괄_연결 = ['매출액','매출원가','매출총이익','판매비와관리비','영업이익','영업이익(발표기준)','금융수익','금융원가','기타수익','기타비용','종속기업,공동지배기업및관계기업관련손익','세전계속사업이익','법인세비용','계속영업이익','중단영업이익','당기순이익','지배주주순이익','비지배주주순이익']


def preprocess_financial_statement_1(df_path):
    df = pd.read_csv(df_path, skiprows=1)
    df = df.T
    df.columns = df.iloc[1]
    df = df[2:]
    return df

def preprocess_financial_statement_2(df):
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:-2]
    df.columns = df.columns.str.replace('계산에 참여한 계정 펼치기', '')
    return df

def save_df_by_year(path, report_type):
    csv_cache = {}
    for i in tqdm(range(len(path))):
        stock_code = path[i].split("/")[-2]
        csv_cache[stock_code] = pd.read_csv(path[i], index_col=0)
        
    year = csv_cache["005930"].index.tolist()

    df_list = {}
    for i in year:
        df_list[i] = pd.DataFrame(columns=report_type)

    for i in tqdm(csv_cache.keys()):
        for j in year:
            try:
                df_list[j].loc[i] = csv_cache[i].loc[j]
            except:
                pass
    return df_list, year
@ray.remote
def crawling_report(stock_code):
    try:
        os.makedirs(f"/app/Data/Info/Sort By Stock Code/{stock_code}", exist_ok=True)
        tables = pd.read_html(f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{stock_code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=", displayed_only=False)
        tables[11].to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-연간.csv")
        preprocess_financial_statement_1(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-연간.csv").to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-연간.csv")
        tables[12].to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-분기.csv")
        preprocess_financial_statement_1(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-분기.csv").to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-연결-분기.csv")
        tables[14].to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-연간.csv")
        preprocess_financial_statement_1(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-연간.csv").to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-연간.csv")
        tables[15].to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-분기.csv")
        preprocess_financial_statement_1(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-분기.csv").to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무제표-별도-분기.csv")
        tables = pd.read_html(f"https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{stock_code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701", displayed_only=False)
        preprocess_financial_statement_2(tables[0]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/포괄손익계산서-연결-연간.csv")
        preprocess_financial_statement_2(tables[1]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/포괄손익계산서-연결-분기.csv")
        preprocess_financial_statement_2(tables[2]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무상태표-연결-연간.csv")
        preprocess_financial_statement_2(tables[3]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무상태표-연결-분기.csv")
        tables = pd.read_html(f"https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{stock_code}&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701", displayed_only=False)
        preprocess_financial_statement_2(tables[0]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/포괄손익계산서-별도-연간.csv")
        preprocess_financial_statement_2(tables[1]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/포괄손익계산서-별도-분기.csv")
        preprocess_financial_statement_2(tables[2]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무상태표-별도-연간.csv")
        preprocess_financial_statement_2(tables[3]).to_csv(f"/app/Data/Info/Sort By Stock Code/{stock_code}/재무상태표-별도-분기.csv")
            
    except Exception as e:
        print(e)


def main():
    _ = public_stock.update_kosdaq_stock_code()
    _ = public_stock.update_kospi_stock_code()
    error_list = []
    stock_code_list = natsorted(public_stock.get_stock_list("ALL"))
    print("재무제표 크롤링 시작. 전체 종목 수: ", len(stock_code_list))
    ray.get([crawling_report.remote(stock_code) for stock_code in stock_code_list])
    print("재무제표 크롤링 종료. 오류 발생 종목 수: ", len(error_list))
    print("재무제표 가공 시작.")
            
    #error_list를 txt파일로 저장
    with open("/app/Data/log/재무제표 로드 오류.txt", "w") as f:
        for error in error_list:
            f.write(error + "\n")
            
    #재무제표_별도_분기
    path = glob("/app/Data/Info/Sort By Stock Code/**/재무제표-별도-분기.csv")
    df_list, year = save_df_by_year(path, 재무_별도)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/분기/별도/{}-재무제표-별도-분기.csv".format(i.replace("/","-")))
        
    #재무제표_연결_분기
    path = glob("/app/Data/Info/Sort By Stock Code/**/재무제표-연결-분기.csv")
    df_list, year = save_df_by_year(path, 재무_연결)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/분기/연결/{}-재무제표-연결-분기.csv".format(i.replace("/","-")))
        
    #재무제표_별도_연간
    path = glob("/app/Data/Info/Sort By Stock Code/**/재무제표-별도-연간.csv")
    df_list, year = save_df_by_year(path, 재무_별도)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/연간/별도/{}-재무제표-별도-연간.csv".format(i.replace("/","-")))
        
    #재무제표_연결_연간
    path = glob("/app/Data/Info/Sort By Stock Code/**/재무제표-연결-연간.csv")
    df_list, year = save_df_by_year(path, 재무_연결)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/연간/연결/{}-재무제표-연결-연간.csv".format(i.replace("/","-")))
        
    #포괄손익계산서_별도_분기
    path = glob("/app/Data/Info/Sort By Stock Code/**/포괄손익계산서-별도-분기.csv")
    df_list, year = save_df_by_year(path, 포괄_별도)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/분기/별도/{}-포괄손익계산서-별도-분기.csv".format(i.replace("/","-")))
        
    #포괄손익계산서_연결_분기
    path = glob("/app/Data/Info/Sort By Stock Code/**/포괄손익계산서-연결-분기.csv")
    df_list, year = save_df_by_year(path, 포괄_연결)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/분기/연결/{}-포괄손익계산서-연결-분기.csv".format(i.replace("/","-")))
        
    #포괄손익계산서_별도_연간
    path = glob("/app/Data/Info/Sort By Stock Code/**/포괄손익계산서-별도-연간.csv")
    df_list, year = save_df_by_year(path, 포괄_별도)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/연간/별도/{}-포괄손익계산서-별도-연간.csv".format(i.replace("/","-")))
        
    #포괄손익계산서_연결_연간
    path = glob("/app/Data/Info/Sort By Stock Code/**/포괄손익계산서-연결-연간.csv")
    df_list, year = save_df_by_year(path, 포괄_연결)
    for i in year:
        df_list[i].to_csv("/app/Data/Info/Sort By Time/연간/연결/{}-포괄손익계산서-연결-연간.csv".format(i.replace("/","-")))
        
    print("재무제표 가공 완료.")
        
if __name__ == "__main__":
    os.makedirs("/app/Data/Info/Sort By Time/분기/별도", exist_ok=True)
    os.makedirs("/app/Data/Info/Sort By Time/분기/연결", exist_ok=True)
    os.makedirs("/app/Data/Info/Sort By Time/연간/별도", exist_ok=True)
    os.makedirs("/app/Data/Info/Sort By Time/연간/연결", exist_ok=True)
    os.makedirs("/app/Data/log", exist_ok=True)
    os.makedirs("/app/Data/KRX", exist_ok=True)
    os.makedirs("/app/Data/Info/Sort By Stock Code", exist_ok=True)
    os.makedirs("/app/Data/마법공식", exist_ok=True)
    main()