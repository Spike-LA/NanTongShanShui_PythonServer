import time

import pymysql

from json import loads
from bottle import get, run
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
import uuid

from App.views_constant import fail, success, do_success, do_fail

usersList = []


@get('/', apply=[websocket])
def chat(ws):
    # 连接数据库
    global action, command_id, object_id
    db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    uid = uuid.uuid4().hex
    usersList.append({"uuid": uid, "ws": ws})  # 如果该用户/设备处于未登录状态，则建立登录状态
    ws.send(uid)
    # 连接时进行登录状态存储（只有websocket_id)
    sql_1 = 'INSERT websocket_relation(websocket_id) VALUES(%s)'
    cursor.execute(sql_1, uid)
    db.commit()
    database_save = True
    is_judged = True
    while True:
        msg = ws.receive()
        if msg:
            msg = loads(msg)  # 将发送的信息转化为json格式
            if database_save:  # 确保新增新的ws对象的操作只执行一次
                websocket_id = uid
                object_id = msg['send_id']
                distinguish_code = msg['distinguish_code']
                action = msg['action']

            # if msg["aim_id"] == '1' and msg["distinguish_code"] == '1':  # 用户的第一条消息用来识别该用户  "aim_id":"1"
            #     equipment_id = msg['equipment_id']
            #     # 将用户的user_id（object_id)和对象识别码与该用户的websocket_id配对并存入数据库
            #     sql_2 = 'UPDATE websocket_relation SET object_id=%s,distinguish_code=%s, equipment_id=%s WHERE websocket_id=%s'
            #     table = [object_id, distinguish_code, equipment_id, websocket_id]
            #     cursor.execute(sql_2, table)
            #     db.commit()
            #     for i in usersList:
            #         if i['uuid'] == msg['aim_id']:  # 找到用户端要发送消息的设备端对象
            #             i['ws'].send(str(msg['action']))
            if msg["distinguish_code"] == '1':  # 发送方为用户端
                whetherEquipmentLogin = False
                command_id = uuid.uuid4().hex
                equipment_id = msg['equipment_id']
                time_now = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间，并改成对应格式
                sql_3 = 'SELECT * from websocket_relation where equipment_id=%s'
                cursor.execute(sql_3, equipment_id)
                results_1 = cursor.fetchall()
                sql_7 = "INSERT  equipment_operation_log (command_id, operation_time, operation_person_id, " \
                        "operation_equipment_id, operation_id) VALUES ('%s', '%s','%s', '%s', '%s')" % (command_id, time_now, object_id, equipment_id, action,)
                cursor.execute(sql_7)
                db.commit()
                if is_judged:
                    if results_1:
                        ws.send("该设备正在被操作")
                        sql_8 = 'UPDATE equipment_operation_log SET send_status=%s WHERE command_id=%s'  # 有人正在操作该设备，记录发送失败日志
                        table = [fail, command_id]
                        cursor.execute(sql_8, table)
                        db.commit()
                        break
                    else:
                        # 将用户端的用户id（object_id)和对象识别码与该用户端的websocket_id配对并存入数据库
                        sql_4 = 'UPDATE websocket_relation SET object_id=%s,distinguish_code=%s,equipment_id=%s WHERE websocket_id=%s'
                        table = [object_id, distinguish_code, equipment_id, websocket_id]
                        cursor.execute(sql_4, table)
                        db.commit()
                        for i in usersList:
                            if i['uuid'] == msg['aim_id']:  # 找到用户端要发送消息的设备端对象
                                i['ws'].send(websocket_id)
                        database_save = False
                is_judged = False

                for i in usersList:
                    if i['uuid'] == msg['aim_id']:  # 找到用户端要发送消息的设备端对象
                        i['ws'].send(str(msg['action']))
                        whetherEquipmentLogin = True
                        sql_9 = 'UPDATE equipment_operation_log SET send_status=%s WHERE command_id=%s'  # 记录发送成功日志
                        table = [success, command_id]
                        cursor.execute(sql_9, table)
                        db.commit()
                        break
                if not whetherEquipmentLogin:
                    sql_10 = 'UPDATE equipment_operation_log SET send_status=%s WHERE command_id=%s'  # 该设备未登录，记录发送失败日志
                    table = [fail, command_id]
                    cursor.execute(sql_10, table)
                    db.commit()
                    ws.send("该设备未登录")
            elif msg["aim_id"] == '0' and msg["distinguish_code"] == '0':  # 设备的第一条消息用来识别该设备  "aim_id":"0"
                # 将设备端的设备id（object_id)和对象识别码与该设备端的websocket_id配对并存入数据库
                sql_15 = 'UPDATE websocket_relation SET object_id=%s,distinguish_code=%s WHERE websocket_id=%s'
                table = [object_id, distinguish_code, websocket_id]
                cursor.execute(sql_15, table)
                db.commit()
                database_save = False
            elif msg["aim_id"] != '0' and msg["distinguish_code"] == '0':  # 发送方为设备端
                whetherUserLogin = False
                database_save = False
                for i in usersList:
                    if i['uuid'] == msg['aim_id']:  # 找到设备端要发送消息的用户端对象
                        i['ws'].send(str(msg['action']))
                        if msg['action'] == '1':
                            sql_12 = 'UPDATE equipment_operation_log SET operate_status=%s WHERE command_id=%s'  # 记录执行成功日志
                            table = [do_success, command_id]
                        else:
                            sql_12 = 'UPDATE equipment_operation_log SET operate_status=%s WHERE command_id=%s'  # 记录执行失败日志
                            table = [do_fail, command_id]
                        cursor.execute(sql_12, table)
                        db.commit()
                        whetherUserLogin = True
                        break
                if not whetherUserLogin:
                    ws.send("该用户未登录")
            else:  # 对象识别码错误
                ws.send("对象识别码错误")
        else:
            break
    # 如果断开连接，则踢出users集合
    for i in usersList:
        if i['ws'] == ws:
            usersList.remove(i)
    sql_5 = 'SELECT * from websocket_relation where websocket_id=%s'  #########
    cursor.execute(sql_5, uid)
    results_2 = cursor.fetchall()
    if results_2:
        sql_6 = 'DELETE from websocket_relation where websocket_id=%s'
        cursor.execute(sql_6, uid)
    db.commit()
    # 关闭数据库连接
    db.close()


run(host='0.0.0.0', port=90, server=GeventWebSocketServer)