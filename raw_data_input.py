import pandas as pd
import sql_module.mysql_control

db = sql_module.mysql_control.Mysql('quantdb')
df = pd.read_excel(r'C:\Users\user\Desktop\All_git\Quant_project\데이터.xlsx')

# 데이터 정리
df.columns = list(df.loc[9][df.columns[:5]]) + list(df.loc[8][df.columns[5:]])
df = df.loc[10:]
df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x[1:])

# 주기 (1Q, 2Q, 3Q, 4Q, Annual) 인데, 1~4Q는 nan값 있으면 버리고, 4Q에 매출0 있으면 버리기
# 카카오, sk텔레콤 처럼 매출원가가 0인 기업들도 있음
df = df.dropna('index')
df = df.drop('Name', axis=1)

# foreign key check 설정을 true로 해두었으므로, 먼저 comtbl 업데이트 필요
# rawtbl 업데이트 해준다.
db.insert_sql(df, 'rawtbl', 'replace')