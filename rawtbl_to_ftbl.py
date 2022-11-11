import sql_module
import pandas as pd

db = sql_module.MYSQL('quantdb')
df = pd.read_sql('select * from ftbl where c_code = 005930', db)

# ftbl - rawtbl
# c_code c_code
# f_date data_year + 1 - 5월 첫날
# sales sales
# gm gross_profit
# ni net_income
# asset assets
# ca current_assets 
# cl current_liabilities
# issued_shares x
# bps bps
# EPS eps

print(df)