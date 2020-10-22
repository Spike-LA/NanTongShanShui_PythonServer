# 定时任务的任务函数
import uuid
import pymysql
import time
from influxdb import InfluxDBClient
import datetime

from App.functions.dict_fetchall import dict_fetchall

conn_db = InfluxDBClient('122.51.173.123', '8086', 'root', 'root', 'testDB')


def task():
    # 连接数据库
    db = pymysql.connect("10.21.1.58", "root", "root", "ntss", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = 'SELECT * FROM (SELECT equipment_and_sensor.equipment_id,equipment_and_sensor.sensor_id,equipment.`status`,equipment.equipment_code,sensor.sensor_threshold,sensor_type.type_name FROM equipment ' \
          'INNER JOIN equipment_and_sensor ON equipment.aid=equipment_and_sensor.equipment_id ' \
          'INNER JOIN sensor ON equipment_and_sensor.sensor_id=sensor.aid ' \
          'INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid ' \
          'INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid) ' \
          'as a where status=1'

    # 执行sql语句
    cursor.execute(sql)

    # 获取数据（形式为列表套字典）
    result_1 = dict_fetchall(cursor)

    for obj in result_1:
        sensor_id = obj['sensor_id']
        equipment_code = obj['equipment_code']
        type_name = obj['type_name']
        sensor_threshold = float(obj['sensor_threshold'])
        # influxdb 数据库查询语言
        sql_1 = "SELECT * FROM b where deviceNum='%s' order by time desc limit 1" % equipment_code

        result_of_influxdb = conn_db.query(sql_1)
        points = result_of_influxdb.get_points()
        for item in points:
            need_save = False
            current_time = int(time.strftime("%Y%m%d%H%M"))  # 获取当前时间，先按照固定格式转化成字符串，再转换成整数
            influx_time = datetime.datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            influx_time = int(datetime.datetime.strftime(influx_time, '%Y%m%d%H%M'))
            # 数据库目前只有10号的数据，所以判断是否是最新数据的两行代码先注释掉
            # if current_time - influx_time > 10:
            #     return
            measurement = ''
            if type_name == 'PH传感器':
                if float(item['ph']) > sensor_threshold:
                    measurement = item['ph']
                    need_save = True
            if type_name == 'ORP传感器':
                if float(item['orp']) > sensor_threshold:
                    measurement = item['orp']
                    need_save = True
            if type_name == '温度传感器':
                if float(item['temper']) > sensor_threshold:
                    measurement = item['temper']
                    need_save = True
            if type_name == '电导率传感器':
                if float(item['conduct']) > sensor_threshold:
                    measurement = item['conduct']
                    need_save = True
            if need_save:  # 如果need_save=True
                aid = uuid.uuid4().hex
                notice_time = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间，并改成对应格式
                sql_1 = "INSERT water_quality_notice (aid, sensor_id, measurement, notice_time,  deal_status)  " \
                        "VALUES ('%s', '%s', %s, '%s',1)" % (aid, sensor_id, measurement, notice_time,)
                cursor.execute(sql_1)
                db.commit()
    # 关闭数据库连接
    db.close()

