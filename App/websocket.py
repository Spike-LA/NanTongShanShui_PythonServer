import pymysql

from json import loads
from bottle import get, run
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
import uuid

usersList = []


@get('/websocket/', apply=[websocket])
def chat(ws):
    # 连接数据库
    db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    uid = uuid.uuid4().hex
    usersList.append({"uuid": uid, "ws": ws})  # 如果该用户/设备处于未登录状态，则建立登录状态
    ws.send(uid)
    database_save = True

    while True:
        msg = ws.receive()
        if msg:
            msg = loads(msg)  # 将发送的信息转化为json格式
            if database_save:  # 确保新增新的ws对象的操作只执行一次
                websocket_id = uid
                object_id = msg['send_id']
                distinguish_code = msg['distinguish_code']

            if msg["distinguish_code"] == '0':  # 发送方为设备端
                whetherUserLogin = False
                sql_3 = 'INSERT websocket_relation(websocket_id,object_id,distinguish_code,equipment_id)' \
                        "VALUES ('%s', '%s', '%s',null)" % (websocket_id, object_id, distinguish_code)
                cursor.execute(sql_3)
                database_save = False
                for i in usersList:
                    if i['uuid'] == msg['aim_id']:  # 找到设备端要发送消息的用户端对象
                        i['ws'].send(str(msg['action']))
                        whetherUserLogin = True
                        break
                if not whetherUserLogin:
                    ws.send("该用户未登录")
            elif msg["distinguish_code"] == '1':  # 发送方为客户端
                whetherEquipmentLogin = False
                equipment_id = msg['equipment_id']
                sql_5 = 'SELECT * from websocket_relation where equipment_id=%s'
                cursor.execute(sql_5,equipment_id)
                results_1 = cursor.fetchall()
                if results_1:
                    break
                else:
                    sql_4 = 'INSERT websocket_relation(websocket_id,object_id,distinguish_code,equipment_id)' \
                            "VALUES ('%s', '%s', '%s','%s')" % (websocket_id, object_id, distinguish_code,equipment_id)
                    cursor.execute(sql_4)
                    database_save = False
                    for i in usersList:
                        if i['uuid'] == msg['aim_id']:  # 找到用户端要发送消息的设备端对象
                            i['ws'].send(str(msg['action']))
                            whetherEquipmentLogin = True
                            break
                    if not whetherEquipmentLogin:
                        ws.send("该设备未登录")
            else:  # 对象识别码错误
                ws.send("对象识别码错误")
        else:
            break
    # 如果断开连接，则踢出users集合
    for i in usersList:
        if i['ws'] == ws:
            usersList.remove(i)
    sql_6 ='SELECT * from websocket_relation where object_id=%s'
    cursor.execute(sql_6,msg['send_id'])
    results_2=cursor.fetchall()
    if results_2:
        sql_2 = 'DELETE from websocket_relation where object_id=%s'
        cursor.execute(sql_2, msg['send_id'])
    db.commit()
    # 关闭数据库连接
    db.close()

run(host='0.0.0.0', port=9000, server=GeventWebSocketServer)
