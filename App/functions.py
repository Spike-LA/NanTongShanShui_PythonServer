import pymysql

from App.views_constant import b


# 数据库连表操作
def maintenance(sql):
    conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    data_list_json = []

    for result in results:
        d = zip(b, result)
        data = dict(d)
        data_list_json.append(data)

    data = {
            "data": data_list_json
                        }
    return data
