

from App.functions import maintenance


import json

from django.core.paginator import Paginator
from django.db import connection
from django.http import JsonResponse

from App.views_constant import b, dict_fetchall



def type_model(request):  # 设备类型与设备型号进行连表搜索，显示类型名、型号名、状态、备注。用原生sql分页并转换为分页对象再格式化成json传给前端
    # http://10.21.1.48:8000/app/typemodel/?type_name=COD传感器&sensor_model=COD8-G07&page=2&size=2
    if request.method == "GET":

        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回
            page = 1
            size = 5
        type_name = request.GET.get("type_name")
        sensor_model = request.GET.get("sensor_model")
        if type_name:
            if sensor_model:
                cursor = connection.cursor()
                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " LEFT JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id LEFT JOIN sensor" \
                      " ON sensor_model.aid=sensor.sensor_model_id) AS a WHERE type_name=%s AND sensor_model=%s"
                cursor.execute(sql, [type_name, sensor_model])
                results = dict_fetchall(cursor)
                cursor.close()

                num = len(results)  # 共计几个对象
                paginator = Paginator(results, size)  # 转为限制行数的paginator对象
                # total = paginator.count  # 计算总行数
                queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
                items = json.dumps(list(queryset))  # 将数据类型进行json格式的编码
                # return JsonResponse(json.loads(items), safe=False)  # 将json格式数据转换为字典可以消除JsonResponse返回的结果中带的反斜杠
                data = {
                    "count": num,
                    "data": json.loads(items)  # JsonResponse消除返回的结果中带的反斜杠
                }

                return JsonResponse(data=data)  # 对象
            else:
                cursor = connection.cursor()
                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " LEFT JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id LEFT JOIN sensor " \
                      "ON sensor_model.aid=sensor.sensor_model_id) AS a WHERE type_name=%s"
                cursor.execute(sql, type_name)
                results = dict_fetchall(cursor)
                cursor.close()

                num = len(results)
                paginator = Paginator(results, size)
                queryset = paginator.page(page)
                items = json.dumps(list(queryset))

                data = {
                    "count": num,
                    "data": json.loads(items)
                }

                return JsonResponse(data=data)
        else:
            if sensor_model:
                cursor = connection.cursor()
                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " LEFT JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id LEFT JOIN sensor ON" \
                      " sensor_model.aid=sensor.sensor_model_id) AS a WHERE sensor_model=%s"
                cursor.execute(sql, sensor_model)
                results = dict_fetchall(cursor)
                cursor.close()

                num = len(results)
                paginator = Paginator(results, size)
                queryset = paginator.page(page)
                items = json.dumps(list(queryset))

                data = {
                    "count": num,
                    "data": json.loads(items)
                }

                return JsonResponse(data=data)
            else:
                cursor = connection.cursor()
                cursor.execute("SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type LEFT JOIN "
                               "sensor_model ON sensor_type.aid=sensor_model.sensor_type_id LEFT JOIN sensor ON "
                               "sensor_model.aid=sensor.sensor_model_id")
                results = dict_fetchall(cursor)
                cursor.close()

                num = len(results)
                paginator = Paginator(results, size)
                queryset = paginator.page(page)
                items = json.dumps(list(queryset))

                data = {
                    "count": num,
                    "data": json.loads(items)
                }

                return JsonResponse(data=data)


def operation(request):  # 设备表、调拨表、客户表进行连表操作，显示设备编码、设备状态、客户单位、客户单位所在地区
    if request.method == "GET":
        region = request.GET.get('region')
        status = request.GET.get('status')
        client_unit = request.GET.get('client_unit')
        if region:
            if status:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where region='%s'and status='%s' and client_unit='%s'" \
                          % (region, status, client_unit)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 111
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where region='%s'and status='%s'" \
                          % (region, status)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 110
            else:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where region='%s' and client_unit='%s'" \
                          % (region, client_unit)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 101
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where region='%s'" \
                          % (region)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 100
        else:
            if status:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where status='%s' and client_unit='%s'" \
                          % (status, client_unit)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 011
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where status='%s'" \
                          % (status)
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 010
            else:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a where client_unit='%s'" \
                          % (client_unit)
                    data = maintenance(sql)  # 001
                    return JsonResponse(data=data)
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a "
                    data = maintenance(sql)
                    return JsonResponse(data=data)  # 000





