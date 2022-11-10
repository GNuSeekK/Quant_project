import sql_module.mysql_control
import pandas as pd
db = sql_module.mysql_control.connecting('quantdb')

df = pd.concat([pd.DataFrame(wics_lc.items()), pd.DataFrame(wics_mc.items())])
df = df.astype('str')
df = "'" + df + "'"

sql_module.mysql_control.insert_sql(db, df, 'ktbl', 'replace', foreign_key_checks=False)