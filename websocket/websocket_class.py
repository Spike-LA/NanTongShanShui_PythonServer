from datetime import datetime
import uuid
from json import loads
import time

import pymysql


class Websocket:

    def __init__(self):
        self.usersList = []
        self.db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')
        self.cursor = self.db.cursor()
        self.user_code = '1' # 用户代号
        self.equipment_code = '0' # 设备代号

    def connect(self, ws):
        database_save = True
        is_judged = True
        whetherEquipmentLogin = False
        websocket_id = ''
        object_id = ''
        distinguish_code = ''
        uid = uuid.uuid4().hex
        self.usersList.append({"uuid": uid, "websocket": ws})  # 如果该用户/设备处于未登录状态，则建立登录状态
        ws.send(uid)
        # 获取当前时间
        now = datetime.now()
        update_time = now.strftime('%Y-%m-%d %H:%M:%S')
        # 连接时进行登录状态存储（只有websocket_id)
        sql_1 = 'INSERT websocket_relation(websocket_id,update_time) VALUES(%s,%s)'
        table = [uid, update_time]
        self.cursor.execute(sql_1, table)
        self.db.commit()
        while True:
            msg = ws.receive()
            if msg:
                msg = loads(msg)  # 将发送的信息转化为json格式

                if msg['action'] == '666':  # 设备端实时数据的记录
                    now_data = msg['data']
                    data_time = datetime.now()
                    now_data_update_time = data_time.strftime('%Y-%m-%d %H:%M:%S')
                    self.heartbeat_task(msg['send_id'], now_data, now_data_update_time)
                else:
                    if database_save:  # 确保新增新的ws对象的操作只执行一次
                        websocket_id = uid
                        object_id = msg['send_id']  # 设备是code，用户是id
                        distinguish_code = msg['distinguish_code']
                    if msg["distinguish_code"] == self.user_code:  # 发送方为用户端
                        sql_16 = 'SELECT * from user where aid=%s'
                        # 判断是否是已登录用户在操作设备，如果是恶意操作则断开ws连接
                        self.cursor.execute(sql_16, object_id)
                        results_3 = self.cursor.fetchall()
                        try:
                            if results_3[0][12] == '-1':
                                break
                        except Exception as e:
                            if results_3[12] == '-1':
                                break
                        equipment_code = msg['equipment_code']
                        command_id = uuid.uuid4().hex
                        self.log_insert(command_id, object_id, equipment_code, msg['action'])
                        if is_judged:
                            result = self.first_operation_judge(ws, equipment_code, command_id, object_id, distinguish_code, websocket_id, msg['aim_id'])
                            if result:
                                break
                            database_save = False
                            is_judged = False
                        for i in self.usersList:
                            if i['uuid'] == msg['aim_id']:  # 找到用户端要发送消息的设备端对象
                                i['websocket'].send(str(msg['action']))
                                whetherEquipmentLogin = True
                                self.log_update(1, command_id)
                                break
                        if not whetherEquipmentLogin:
                            self.log_update(0, command_id)
                            ws.send("该设备未登录")
                    elif msg["aim_id"] == '0' and msg["distinguish_code"] == '0':  # 设备的第一条消息用来识别该设备  "aim_id":"0"
                        # 判断是否有设备残留信息，如果有的话就删除它
                        self.whether_left_log_info(object_id)
                        # 将设备端的设备id（object_id)和对象识别码与该设备端的websocket_id配对并存入数据库
                        sql_15 = 'UPDATE websocket_relation SET object_id=%s,distinguish_code=%s WHERE websocket_id=%s'
                        table = [object_id, distinguish_code, websocket_id]
                        self.cursor.execute(sql_15, table)
                        self.db.commit()
                        database_save = False
                    elif msg["aim_id"] != '0' and msg["distinguish_code"] == '0':  # 发送方为设备端
                        whetherUserLogin = False
                        database_save = False
                        for i in self.usersList:
                            if i['uuid'] == msg['aim_id']:  # 找到设备端要发送消息的用户端对象
                                i['websocket'].send(str(msg['action']))
                                sql_12 = 'UPDATE equipment_operation_log SET operate_status=%s WHERE command_id=%s'
                                table = [1, command_id]
                                if msg['action'] == '1':
                                    pass
                                else:
                                    table[0] = 0
                                self.cursor.execute(sql_12, table)
                                self.db.commit()
                                whetherUserLogin = True
                                break
                        if not whetherUserLogin:
                            ws.send("该用户未登录")
                    else:  # 对象识别码错误
                        ws.send("对象识别码错误")
            else:
                break
        # 如果断开连接，则踢出users集合
        for i in self.usersList:
            if i['websocket'] == ws:
                self.usersList.remove(i)
        sql_5 = 'SELECT * from websocket_relation where websocket_id=%s'
        self.cursor.execute(sql_5, uid)
        results_2 = self.cursor.fetchall()
        if results_2:
            sql_6 = 'DELETE from websocket_relation where websocket_id=%s'
            self.cursor.execute(sql_6, uid)
        self.db.commit()
        # 关闭数据库连接
        self.db.close()

    def heartbeat_task(self, equipment_code, now_data, now_data_update_time):
        """
        当接收到心跳包时执行
        equipment_code:实时数据的设备编号
        now_data:设备端传来的实时数据（是一个对象），格式为{“酸碱度”:6.06pH,”浊度”:1NTU,”ORP”:”1mv”,”电导率”:”1uS/cm”,”腐蚀率:1mm/a,”水温”:1℃”}
        :return:
        """
        # 删除历史实时数据
        sql_19 = 'DELETE from real_time_data where equipment_code=%s'
        self.cursor.execute(sql_19, equipment_code)
        # 更新设备的登录时间（用于定时任务搜索设备是否出故障）
        sql_20 = 'UPDATE websocket_relation SET update_time=%s WHERE object_id=%s'
        table = [now_data_update_time, equipment_code]
        self.cursor.execute(sql_20, table)
        self.db.commit()
        key_list = now_data.keys() # 获取所有键
        print(key_list)
        for key in key_list:
            now_data_id = uuid.uuid4().hex
            table = [now_data_id, equipment_code, key, now_data[key], now_data_update_time]
            sql_21 ="INSERT real_time_data (uuid, equipment_code, mearsure_type, mearsurement, update_time) VALUES (%s,%s,%s,%s,%s)"
            self.cursor.execute(sql_21, table)
            self.db.commit()

    def log_insert(self, cid, object_id, equipment_code, action):
        """
        用于操作日志的插入
        :param object_id: 操作者uuid
        :param equipment_code: 操作设备编号
        :param action: 操作命令
        :return:
        """
        time_now = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间，并改成对应格式
        sql_7 = "INSERT  equipment_operation_log (command_id, operation_time, operation_person_id, " \
                "operation_equipment_code, operation_id) VALUES ('%s', '%s','%s', '%s', '%s')"
        table = [cid, time_now, object_id, equipment_code, action]
        self.cursor.execute(sql_7,table)
        self.db.commit()

    def log_update(self, send_status, cid):
        """
        :param send_status: 日志中所写的操作执行结果code
        :param cid: 日志的uuid
        :return:
        """
        sql_9 = 'UPDATE equipment_operation_log SET send_status=%s WHERE command_id=%s'
        table = [send_status, cid]
        self.cursor.execute(sql_9, table)
        self.db.commit()

    def first_operation_judge(self, ws, equ_code, cid, obj_id, dis_code, ws_id, aim_id):
        """
        用于用户初次发送操作指令时判断设备是否正在被使用
        :param ws: ws对象
        :param equ_code: 设备编号
        :param cid: 日志的uuid
        :return:
        """
        whether_break = True
        sql_3 = 'SELECT * from websocket_relation where equipment_code=%s'
        self.cursor.execute(sql_3, equ_code)
        results_1 = self.cursor.fetchall()
        if results_1:
            ws.send("该设备正在被操作")
            self.log_update(0, cid)
        else:
            # 将用户端的用户id（object_id)和对象识别码与该用户端的websocket_id配对并存入数据库
            sql_4 = 'UPDATE websocket_relation SET object_id=%s,distinguish_code=%s,equipment_code=%s WHERE websocket_id=%s'
            table = [obj_id, dis_code, equ_code, ws_id]
            self.cursor.execute(sql_4, table)
            self.db.commit()
            for i in self.usersList:
                if i['uuid'] == aim_id:  # 找到用户端要发送消息的设备端对象
                    i['websocket'].send(ws_id)
            whether_break = False
        return whether_break

    def whether_left_log_info(self,obj_id):
        sql_17 = 'SELECT * from websocket_relation where object_id=%s'
        self.cursor.execute(sql_17, obj_id)
        result_17 = self.cursor.fetchall()
        if result_17:
            sql_18 = 'DELETE from websocket_relation where object_id=%s'
            self.cursor.execute(sql_18,obj_id)
            self.db.commit()



