import numpy as np
import sql_module.mysql_control
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime as dt
from dateutil.relativedelta import relativedelta
import Keesung_logging
from tqdm import tqdm

db = sql_module.mysql_control.Mysql('quantdb')

code_list = pd.read_sql('SELECT c_code FROM comtbl',db)['c_code'].tolist()
logger = Keesung_logging.my_logger()

for code in tqdm(code_list, desc='ftbl update'):
    try:
        invest_url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701'
        invest_page = requests.get(invest_url)
        fs_url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
        fs_page = requests.get(fs_url)
        soup = BeautifulSoup(invest_page.text, "html.parser")
        # 수정평균주식수
        stock = soup.find_all('tr', class_= 'c_grid1_1 rwf acd_dep2_sub')
        issued_shares = [x.text for x in stock if '주식수' in x.text] # 크롤링 데이터
        index = str(issued_shares).find('수정')
        issued_shares = str(issued_shares)[index:]
        issued_shares = issued_shares.replace('\\n', ' ')
        issued_shares = issued_shares.replace('\\xa0', '0')
        issued_shares = issued_shares.replace(',', '')
        issued_shares = issued_shares.split(' ')[:6]
        # 날짜, EPS, BPS
        invest_df = pd.read_html(invest_page.text, index_col = 0)[1]
        fs_df = pd.read_html(fs_page.text, index_col = 0)
        acc_month = invest_df.columns.tolist()[-2].split('/')[1] # account month 결산월
        df = []
        for year in range(2019,2022):
            column = [x for x in invest_df.columns.tolist() if f'{year}/{acc_month}' in x]
            if len(column) > 0:
                # 회사코드 append
                text_list = []
                text_list.append("'" + code + "'") 
                # column 설정
                column = column[0]
                # f_date append
                f_date = dt.datetime(year,int(acc_month),1) + relativedelta(months=5)
                f_date = f"'{str(f_date)[:10]}'"
                text_list.append(f_date) 
                # sales append (매출액)
                sales = str(fs_df[0][column]['매출액']).split('.')[0]
                text_list.append(sales)
                # gm append (매출총이익)
                gm = str(fs_df[0][column]['매출총이익']).split('.')[0]
                text_list.append(gm)
                # ni append (당기순이익)
                ni = str(fs_df[0][column]['당기순이익']).split('.')[0]
                text_list.append(ni)
                # asset append (자산)
                asset = str(fs_df[2][column]['자산']).split('.')[0]
                text_list.append(asset)
                # ca append (유동자산)
                index = [x for x in fs_df[2].index.tolist() if '유동자산' in x][0]
                ca = str(fs_df[2][column][index]).split('.')[0]
                text_list.append(ca)
                # cl append (유동부채)
                index = [x for x in fs_df[2].index.tolist() if '유동부채' in x][0]
                cl = str(fs_df[2][column][index]).split('.')[0]
                text_list.append(cl)
                # issued_shares append
                index = invest_df.columns.tolist().index(column)
                text_list.append(str(issued_shares[index+1]))
                # bps append
                index = [x for x in invest_df.index.tolist() if 'BPS계산' in x][0]
                bps = invest_df[column][index] 
                text_list.append(str(bps)) 
                # eps append
                index = [x for x in invest_df.index.tolist() if 'EPS계산' in x][0]
                eps = invest_df[column][index]
                text_list.append(str(eps))
                if np.nan not in text_list:
                    df.append(text_list)
                else:
                    logger.error(f'Error Code : You have Null Data in {code}')
        df = pd.DataFrame(df)
        db.insert_sql(df, 'ftbl', 'replace', foreign_key_checks = True)
    except Exception as e:
        logger.error(f'{code} - {e}')
logger.error_check()