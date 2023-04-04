import datetime
import os 
import urllib.request
import ssl
import zipfile
import os
import pandas as pd
from glob import glob
def update_kospi_stock_code():
    if os.path.exists(f"/app/Data/KRX/kospi_stock_info.csv"):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"/app/Data/KRX/kospi_stock_info.csv"))
        if file_time.date() == datetime.datetime.today().date():
            return file_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip",
                                "/app/Data/KRX/kospi_code.zip")
        
        os.chdir("/app/Data/KRX")
        kospi_zip = zipfile.ZipFile('kospi_code.zip')
        kospi_zip.extractall()
        kospi_zip.close()
        if os.path.exists("/app/Data/KRX/kospi_code.zip"):
            os.remove("/app/Data/KRX/kospi_code.zip")
            
        file_name = "/app/Data/KRX/kospi_code.mst"
        tmp_fil1 = "/app/Data/KRX/kospi_code_part1.tmp"
        tmp_fil2 = "/app/Data/KRX/kospi_code_part2.tmp"
        wf1 = open(tmp_fil1, mode="w")
        wf2 = open(tmp_fil2, mode="w")

        with open(file_name, mode="r", encoding="cp949") as f:
            for row in f:
                rf1 = row[0:len(row) - 228]
                rf1_1 = rf1[0:9].rstrip()
                rf1_2 = rf1[9:21].rstrip()
                rf1_3 = rf1[21:].strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                rf2 = row[-228:]
                wf2.write(rf2)

        wf1.close()
        wf2.close()

        part1_columns = ['단축코드', '표준코드', '한글명']
        df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='utf-8')

        field_specs = [2, 1, 4, 4, 4,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 9, 5, 5, 1,
                    1, 1, 2, 1, 1,
                    1, 2, 2, 2, 3,
                    1, 3, 12, 12, 8,
                    15, 21, 2, 7, 1,
                    1, 1, 1, 1, 9,
                    9, 9, 5, 9, 8,
                    9, 3, 1, 1, 1
                    ]

        part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
                        '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
                        'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
                        'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
                        'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
                        'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
                        'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
                        '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
                        '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
                        '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
                        '상장주수', '자본금', '결산월', '공모가', '우선주',
                        '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
                        '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
                        '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
                        ]

        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        # clean temporary file and dataframe
        del (df1)
        del (df2)
        os.remove(tmp_fil1)
        os.remove(tmp_fil2)
        os.remove(file_name)
        df.to_csv(f"/app/Data/KRX/kospi_stock_info.csv", index=False, encoding='utf-8')
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"/app/Data/KRX/kospi_stock_info.csv")).strftime('%Y-%m-%d %H:%M:%S')
        return file_time
    
    
def update_kosdaq_stock_code(verbose=False):
    if os.path.exists(f"/app/Data/KRX/kosdaq_stock_info.csv"):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"/app/Data/KRX/kospi_stock_info.csv"))
        if file_time.date() == datetime.datetime.today().date():
            return file_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip",
                                "/app/Data/KRX/kosdaq_code.zip")
        
        os.chdir("/app/Data/KRX")
        kosdaq_zip = zipfile.ZipFile('kosdaq_code.zip')
        kosdaq_zip.extractall()
        kosdaq_zip.close()
        if os.path.exists("/app/Data/KRX/kosdaq_code.zip"):
            os.remove("/app/Data/KRX/kosdaq_code.zip")
            
        file_name = "/app/Data/KRX/kosdaq_code.mst"
        tmp_fil1 = "/app/Data/KRX/kosdaq_code_part1.tmp"
        tmp_fil2 = "/app/Data/KRX/kosdaq_code_part2.tmp"
        wf1 = open(tmp_fil1, mode="w")
        wf2 = open(tmp_fil2, mode="w")

        with open(file_name, mode="r", encoding="cp949") as f:
            for row in f:
                rf1 = row[0:len(row) - 222]
                rf1_1 = rf1[0:9].rstrip()
                rf1_2 = rf1[9:21].rstrip()
                rf1_3 = rf1[21:].strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                rf2 = row[-222:]
                wf2.write(rf2)

        wf1.close()
        wf2.close()

        part1_columns = ['단축코드','표준코드','한글종목명']
        df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='utf-8')

        field_specs = [2, 1,
                    4, 4, 4, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 9,
                    5, 5, 1, 1, 1,
                    2, 1, 1, 1, 2,
                    2, 2, 3, 1, 3,
                    12, 12, 8, 15, 21,
                    2, 7, 1, 1, 1,
                    1, 9, 9, 9, 5,
                    9, 8, 9, 3, 1,
                    1, 1
                    ]

        part2_columns = ['증권그룹구분코드','시가총액 규모 구분 코드 유가',
                        '지수업종 대분류 코드','지수 업종 중분류 코드','지수업종 소분류 코드','벤처기업 여부 (Y/N)',
                        '저유동성종목 여부','KRX 종목 여부','ETP 상품구분코드','KRX100 종목 여부 (Y/N)',
                        'KRX 자동차 여부','KRX 반도체 여부','KRX 바이오 여부','KRX 은행 여부','기업인수목적회사여부',
                        'KRX 에너지 화학 여부','KRX 철강 여부','단기과열종목구분코드','KRX 미디어 통신 여부',
                        'KRX 건설 여부','(코스닥)투자주의환기종목여부','KRX 증권 구분','KRX 선박 구분',
                        'KRX섹터지수 보험여부','KRX섹터지수 운송여부','KOSDAQ150지수여부 (Y,N)','주식 기준가',
                        '정규 시장 매매 수량 단위','시간외 시장 매매 수량 단위','거래정지 여부','정리매매 여부',
                        '관리 종목 여부','시장 경고 구분 코드','시장 경고위험 예고 여부','불성실 공시 여부',
                        '우회 상장 여부','락구분 코드','액면가 변경 구분 코드','증자 구분 코드','증거금 비율',
                        '신용주문 가능 여부','신용기간','전일 거래량','주식 액면가','주식 상장 일자','상장 주수(천)',
                        '자본금','결산 월','공모 가격','우선주 구분 코드','공매도과열종목여부','이상급등종목여부',
                        'KRX300 종목 여부 (Y/N)','매출액','영업이익','경상이익','단기순이익','ROE(자기자본이익률)',
                        '기준년월','전일기준 시가총액 (억)','그룹사 코드','회사신용한도초과여부','담보대출가능여부','대주가능여부'
                        ]

        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        # clean temporary file and dataframe
        del(df1)
        del(df2)
        os.remove(tmp_fil1)
        os.remove(tmp_fil2)
        os.remove(file_name)
        df.to_csv(f"/app/Data/KRX/kosdaq_stock_info.csv", index=False, encoding='utf-8')
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"/app/Data/KRX/kosdaq_stock_info.csv")).strftime('%Y-%m-%d %H:%M:%S')
        #수정된 시간을 기록한다.
        return file_time
    
