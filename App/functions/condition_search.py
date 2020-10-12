from django.db import connection
from App.functions.dict_fetchall import dict_fetchall


# 数据库连表多条件搜索
def maintenances(sql, table):
    cursor = connection.cursor()
    cursor.execute(sql, table)
    results = dict_fetchall(cursor)
    cursor.close()
    return results


# 数据库连表无条件搜索
def maintenance(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dict_fetchall(cursor)
    cursor.close()
    return results
