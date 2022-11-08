import pymysql

def connecting(db_name):
    path = 'db_info.txt'
    f = open(path)
    id, pw, host = f.read().split()
    db = pymysql.connect(
        user = id,
        port = 3306,
        passwd = pw,
        host = host,
        db = db_name,
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
    )
    return db

#데이터 넣기, 입력값 // db = 데이터베이스, df = 데이터프레임
def insert_replace(db,df,tbl,foreign_key_checks = False):
    """_summary_

    Args:
        db (pymysql.connect): 연결된 db
        df (pd.DataFrame): input 데이터 프레임
        tbl (_type_): _description_
        foreign_key_checks (bool, optional): _description_. Defaults to False.
    """    
    if foreign_key_checks:
        with db.cursor() as cursor:
            cursor.execute('SET foreign_key_checks=0')
    df_list = df.values.tolist()
    slicing = 5000
    rep = int(len(df_list)/slicing) + 1 #반복횟수
    for num in range(rep):
        if num != (rep-1):
            df_sql = df_list[num*slicing:(num+1)*slicing]
        else:
            df_sql = df_list[num*slicing:]
        sql_list = []
        for value in df_sql:
            tmp = '(' + ', '.join(value) + ')'
            sql_list.append(tmp)
    
        sql = f'replace into {tbl} values ' + ', '.join(sql_list)
        with db.cursor() as cursor:
            cursor.execute(sql)
    if foreign_key_checks:
        with db.cursor() as cursor:
            cursor.execute('SET foreign_key_checks=1')
    db.commit()