import sql_module
import pandas as pd
import quant_infos.wics_code
db = sql_module.Mysql('quantdb')

df = pd.concat([pd.DataFrame(quant_infos.wics_code.wics_lc.items()), pd.DataFrame(quant_infos.wics_code.wics_mc.items())])
df = df.astype('str')
df = "'" + df + "'"

db.insert_sql(df, 'ktbl', 'replace', foreign_key_checks=False)