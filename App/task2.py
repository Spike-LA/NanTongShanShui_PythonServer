import pymysql

from datetime import datetime

# 自定义原生sql的fetchall方法（将获取的数据形式改为列表套字典）
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]  # 拿到对应的字段列表
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()]

#  定时检测websocket数据库是否存在因为异常操作残留的垃圾数据
def task():
    # 连接数据库
    db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')
    # 获取当前时间
    time_now = datetime.now()
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 遍历设备对象
    sql_1 = 'SELECT * FROM websocket_relation WHERE distinguish_code=0'
    cursor.execute(sql_1)
    results_1 = dict_fetchall(cursor)
    db.commit()
    if results_1:
        for obj in results_1:
            if obj['update_time']:
                update_time = obj['update_time']
                time_distance = time_now-update_time
                if time_distance.seconds > 420:  # 设备7分钟内没发送表示正常运行的消息给服务器
                    equipment_websocket_id = obj['websocket_id']
                    sql_2 = 'DELETE from websocket_relation where websocket_id=%s'
                    cursor.execute(sql_2, equipment_websocket_id)
                    db.commit()

    # 遍历用户对象
    sql_3 = 'SELECT * FROM websocket_relation WHERE distinguish_code is NULL or distinguish_code=1 '
    cursor.execute(sql_3)
    results_3 = dict_fetchall(cursor)
    db.commit()
    if results_3:
        for obj in results_3:
            if obj['update_time']:
                update_time = obj['update_time']
                time_distance = time_now - update_time
                if time_distance.seconds > 350:  # 用户连接时间已经超过5分钟了
                    user_websocket_id = obj['websocket_id']
                    sql_4 = 'DELETE from websocket_relation where websocket_id=%s'
                    cursor.execute(sql_4, user_websocket_id)
                    db.commit()

