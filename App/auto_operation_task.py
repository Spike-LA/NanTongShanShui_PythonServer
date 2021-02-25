import asyncio
import json
import datetime

import pymysql
from django.db import connection
import websockets


# 数据库连表无条件搜索
def maintenance(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = dict_fetchall(cursor)
    cursor.close()
    return results

# 自定义原生sql的fetchall方法（将获取的数据形式改为列表套字典）
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]  # 拿到对应的字段列表
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()]

# 建立websocket请求和发送命令
async def hello(url,data):
    async with websockets.connect(url) as websocket:
        data_json = json.dumps(data)
        await websocket.send(data_json)


def auto_operation():
    db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT auto_operation_info.uuid,auto_operation_info.pump_code,pump.equipment_code,websocket_id,operation_time,operation_type,auto_operation_info.`status`,begin_time,end_time,period,next_run_time FROM auto_operation_info " \
          "INNER JOIN pump ON auto_operation_info.pump_code=pump.pump_code " \
          "INNER JOIN equipment ON pump.equipment_code=equipment.equipment_code " \
          "INNER JOIN websocket_relation ON equipment.equipment_code=object_id"
    results = maintenance(sql)
    for data in results:
        command = {"send_id": "自动",
                "equipment_code": "",
                "aim_id": "",
                "action": {"pump_code": "", "open_time": "", "dosage":""},
                "distinguish_code": "2"}
        time_now = datetime.datetime.now() # 获取当前时间
        if data['status'] == '0':  # 该自动任务状态为未完成
            if data['opration_type'] == '0': # 该任务类型为定时任务
                time_distance = time_now-data['begin_time']
                if datetime.timedelta(days=0,seconds=-60)<=time_distance<=datetime.timedelta(days=0,seconds=60): # 如果定时任务的时间与当前时间差在一分钟以内
                    command['equipment_code'] = data['equipment_code']
                    command['aim_id'] = data['websocket_id']
                    command['action']['pump_code'] = data['pump_code']
                    command['action']['open_time'] = data['operation_time']
                    command['action']['dosage'] = data['dosage']
                    asyncio.get_event_loop().run_until_complete(hello('ws://122.51.80.50:90',command)) # 发送websocket请求至服务器
                    sql_1 = 'UPDATE auto_operation_info SET status=%s WHERE uuid=%s'
                    table_1 = ['1',data['uuid']]
                    cursor.execute(sql_1,table_1)
                    db.commit()
            else: # 该任务类型为周期性任务
                time_distance = time_now-data['next_run_time']
                if datetime.timedelta(days=0, seconds=-60) <= time_distance <= datetime.timedelta(days=0,seconds=60):  # 如果周期任务的下次执行时间与当前时间差在一分钟以内
                    command['equipment_code'] = data['equipment_code']
                    command['aim_id'] = data['websocket_id']
                    command['action']['pump_code'] = data['pump_code']
                    command['action']['open_time'] = data['operation_time']
                    command['action']['dosage'] = data['dosage']
                    days = int(data['period'])
                    asyncio.get_event_loop().run_until_complete(
                        hello('ws://122.51.80.50:90', command))  # 发送websocket请求至服务器
                    if data['end_time']-time_now < datetime.timedelta(days=days): # 已经达不到下次周期性任务的时间，任务就已经要结束了
                        sql_2 = 'UPDATE auto_operation_info SET status=%s WHERE uuid=%s'
                        table_2 = ['1', data['uuid']]
                        cursor.execute(sql_2, table_2)
                        db.commit()
                    else:
                        next_run_time = time_now+datetime.timedelta(days=days)
                        sql_3 = 'UPDATE auto_operation_info SET next_run_time=%s WHERE uuid=%s' # 更新下次操作时间
                        table_3 = [next_run_time,data['uuid']]
                        cursor.execute(sql_3, table_3)
                        db.commit()