def return_only_stock_df():
    # 증권그룹구분코드가 DR, EW, SW, SR, BC, FE를 제외한 것들만 가져온다. 
    # ST:주권 MF:증권투자회사 RT:부동산투자회사    
    # SC:선박투자회사 IF:사회간접자본투융자회사    
    # DR:주식예탁증서 EW:ELW EF:ETF                
    # SW:신주인수권증권 SR:신주인수권증서          
    # BC:수익증권 FE:해외ETF FS:외국주권
    # 우선주 코드가 0인 것만 가져온다.
    kosdaq_stock_info_file = "/app/Data/KRX/kosdaq_stock_info.csv"
    kosdaq_stock_info_df = pd.read_csv(kosdaq_stock_info_file, encoding="utf-8")
    kosdaq_stock_info_df = kosdaq_stock_info_df[kosdaq_stock_info_df["증권그룹구분코드"].isin(["DR", "EW", "EF", "SW", "SR", "BC", "FE", "EN", "IF", "MF"]) == False]
    kosdaq_stock_info_df = kosdaq_stock_info_df[kosdaq_stock_info_df["우선주 구분 코드"] == 0]
    kosdaq_stock_info_df = kosdaq_stock_info_df[kosdaq_stock_info_df["기업인수목적회사여부"] == "N"]
    
    kospi_stock_info_file = "/app/Data/KRX/kospi_stock_info.csv"
    kospi_stock_info_df = pd.read_csv(kospi_stock_info_file, encoding="utf-8")
    kospi_stock_info_df = kospi_stock_info_df[kospi_stock_info_df["그룹코드"].isin(["DR", "EW", "EF", "SW", "SR", "BC", "FE", "EN", "IF", "MF"]) == False]
    kospi_stock_info_df = kospi_stock_info_df[kospi_stock_info_df["우선주"] == 0]
    return kosdaq_stock_info_df, kospi_stock_info_df
    
def get_stock_list(market = "ALL"):
    kosdaq_stock_info_df, kospi_stock_info_df = return_only_stock_df()
    if market == "KOSPI":
        code_list = list(kospi_stock_info_df["단축코드"])
    elif market == "KOSDAQ":
        code_list = list(kosdaq_stock_info_df["단축코드"])
    else:
        code_list = list(kosdaq_stock_info_df["단축코드"]) + list(kospi_stock_info_df["단축코드"])
    return code_list



def get_listing_date(stock_code=None):
    kosdaq_data, kospi_data = return_only_stock_df()
    kosdaq_data = kosdaq_data[["단축코드", "주식 상장 일자"]]
    kosdaq_data = kosdaq_data.rename(columns={"주식 상장 일자": "상장일자"})
    kospi_data = kospi_data[["단축코드", "상장일자"]]
    listing_date = pd.concat([kosdaq_data, kospi_data])
    if stock_code is None:
        return listing_date
    else:
        listing_date = listing_date[listing_date["단축코드"] == stock_code]
        listing_date = listing_date["상장일자"].values[0]
        return listing_date

def get_stock_name(stock_code=None):
    kosdaq_data, kospi_data = return_only_stock_df()
    kosdaq_data = kosdaq_data[["단축코드", "한글종목명"]]
    kosdaq_data = kosdaq_data.rename(columns={"한글종목명": "종목명"})
    kospi_data = kospi_data[["단축코드", "한글명"]]
    kospi_data = kospi_data.rename(columns={"한글명": "종목명"})
    stock_name = pd.concat([kosdaq_data, kospi_data])
    if stock_code is None:
        return stock_name
    else:
        stock_name = stock_name[stock_name["단축코드"] == stock_code]
        stock_name = stock_name["종목명"].values[0]
        return stock_name

def get_stock_market_cap(stock_code=None):
    
    kosdaq_data, kospi_data = return_only_stock_df()
    kosdaq_data = kosdaq_data[["단축코드", "전일기준 시가총액 (억)"]]
    kosdaq_data = kosdaq_data.rename(columns={"전일기준 시가총액 (억)": "시가총액"})
    kospi_data = kospi_data[["단축코드", "시가총액"]]
    market_cap = pd.concat([kosdaq_data, kospi_data])
    if stock_code is None:
        return market_cap
    else:
        market_cap = market_cap[market_cap["단축코드"] == stock_code]
        market_cap = market_cap["시가총액"].values[0]
        return market_cap
    
    
    
    