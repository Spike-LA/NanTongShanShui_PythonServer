# 定时任务的任务函数
import uuid
import pymysql
import time
from influxdb import InfluxDBClient
import datetime

from App.functions.dict_fetchall import dict_fetchall


# 水质提醒记录的定时任务
def task():
    # 连接数据库
    db = pymysql.connect("122.51.80.50", "root", "lab325", "ntss", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = 'SELECT * FROM (SELECT equipment_and_sensor.equipment_id,equipment_and_sensor.sensor_id,equipment.`status`,equipment.equipment_code,sensor.high_sensor_threshold,sensor.down_sensor_threshold,sensor_type.type_name FROM equipment ' \
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
        high_sensor_threshold_str = obj['high_sensor_threshold']
        down_sensor_threshold_str = obj['down_sensor_threshold']

        # 获取实时数据
        sql_1 = "SELECT * FROM real_time_data where equipment_code=%s"
        cursor.execute(sql_1,equipment_code)
        result_of_real_data = dict_fetchall(cursor)
        for real_data_obj in result_of_real_data: # 遍历该设备的每一条实时数据对象（每一条数据都是一个字典）
            need_save = False
            time_now = datetime.datetime.now() # 获取当前时间
            if time_now-real_data_obj['update_time']>datetime.timedelta(seconds=300): # 如果这个实时数据与当前时间超过5分钟时差，则不进行操作
                pass
            else:
                measurement_and_unit = ''
                if type_name == 'PH传感器' and real_data_obj['measure_type'] == '酸碱度':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('pH',''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('pH',''))
                    measurement = float(real_data_obj['measurement'].replace('pH',''))
                    if measurement< down_sensor_threshold or measurement> high_sensor_threshold:
                        need_save = True
                if type_name == '浊度传感器' and real_data_obj['measure_type'] == '浊度':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('NTU', ''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('NTU', ''))
                    measurement = float(real_data_obj['measurement'].replace('NTU', ''))
                    if measurement < down_sensor_threshold or measurement > high_sensor_threshold:
                        need_save = True
                if type_name == 'ORP传感器' and real_data_obj['measure_type'] == 'ORP':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('mv', ''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('mv', ''))
                    measurement = float(real_data_obj['measurement'].replace('mv', ''))
                    if measurement < down_sensor_threshold or measurement > high_sensor_threshold:
                        need_save = True
                if type_name == '电导率传感器' and real_data_obj['measure_type'] == '电导率':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('uS/cm', ''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('uS/cm', ''))
                    measurement = float(real_data_obj['measurement'].replace('uS/cm', ''))
                    if measurement < down_sensor_threshold or measurement > high_sensor_threshold:
                        need_save = True
                if type_name == '腐蚀率传感器' and real_data_obj['measure_type'] == '腐蚀率':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('mm/a', ''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('mm/a', ''))
                    measurement = float(real_data_obj['measurement'].replace('mm/a', ''))
                    if measurement < down_sensor_threshold or measurement > high_sensor_threshold:
                        need_save = True
                if type_name == '温度传感器' and real_data_obj['measure_type'] == '水温':
                    high_sensor_threshold = float(high_sensor_threshold_str.replace('℃', ''))
                    down_sensor_threshold = float(down_sensor_threshold_str.replace('℃', ''))
                    measurement = float(real_data_obj['measurement'].replace('℃', ''))
                    if measurement < down_sensor_threshold or measurement > high_sensor_threshold:
                        need_save = True
            if need_save:  # 如果need_save=True
                aid = uuid.uuid4().hex
                notice_time = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间，并改成对应格式
                measurement_and_unit = real_data_obj['measurement']
                sql_1 = "INSERT water_quality_notice (aid, sensor_id, measurement, notice_time,  deal_status)  " \
                        "VALUES ('%s', '%s', '%s', '%s',1)" % (aid, sensor_id, measurement_and_unit, notice_time,)
                cursor.execute(sql_1)
                db.commit()
    # 关闭数据库连接
    db.close()

