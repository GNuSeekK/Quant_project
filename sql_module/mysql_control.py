import pymysql
import os
class Mysql(pymysql.connections.Connection):
    
    def __init__(self, db_name):
        path = 'db_info.txt'
        f = open(path)
        id, pw, host = f.read().split()
        super().__init__(
            user = id,
            port = 3306,
            passwd = pw,
            host = host,
            db = db_name,
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
        )
        
    def insert_sql(self, df, tbl, mode, foreign_key_checks = True):
        """
        replace into를 이용하여 데이터를 업데이트 한다.

        Args:
            df (pd.DataFrame): input 데이터 프레임
            tbl (str): 테이블 이름
            mode (str): 입력 모드 replace, ignore
            foreign_key_checks (bool, optional): _description_. Defaults to False.
        """    
        if mode == 'replace':
            sql = f'replace into {tbl} values '
        elif mode == 'ignore':
            sql = f'insert ignore into {tbl} values '
        if foreign_key_checks == False:
            with self.cursor() as cursor:
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
        
            sql +=  ', '.join(sql_list)
            with self.cursor() as cursor:
                cursor.execute(sql)
        if foreign_key_checks == False:
            with self.cursor() as cursor:
                cursor.execute('SET foreign_key_checks=1')
        self.commit()
# def connecting(db_name):
#     path = 'db_info.txt'
#     f = open(path)
#     id, pw, host = f.read().split()
#     db = pymysql.connect(
#         user = id,
#         port = 3306,
#         passwd = pw,
#         host = host,
#         db = db_name,
#         charset = 'utf8',
#         cursorclass = pymysql.cursors.DictCursor
#     )
#     return db

#데이터 넣기, 입력값 // db = 데이터베이스, df = 데이터프레임

# def insert_sql(db, df, tbl, mode, foreign_key_checks = True):
#     """
#     replace into를 이용하여 데이터를 업데이트 한다.

#     Args:
#         db (pymysql.connect): 연결된 db
#         df (pd.DataFrame): input 데이터 프레임
#         tbl (str): 테이블 이름
#         mode (str): 입력 모드 replace, ignore
#         foreign_key_checks (bool, optional): _description_. Defaults to False.
#     """    
#     if mode == 'replace':
#         sql = f'replace into {tbl} values '
#     elif mode == 'ignore':
#         sql = f'insert ignore into {tbl} values '
#     if foreign_key_checks == False:
#         with db.cursor() as cursor:
#             cursor.execute('SET foreign_key_checks=0')
#     df_list = df.values.tolist()
#     slicing = 5000
#     rep = int(len(df_list)/slicing) + 1 #반복횟수
#     for num in range(rep):
#         if num != (rep-1):
#             df_sql = df_list[num*slicing:(num+1)*slicing]
#         else:
#             df_sql = df_list[num*slicing:]
#         sql_list = []
#         for value in df_sql:
#             tmp = '(' + ', '.join(value) + ')'
#             sql_list.append(tmp)
    
#         sql +=  ', '.join(sql_list)
#         with db.cursor() as cursor:
#             cursor.execute(sql)
#     if foreign_key_checks == False:
#         with db.cursor() as cursor:
#             cursor.execute('SET foreign_key_checks=1')
#     db.commit()
    