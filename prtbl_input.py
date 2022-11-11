import sql_module
import pandas as pd
import requests
from bs4 import BeautifulSoup
import Keesung_logging
from tqdm import tqdm

db = sql_module.Mysql('quantdb')

code_list = pd.read_sql('SELECT c_code FROM comtbl', db)['c_code'].tolist()
logger = Keesung_logging.my_logger()
timeframe = 'day'
count = '5000'

for code in tqdm(code_list, desc='ftbl update'):
    try:
        url = 'https://fchart.stock.naver.com/sise.nhn?requestType=0'
        # price_url = url + '&symbol=' + code + '&timeframe=' + timeframe + '&count=' + count
        price_url = f'{url}&symbol={code}&timeframe={timeframe}&count={count}'
        price_data = requests.get(price_url)
        price_data_bs = BeautifulSoup(price_data.text, 'lxml')
        item_list = price_data_bs.find_all('item')

        date_list = []
        price_list = []

        for item in item_list:
            temp_data = item['data']
            datas = temp_data.split('|') # 날짜, 시가, 고가, 저가, 종가, 거래량
            date_list.append("'" + datas[0][:4] + "-" + datas[0][4:6] + "-" + datas[0][6:] + "'")
            price_list.append(datas[4])

        code_list = [f"'{code}'"] * len(date_list)
        price_df = pd.DataFrame(
                    {
                    'code' : code_list,
                    'date' : date_list,
                    'price' : price_list
                    }
                )
        db.insert_sql(price_df, 'prtbl', 'replace')
    except Exception as e:
        logger.error(f'{code} - {e}')
logger.error_check()