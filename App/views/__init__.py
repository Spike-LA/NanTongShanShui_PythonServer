import json

from django.core.paginator import Paginator
from django.http import JsonResponse


from App.functions.condition_search import maintenances, maintenance



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

                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id INNER JOIN sensor" \
                      " ON sensor_model.aid=sensor.sensor_model_id) AS a WHERE type_name=%s AND sensor_model=%s"
                table = [type_name, sensor_model]
                results = maintenances(sql, table)

                num = len(results)  # 共计几个对象
                paginator = Paginator(results, size)  # 转为限制行数(size)的paginator对象
                # total = paginator.count  # 计算总行数
                queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
                items = json.dumps(list(queryset))  # 将数据类型进行json格式的编码
                # return JsonResponse(json.loads(items), safe=False)  # 将json格式数据转换为字典可以消除JsonResponse返回的结果中带的反斜杠
                data = {
                    "count": num,
                    "data": json.loads(items)  # JsonResponse消除返回的结果中带的反斜杠
                }
            else:
                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id INNER JOIN sensor " \
                      "ON sensor_model.aid=sensor.sensor_model_id) AS a WHERE type_name=%s"
                table = [type_name]
                results = maintenances(sql, table)


                num = len(results)
                paginator = Paginator(results, size)
                queryset = paginator.page(page)
                items = json.dumps(list(queryset))

                data = {
                    "count": num,
                    "data": json.loads(items)
                }
        else:
            if sensor_model:
                sql = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id INNER JOIN sensor ON" \
                      " sensor_model.aid=sensor.sensor_model_id) AS a WHERE sensor_model=%s"
                table = [sensor_model]
                results = maintenances(sql, table)

                num = len(results)
                paginator = Paginator(results, size)
                queryset = paginator.page(page)
                items = json.dumps(list(queryset))

                data = {
                    "count": num,
                    "data": json.loads(items)
                }

            else:
                sql = "SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type " \
                      "INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id " \
                      "INNER JOIN sensor ON sensor_model.aid=sensor.sensor_model_id"
                results = maintenance(sql)

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
    # http://10.21.1.48:8000/app/operation/?region=地区&status=设备状态&client_unit=客户单位&page=2&size=2
    if request.method == "GET":
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回（page和size有一个为空则为True,执行默认分页)
            page = 1
            size = 5
        region = request.GET.get('region')
        status = request.GET.get('status')
        client_unit = request.GET.get('client_unit')
        if region:
            if status:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where region=%sand status=%s and client_unit=%s"
                    table = [region, status, client_unit]
                    results = maintenances(sql, table)  # 001
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
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where region=%sand status=%s"
                    table = [region, status]
                    results = maintenances(sql, table)  # 001
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
            else:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where region=%s and client_unit=%s"
                    table = [region, client_unit]
                    results = maintenances(sql, table)  # 001
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
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where region=%s"
                    table = [region]
                    results = maintenances(sql, table)  # 001
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
        else:
            if status:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where status=%s and client_unit=%s"
                    table = [status, client_unit]
                    results = maintenances(sql, table)  # 001
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
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where status=%s"
                    table = [status]
                    results = maintenances(sql, table)  # 001
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
            else:
                if client_unit:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where client_unit=%s"
                    table = [client_unit]
                    results = maintenances(sql, table)  # 001
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
                else:
                    sql = "SELECT * from (SELECT equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment LEFT JOIN equipment_scrap ON equipment.aid=equipment_scrap.equipment_id " \
                          "RIGHT JOIN client ON equipment_scrap.client_id=client.aid) AS a "
                    results = maintenance(sql)  # 000
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
