import sql_module.mysql_control
import pandas as pd
import datetime as dt
import requests
import quant_infos.wics_code
db = sql_module.mysql_control.connecting('quantdb')

wics_mc = quant_infos.wics_code.wics_mc
wics_lc = quant_infos.wics_code.wics_lc

df = pd.DataFrame(columns=['code', 'name', 'ls', 'ms'])
# there is no data in the stock market closed day and before market open. 
# weekends, Jan 1, Dec 31 etc

day_cnt = 1
for wics_code in wics_mc.keys():
    while True:
        date = str(dt.date.today() - dt.timedelta(days = day_cnt)).replace('-','')
        response = requests.get(quant_infos.wics_code.wics_url(date, wics_code))
    
        if response.status_code == 200: # request success
            json_list = response.json() # dictionary
            if len(json_list['list']) == 0:
                day_cnt += 1
                continue
            # response.text -> return str type
            for json in json_list['list']:
                ls = json['SEC_CD'][-2:] # Large sector
                ms = json['IDX_CD'][-4:] # Medium sector
                code = json['CMP_CD'] # Company code
                name = json['CMP_KOR'] # Company korean name
                df = df.append({'code':code, 'name':name, 'ls':ls, 'ms':ms}, 
                        ignore_index=True)
        else:
            print('Error:' + response.status_code)
            print('WICS code:' + str(wics_code))

df = "'" + df + "'"

sql_module.mysql_control.insert_sql(db, df, 'comtbl', 'replace', foreign_key_checks = False)