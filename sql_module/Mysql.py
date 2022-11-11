"""
Mysql

insert_sql : 5000개씩 bulk insert 수행 (입력값 pd.Dataframe) 
"""
import pymysql
import os
import pandas as pd
class Mysql(pymysql.connections.Connection):
    
    def __init__(self, db_name: str):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_info.txt')
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
        
    def insert_sql(self, df: pd.DataFrame, tbl: str, mode: str, foreign_key_checks: bool=True):
        """
        replace into를 이용하여 데이터를 업데이트 한다.

        Args:
            df (pd.DataFrame): input 데이터 프레임
            tbl (str): 테이블 이름
            mode (str): 입력 모드 replace, ignore
            foreign_key_checks (bool, optional): 외래키 체크 옵션 (True면 체크 한다). Defaults to True.
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