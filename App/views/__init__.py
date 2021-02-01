import json
import datetime

import xlwt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from influxdb_metrics.utils import query

from App.functions.condition_search import maintenances, maintenance
from App.models import EquipmentMaintenance, ContactPeople, SensorType, SensorModel, Sensor, Equipment, \
    EquipmentAndSensor, MainEngine, User, Role, PowerRelation, Power, EquipmentAllocation, WebsocketRelation, Pump
from App.serializers.contact_people_serializer import ContactPeopleSerializer
from App.serializers.equipment_maintenance_serializer import EquipmentMaintenanceSerializer
from App.serializers.sensor_serializer import SensorSerializer
from App.views_constant import stop_run, equipped


def type_model(request):  # 设备类型与设备型号进行连表搜索，显示类型名、型号名、状态、备注。用原生sql分页并转换为分页对象再格式化成json传给前端
    # http://10.21.1.48:8000/app/typemodel/?type_name=COD传感器&sensor_model=COD8-G07&page=2&size=2
    if request.method == "GET":

        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        type_name = request.GET.get("type_name")
        sensor_model = request.GET.get("sensor_model")
        sensor_code = request.GET.get('sensor_code')
        status = request.GET.get('status')
        sql = "SELECT * FROM (SELECT DISTINCT sensor.aid,sensor.sensor_threshold,sensor.notice_content," \
              "sensor.default_compensation,sensor.theoretical_value,type_name,sensor_model,note,sensor_code," \
              "sensor.`status` FROM sensor_type INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id " \
              "INNER JOIN sensor ON sensor_model.aid=sensor.sensor_model_id) AS a"

        a = "type_name=%s"
        b = "sensor_model=%s"
        c = "sensor_code=%s"
        d = "status=%s"

        child_sql = []
        child_params = []
        if type_name:
            child_sql.append(a)
            child_params.append(type_name)
        if sensor_model:
            child_sql.append(b)
            child_params.append(sensor_model)
        if sensor_code:
            child_sql.append(c)
            child_params.append(sensor_code)
        if status:
            child_sql.append(d)
            child_params.append(status)

        number = len(child_sql)

        if number >= 1:
            if number == 1:
                sql = sql + ' where ' + child_sql[0]
            else:
                sql = sql + ' where ' + child_sql[0]
                for i in child_sql[1:]:
                    sql = sql + ' and ' + i
        else:
            sql = sql
        if len(child_params) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, child_params)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


def operation(request):  # 设备表、调拨表、客户表进行连表操作，显示设备编码、设备状态、客户单位、客户单位所在地区
    # http://10.21.1.106:8000/app/operation/?region=地区&status=设备状态&client_unit=客户单位&page=2&size=2
    if request.method == "GET":
        # page = request.GET.get("page")  # 第几页
        # size = request.GET.get("size")  # 每页多少
        # if not page:
        #     page = 1
        #     size = 5
        # if not size:
        #     page = 1
        #     size = 5
        region = request.GET.get('region')
        status = request.GET.get('status')
        client_unit = request.GET.get('client_unit')
        client_id = request.GET.get('client_id')
        sql_1 = "SELECT * from (SELECT DISTINCT equipment.aid,equipment.status,equipment.equipment_code,client.client_unit,client.aid as client_id," \
                "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a"
        a = "region=%s"
        b = "status=%s"
        c = "client_unit=%s"
        d = "client_id=%s"
        # if region:
        #     if status:
        #         if client_unit:
        #             sql = sql_1 + " where "+a+" and "+b+" and "+c
        #             table = [region, status, client_unit]
        #         else:
        #             sql = sql_1 + " where "+a+" and "+b
        #             table = [region, status]
        #     else:
        #         if client_unit:
        #             sql = sql_1 + " where "+a+" and "+c
        #             table = [region, client_unit]
        #         else:
        #             sql = sql_1 + " where " + a
        #             table = [region]
        # else:
        #     if status:
        #         if client_unit:
        #             sql = sql_1 + " where " + b + " and " + c
        #             table = [status, client_unit]
        #         else:
        #             sql = sql_1 + " where " + b
        #             table = [status]
        #     else:
        #         if client_unit:
        #             sql = sql_1 + " where " + c
        #             table = [client_unit]
        #         else:
        #             sql = sql_1
        #             # sql = sql_1 + " where `status`!= 1 AND `status`!= 2 "
        #             table = []
        if region:
            if status:
                if client_unit:
                    if client_id:  # 1111
                        sql = sql_1 + " where " + a + " and " + b + " and " + c + " and " + d
                        table = [region, status, client_unit, client_id]
                    else:  # 1110
                        sql = sql_1 + " where " + a + " and " + b + " and " + c
                        table = [region, status, client_unit]
                else:
                    if client_id:  # 1101
                        sql = sql_1 + " where " + a + " and " + b + " and " + d
                        table = [region, status, client_id]
                    else:  # 1100
                        sql = sql_1 + " where " + a + " and " + b
                        table = [region, status]
            else:
                if client_unit:
                    if client_id:  # 1011
                        sql = sql_1 + " where " + a + " and " + c + " and " + d
                        table = [region, client_unit, client_id]
                    else:  # 1010
                        sql = sql_1 + " where " + a + " and " + c
                        table = [region, client_unit]
                else:
                    if client_id:  # 1001
                        sql = sql_1 + " where " + a + " and " + d
                        table = [region, client_id]
                    else:  # 1000
                        sql = sql_1 + " where " + a
                        table = [region]
        else:
            if status:
                if client_unit:
                    if client_id:  # 0111
                        sql = sql_1 + " where " + b + " and " + c + " and " + d
                        table = [status, client_unit, client_id]
                    else:  # 0110
                        sql = sql_1 + " where " + b + " and " + c
                        table = [status, client_unit]
                else:
                    if client_id:  # 0101
                        sql = sql_1 + " where " + b + " and " + d
                        table = [status, client_id]
                    else:  # 0100
                        sql = sql_1 + " where " + b
                        table = [status]
            else:
                if client_unit:
                    if client_id:  # 0011
                        sql = sql_1 + " where " + c + " and " + d
                        table = [client_unit, client_id]
                    else:  # 0010
                        sql = sql_1 + " where " + c
                        table = [client_unit]
                else:
                    if client_id:  # 0001
                        sql = sql_1 + " where " + d
                        table = [client_id]
                    else:  # 0000
                        sql = sql_1
                        table = []

        if len(table) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, table)
        num = len(results)  # 共计几个对象
        # paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        # queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(results)  # JsonResponse消除返回的结果中带的反斜杠
        }

    return JsonResponse(data=data)  # 对象


# 用于查询单个设备的维护报修记录
def equipmentmaintenance(request):
    if request.method == "GET":
        begin_time = request.GET.get('begin_time')
        end_time = request.GET.get('end_time')
        maintain_cause = request.GET.get('maintain_cause')
        equipment_id = request.GET.get('equipment_id')
        currentPage = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not currentPage:
            currentPage = 1
            size = 5
        if not size:
            currentPage = 1
            size = 5

        if not begin_time:
            if not end_time:
                if maintain_cause:  # 通过维护原因查找 001
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(
                        equipment_id=equipment_id).filter(maintain_cause=maintain_cause)
                else:  # 无条件查找 000
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id)
            else:
                if maintain_cause:  # 通过维护原因和end_time查找 011
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id). \
                        filter(repair_time__lte=end_time).filter(maintain_cause=maintain_cause)
                else:  # 通过end_time查找 010
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter \
                        (repair_time__lte=end_time)
        else:
            if not end_time:
                if maintain_cause:  # 通过维护原因和begin_time查找 101
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter \
                        (repair_time__gte=begin_time).filter(maintain_cause=maintain_cause)
                else:  # 通过begin_time查找 100
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter \
                        (repair_time__gte=begin_time)
            else:
                if maintain_cause:  # 通过维护原因和时间范围查找 111
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter \
                        (repair_time__gte=begin_time).filter(repair_time__lte=end_time).filter(
                        maintain_cause=maintain_cause)
                else:  # 通过end_time、begin_time查找 110
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter \
                        (repair_time__gte=begin_time).filter(repair_time__lte=end_time)
        num = len(que)  # 共计几个对象
        serializer = EquipmentMaintenanceSerializer(instance=que, many=True)  # 利用序列化器将查询集转化为有序字典
        data_1 = serializer.data
        paginator = Paginator(data_1, size)  # 确定分页器对象
        data_2 = paginator.page(currentPage)  # 当前页的数据
        data = {
            "count": num,
            "data": list(data_2)
        }
    return JsonResponse(data=data)


# 每个用户对应的各个联系人的信息查询
def clientcontactpeople(request):
    # http://10.21.1.106:8000/app/ClientContactPeople/?&client_id=&currentPage=2&size=2
    if request.method == 'GET':
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        client_id = request.GET.get('client_id')
        que = ContactPeople.objects.filter(client_id=client_id)
        num = len(que)  # 共计几个对象
        if num > 0:
            serializer = ContactPeopleSerializer(instance=que, many=True)
            data_1 = serializer.data
            paginator = Paginator(data_1, size)  # 确定分页器对象
            data_2 = paginator.page(page)  # 当前页的数据
            data = {
                "count": num,
                "data": list(data_2)
            }
        else:
            data = []

        return JsonResponse(data=data, safe=False)


# 实时监控接口（页面上部）
def real_time_monitoring_high(request):
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        sql = "SELECT * from (SELECT DISTINCT equipment.aid,equipment.status,equipment.equipment_code,client.client_unit," \
              "client.region,equipment_allocation.client_id FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
              "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a where aid =%s"
        table = [equipment_id]
        result = maintenances(sql, table)
        num = len(result)  # 共计几个对象
        paginator = Paginator(result, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


# 用于向前端返回所有的传感器类型和类型id
def sensortype(request):
    if request.method == 'GET':
        queryset = SensorType.objects.all()
        data = []
        for obj in queryset:
            data_1 = {}
            data_1['aid'] = obj.aid
            data_1['type_name'] = obj.type_name
            data_1['state'] = obj.state
            data.append(data_1)
    return JsonResponse(data=data, safe=False)


# 用于获取对应传感器类型下的传感器型号和型号id
def sensortypetomodel(request):
    # http://10.21.1.106:8000/app/sensor_type_to_model/?type_name=
    if request.method == 'GET':
        type_name = request.GET.get('type_name')
        queryset_1 = SensorType.objects.filter(type_name=type_name)
        data_1 = []
        data_2 = []
        for obj_1 in queryset_1:
            data_1.append(obj_1.aid)
        for aid in data_1:
            queryset_2 = SensorModel.objects.filter(sensor_type_id=aid)
            for obj_2 in queryset_2:
                data_3 = {}
                data_3['aid'] = obj_2.aid
                data_3['sensor_model'] = obj_2.sensor_model
                data_3['states'] = obj_2.states
                data_2.append(data_3)

    return JsonResponse(data=data_2, safe=False)


# 设备信息页面的查询和搜索
def equipmenttoenginename(request):
    # http://10.21.1.106:8000/app/equipment_to_engine_name/?engine_code=&equipment_code=&currentPage=&size=
    if request.method == 'GET':
        engine_code = request.GET.get('engine_code')
        equipment_code = request.GET.get('equipment_code')
        status = request.GET.get('status')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        sql = "SELECT * from (SELECT DISTINCT equipment.status,equipment.equip_person,equipment.aid AS equipment_id,equipment.engine_code,equipment.equipment_code,main_engine.engine_name,main_engine.aid AS engine_id,equipment.storehouse,equipment.storage_location,equipment.note " \
              "FROM equipment " \
              "INNER JOIN main_engine ON equipment.engine_code=main_engine.engine_code) AS a "

        a = "engine_code=%s"
        b = "equipment_code=%s"
        c = "status=%s"
        child_sql = []
        child_params = []
        if engine_code:
            child_sql.append(a)
            child_params.append(engine_code)
        if equipment_code:
            child_sql.append(b)
            child_params.append(equipment_code)
        if status:
            child_sql.append(c)
            child_params.append(status)

        number = len(child_sql)
        if number >= 1:
            if number == 1:
                sql = sql + ' where ' + child_sql[0]
            else:
                sql = sql + ' where ' + child_sql[0]
                for i in child_sql[1:]:
                    sql = sql + ' and ' + i
        else:
            sql = sql
        print(sql)
        if len(child_params) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, child_params)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


# 设备表、传感器表、传感器类型表、传感器型号表四表级联
# 用于通过设备id(用户端)给前端传输对应设备上的传感器编码、传感器型号、传感器类型、默认阈值
# 用于通过设备code(硬件端)给硬件传输(修改)对应设备上的传感器编码、传感器型号、传感器类型、默认阈值
def equipmenttosensor3(request):
    # http://10.21.1.106:8000/app/equipment_to_sensor3/?equipment_id=&currentPage=&size=
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        equipment_code = request.GET.get('equipment_code')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
        if not size:
            size = 5
        a = 'equipment_id=%s'
        b = 'equipment_code=%s'
        sql_1 = "SELECT * from (SELECT DISTINCT sensor_type.unit,sensor.aid,sensor.sensor_code,sensor_model.sensor_model," \
                "sensor.high_sensor_threshold,sensor.down_sensor_threshold,sensor_type.type_name,equipment_and_sensor.equipment_id,equipment_code,equipment_and_sensor.sensor_id " \
                "FROM equipment_and_sensor " \
                "INNER JOIN equipment " \
                "ON equipment.aid=equipment_and_sensor.equipment_id " \
                "INNER JOIN sensor " \
                "ON equipment_and_sensor.sensor_id=sensor.aid " \
                "INNER JOIN sensor_model " \
                "ON sensor.sensor_model_id=sensor_model.aid " \
                "INNER JOIN sensor_type " \
                "ON sensor_model.sensor_type_id=sensor_type.aid) AS a "
        if equipment_id:
            sql = sql_1+" where "+a
            table = [equipment_id]
        elif equipment_code:
            sql = sql_1 + " where " + b
            table = [equipment_code]
        else:
            sql = sql_1
            table = []

        if len(table) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, table)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)
        }
        return JsonResponse(data=data)


# 与时序数据库进行交互操作
def real_time_monitoring_down(request):
    if request.method == 'GET':
        deviceNum = request.GET.get('deviceNum')
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_begin = "T00:00:00.000000Z"
        time_end = "T23:59:59.000000Z"
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        tomorrow = today + oneday
        if not begin_time_first:
            if not end_time_first:
                begin_time_first = str(today)
                end_time_first = str(tomorrow)
                # 数据库只有10月10号的数据,之后完成的时候是用上面两行代码
                # begin_time_first = '2020-10-10'
                # end_time_first = '2020-10-11'
        begin_time = begin_time_first + time_begin
        end_time = end_time_first + time_end
        print(begin_time, end_time)
        sql = "select * from b where deviceNum='%s' and time >= '%s' and time <= '%s'" % (
            deviceNum, begin_time, end_time)
        data = query(sql)
        print(data)
        if data:
            for result_list in data:
                return JsonResponse(data=result_list, safe=False)
        else:
            table = []
            return JsonResponse(data=table, safe=False)


# 通过传感器型号aid给前端发送对应的传感器的全局id和编码
def sensormodeltocode(request):
    # http://10.21.1.106:8000/app/sensor_model_to_code/?sensor_model_id=
    if request.method == "GET":
        sensor_model_id = request.GET.get('sensor_model_id')
        que = Sensor.objects.filter(sensor_model_id=sensor_model_id)
        serializer = SensorSerializer(instance=que, many=True)
        data = serializer.data
    return JsonResponse(data=data, safe=False)


# 通过设备编码获取对应设备上的传感器的aid,类型,标定理论值
def deviceNumtotypename(request):
    # http://10.21.1.106:8000/app/deviceNum_to_typename/?deviceNum=
    if request.method == 'GET':
        equipment_code = request.GET.get('deviceNum')
        query_1 = Equipment.objects.filter(equipment_code=equipment_code).first()  # 通过设备编号查到该设备对象
        # print(query_1)
        query_2 = EquipmentAndSensor.objects.filter(equipment_id=query_1.aid)
        # print(query_2)
        table_1 = []
        for obj_1 in query_2:
            table_1.append(obj_1.sensor_id)  # 获取该设备上的各个传感器id
        print(table_1)

        sql = "SELECT * FROM (SELECT DISTINCT sensor.sensor_code,sensor.aid,sensor_type.type_name,sensor_model.sensor_model,sensor.theoretical_value " \
              "FROM sensor " \
              "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
              "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid ) " \
              "AS a where aid=%s"

        data = []
        for obj_2 in table_1:
            results = maintenances(sql, obj_2)
            if len(results):
                data.append(results[0])
        return JsonResponse(data=data, safe=False)


# 水质记录查询
def waterqualitynotice(request):
    # http://10.21.1.106:8000/app/water_quality_notice/?currentPage=2&size=5&equipment_id=
    if request.method == 'GET':
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        equipment_id = request.GET.get('equipment_id')
        type_name = request.GET.get('type_name')
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_second_first = 'T00:00:00'
        time_second_end = 'T23:59:59'
        if begin_time_first:
            begin_time = begin_time_first + time_second_first
        if end_time_first:
            end_time = end_time_first + time_second_end
        a = 'notice_time >= %s'
        b = 'notice_time <= %s'
        c = 'type_name = %s'

        sql_first = "SELECT * FROM (SELECT DISTINCT equipment_id,measurement,water_quality_notice.sensor_id,type_name,sensor.notice_content,water_quality_notice.notice_time " \
                    "FROM water_quality_notice " \
                    "INNER JOIN sensor ON water_quality_notice.sensor_id=sensor.aid " \
                    "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
                    "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid " \
                    "INNER JOIN equipment_and_sensor ON sensor.aid=equipment_and_sensor.sensor_id " \
                    "INNER JOIN equipment ON equipment.aid=equipment_and_sensor.equipment_id) AS a WHERE equipment_id=%s"

        if not equipment_id:
            data = {
                'msg': '未发送唯一标识'
            }
            return JsonResponse(data=data)

        if begin_time_first:
            if end_time_first:
                if type_name:  # 111
                    sql = sql_first + ' and ' + a + ' and ' + b + ' and ' + c
                    table = [equipment_id, begin_time, end_time, type_name]
                else:  # 110
                    sql = sql_first + ' and ' + a + ' and ' + b
                    table = [equipment_id, begin_time, end_time]
            else:
                if type_name:  # 101
                    sql = sql_first + ' and ' + a + ' and ' + c
                    table = [equipment_id, begin_time, type_name]
                else:  # 100
                    sql = sql_first + ' and ' + a
                    table = [equipment_id, begin_time]
        else:
            if end_time_first:
                if type_name:  # 011
                    sql = sql_first + ' and ' + b + ' and ' + c
                    table = [equipment_id, end_time, type_name]
                else:  # 010
                    sql = sql_first + ' and ' + b
                    table = [equipment_id, end_time]
            else:
                if type_name:  # 001
                    sql = sql_first + ' and ' + c
                    table = [equipment_id, type_name]
                else:  # 000
                    sql = sql_first
                    table = [equipment_id]

        results = maintenances(sql, table)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)
        }
        return JsonResponse(data=data)


# 给前端传输所有主机编号都主机名称
def mainenginecodeandname(request):
    # http://10.21.1.106:8000/app/main_engine_code_and_name/
    if request.method == 'GET':
        query = MainEngine.objects.all()
        table = []
        for obj in query:
            dic = {}
            dic['engine_name'] = obj.engine_name
            dic['engine_code'] = obj.engine_code
            dic['status'] = obj.status
            if obj.status == '1':
                table.append(dic)
    return JsonResponse(data=table, safe=False)


# 实时监控界面的设备详情弹窗(前面五个)
def equipmentdetail(request):
    # http://10.21.1.106:8000/app/equipment_detail/?equipment_id=
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        if equipment_id:
            obj = EquipmentAndSensor.objects.filter(equipment_id=equipment_id).all()
            obj_1 = EquipmentAllocation.objects.filter(equipment_id=equipment_id).first()
            obj_2 = ContactPeople.objects.filter(client_id=obj_1.client_id).first()
            print(obj_2)
            if not obj:
                if not obj_2:
                    sql = "SELECT * FROM (SELECT DISTINCT equipment.aid AS equipment_id,main_engine.engine_code,main_engine." \
                          "engine_name FROM main_engine INNER JOIN equipment ON main_engine.engine_code=equipment.engine_code " \
                          "INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid ) AS a WHERE equipment_id=%s"
                else:
                    sql = "SELECT * FROM (SELECT DISTINCT equipment.aid AS equipment_id,main_engine.engine_code,main_engine." \
                          "engine_name,contact_people.contact_person,contact_people.contact_tel,contact_people.`status` FROM main_engine " \
                          "INNER JOIN equipment ON main_engine.engine_code=equipment.engine_code " \
                          "INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid " \
                          "INNER JOIN contact_people ON client.aid=contact_people.client_id) AS a WHERE equipment_id=%s"
            else:
                if not obj_2:
                    sql = "SELECT * FROM (SELECT DISTINCT equipment_and_sensor.equipment_id,main_engine.engine_code,main_" \
                          "engine.engine_name,sensor_type.type_name,sensor_model.sensor_model FROM main_engine " \
                          "INNER JOIN equipment ON main_engine.engine_code=equipment.engine_code " \
                          "INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid " \
                          "INNER JOIN equipment_and_sensor ON equipment.aid=equipment_and_sensor.equipment_id " \
                          "INNER JOIN sensor ON equipment_and_sensor.sensor_id=sensor.aid " \
                          "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
                          "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid) AS a WHERE equipment_id=%s"
                else:
                    sql = "SELECT * FROM (SELECT DISTINCT equipment_and_sensor.equipment_id,main_engine.engine_code," \
                          "main_engine.engine_name,contact_people.contact_person,contact_people.contact_tel," \
                          "sensor_type.type_name,sensor_model.sensor_model,contact_people.`status` " \
                          "FROM main_engine INNER JOIN equipment ON main_engine.engine_code=equipment.engine_code " \
                          "INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid " \
                          "INNER JOIN contact_people ON client.aid=contact_people.client_id " \
                          "INNER JOIN equipment_and_sensor ON equipment.aid=equipment_and_sensor.equipment_id " \
                          "INNER JOIN sensor ON equipment_and_sensor.sensor_id=sensor.aid " \
                          "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
                          "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid) AS a WHERE equipment_id=%s"
            table = [equipment_id]
            data = maintenances(sql, table)
            if len(data) > 0:
                return JsonResponse(data=data, safe=False)
            else:
                data = {
                    'msg': '设备标识不正确'
                }
                return JsonResponse(data=data)
        else:
            data = {
                'msg': '未发送设备唯一标识'
            }
            return JsonResponse(data=data)


@csrf_exempt
def loginin(request):
    # http://127.0.0.1:8000/app/login_in/
    if request.method == 'POST':
        # 从request中拿出body属性（二进制格式），利用decode方法解码成python格式，再利用replace方法将'替换为\"。之后用json模块的loads函数将其转化为
        # json（字典）格式，最后用get函数获取对应的键值
        account = json.loads(request.body.decode().replace("'", "\"")).get('account')
        password = json.loads(request.body.decode().replace("'", "\"")).get('password')
        obj = User.objects.filter(account=account).first()
        if obj:  # 账户存在
            if obj.password == password:  # 账户存在且密码正确

                data = {
                    'username': obj.name,
                    'user_id': obj.aid,
                    'role_id': obj.role_id,
                    'msg': '登陆成功',
                }

                user_object = User.objects.filter(account=account).first()  # 找到该用户对象
                user_object.login_status = 1  # 将该用户的登录状态设置为已登录
                user_object.save()

            else:  # 账户存在但密码不正确
                data = {
                    'msg': '密码不正确',
                }
        else:  # 账户不存在
            data = {
                'msg': '账户名不存在',
            }

    return JsonResponse(data=data, safe=False)


# 前端验证登陆状态时，返回给前端这个账号的所有权限别名以及该用户所关联的客户id
def verify(request):
    # http://127.0.0.1:8000/app/verify/?user_id=&role_id=
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        role_id = request.GET.get('role_id')
        query_role_power = PowerRelation.objects.filter(aim_id=role_id)
        query_user_power = PowerRelation.objects.filter(aim_id=user_id)
        obj = User.objects.filter(aid=user_id).first()
        list_power_id = []
        list_power_num = []

        for obj_1 in query_role_power:
            list_power_id.append(obj_1.power_id)

        for obj_2 in query_user_power:
            list_power_id.append(obj_2.power_id)

        for obj_3 in list_power_id:
            query_power_object = Power.objects.filter(aid=obj_3).first()
            list_power_num.append(query_power_object.power_num)

        data = {
            'count': len(list_power_num),
            'power_num': list_power_num,
            'client_id': obj.client_id
        }
    return JsonResponse(data=data, safe=False)


# 通过前端发送的设备编号，将设备对应传感器的类型、标定时间、标定理论值、标定实际值返回给前端
def sensorcalibrationretrieve(request):
    # http: // 127.0.0.1:8000/app/sensor_calibration_retrieve/?deviceNum=&currentPage=&size=&type_name=&begin_time=&end_time=
    if request.method == 'GET':
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        equipment_code = request.GET.get('deviceNum')
        type_name = request.GET.get('type_name')
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_second_begin = 'T00:00:00'
        time_second_end = 'T23:59:59'
        if begin_time_first:
            begin_time = begin_time_first + time_second_begin
        if end_time_first:
            end_time = end_time_first + time_second_end
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        a = 'calibrate_time>=%s'
        b = 'calibrate_time<=%s'
        c = 'type_name=%s'

        sql_1 = "SELECT * FROM (SELECT DISTINCT sensor_calibration.calibrate_time,sensor_calibration.actual_value,sensor_calibration.calibrate_compensation,sensor.theoretical_value,sensor_type.type_name,equipment.equipment_code " \
                "FROM sensor_calibration " \
                "INNER JOIN sensor ON sensor_calibration.sensor_id=sensor.aid " \
                "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
                "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid " \
                "INNER JOIN equipment_and_sensor ON sensor.aid=equipment_and_sensor.sensor_id " \
                "INNER JOIN equipment ON equipment_and_sensor.equipment_id=equipment.aid) AS a WHERE equipment_code=%s"

        if begin_time_first:
            if end_time_first:
                if type_name:  # 111
                    sql = sql_1 + ' and ' + a + ' and ' + b + ' and ' + c
                    table = [equipment_code, begin_time, end_time, type_name]
                else:  # 110
                    sql = sql_1 + ' and ' + a + ' and ' + b
                    table = [equipment_code, begin_time, end_time]
            else:
                if type_name:  # 101
                    sql = sql_1 + ' and ' + a + ' and ' + c
                    table = [equipment_code, begin_time, type_name]
                else:  # 100
                    sql = sql_1 + ' and ' + a
                    table = [equipment_code, begin_time]

        else:
            if end_time_first:
                if type_name:  # 011
                    sql = sql_1 + ' and ' + b + ' and ' + c
                    table = [equipment_code, end_time, type_name]
                else:  # 010
                    sql = sql_1 + ' and ' + b
                    table = [equipment_code, end_time]
            else:
                if type_name:  # 001
                    sql = sql_1 + ' and ' + c
                    table = [equipment_code, type_name]
                else:  # 000
                    sql = sql_1
                    table = [equipment_code]

        results = maintenances(sql, table)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)
        queryset = paginator.page(page)
        data = {
            "count": num,
            "data": list(queryset)
        }
        return JsonResponse(data=data)  # 对象


# 通过角色id查找角色对应的所有权限
def rolepowers(request):
    # http://10.21.1.106:8000/app/role_power/?role_id=
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        que = PowerRelation.objects.filter(aim_id=role_id)
        power_list = []
        power_num = []
        for power_relation_obj in que:
            power_list.append(power_relation_obj.power_id)
        for power_obj in power_list:
            obj = Power.objects.filter(aid=power_obj).first()
            power_num.append(obj.power_num)

        data = {
            'count': len(power_num),
            'data': power_num,
        }

    return JsonResponse(data=data, safe=False)


# 通过设备id查找对应设备上传感器的水质提醒记录
def waternoticeretrieve(request):
    # http://10.21.1.106:8000/app/water_notice_retrieve/?currentPage=&size=&equipment_id=&begin_time=&end_time=&type_name=&deal_status=
    if request.method == 'GET':
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        equipment_id = request.GET.get('equipment_id')
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_second_begin = 'T00:00:00'
        time_second_end = 'T23:59:59'
        if begin_time_first:
            begin_time = begin_time_first + time_second_begin
        if end_time_first:
            end_time = end_time_first + time_second_end
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        type_name = request.GET.get('type_name')
        deal_status = request.GET.get('deal_status')
        sql = "SELECT * FROM (SELECT DISTINCT water_quality_notice.aid,water_quality_notice.deal_status,water_quality_notice.notice_time,water_quality_notice.deal_time,sensor.notice_content,sensor_type.type_name, equipment_and_sensor.equipment_id " \
              "FROM water_quality_notice " \
              "INNER JOIN sensor ON water_quality_notice.sensor_id=sensor.aid " \
              "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
              "INNER JOIN sensor_type ON sensor_type.aid=sensor_model.sensor_type_id " \
              "INNER JOIN equipment_and_sensor ON sensor.aid=equipment_and_sensor.sensor_id " \
              "INNER JOIN equipment ON equipment_and_sensor.equipment_id=equipment.aid) AS a WHERE equipment_id=%s"

        a = 'notice_time>=%s'
        b = 'notice_time<=%s'
        c = 'type_name=%s'
        d = 'deal_status=%s'
        e = 'order by notice_time desc'
        child_sql = []
        child_params = []
        child_params.append(equipment_id)
        if begin_time_first:
            child_sql.append(a)
            child_params.append(begin_time)
        if end_time_first:
            child_sql.append(b)
            child_params.append(end_time)
        if type_name:
            child_sql.append(c)
            child_params.append(type_name)
        if deal_status:
            child_sql.append(d)
            child_params.append(deal_status)

        number = len(child_sql)
        if number > 0:
            for i in child_sql:
                sql = sql + ' and ' + i
        sql = sql + e
        if len(child_params) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, child_params)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


# 设备报废的查询和搜索
def equipmentscrapretrieve(request):
    # http://10.21.1.106:8000/app/equipment_scrap_retrieve/?currentPage=&size=&equipment_code=
    if request.method == 'GET':
        equipment_code = request.GET.get('equipment_code')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        sql_1 = "SELECT * FROM (SELECT DISTINCT equipment_scrap.applicant_time,main_engine.engine_code,main_engine.engine_name,equipment_scrap.scrapping_reasons,equipment_scrap.remark,equipment_scrap.applicant,equipment_scrap.applicant_tel,equipment.storehouse,equipment.storage_location,equipment.equipment_code,equipment_id,equipment_scrap.aid  " \
                "FROM equipment_scrap " \
                "INNER JOIN equipment " \
                "ON equipment_scrap.equipment_id=equipment.aid " \
                "INNER JOIN main_engine ON equipment_scrap.engine_id=main_engine.aid) AS a"

        if equipment_code:
            sql = sql_1 + ' where equipment_code=%s'
            table = [equipment_code]
        else:
            sql = sql_1
            table = []

        sql = sql + ' order by applicant_time desc'
        print(sql)
        if len(table) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, table)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)
        }
        return JsonResponse(data=data)


# 设备配置记录查询和搜索
def equipmentconfigurationretrieve(request):
    # http://10.21.1.106:8000/app/equipment_configuration_retrieve/?currentPage=&size=&equipment_code=&engine_code=&begin_time=&end_time=&
    if request.method == 'GET':
        engine_code = request.GET.get('engine_code')
        equipment_code = request.GET.get('equipment_code')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_second_begin = 'T00:00:00'
        time_second_end = 'T23:59:59'
        print(begin_time_first, end_time_first)
        if begin_time_first:
            begin_time = begin_time_first + time_second_begin
        if end_time_first:
            end_time = end_time_first + time_second_end

        sql = "SELECT * FROM (SELECT DISTINCT equipment.aid,equipment.alert_time,equipment.equip_person,equipment.equipment_code,equipment.storehouse,equipment.storage_location,main_engine.engine_code,main_engine.engine_name " \
              "FROM equipment " \
              "INNER JOIN main_engine ON equipment.engine_code=main_engine.engine_code) AS a "
        a = 'alert_time>=%s'
        b = 'alert_time<=%s'
        c = 'engine_code=%s'
        d = 'equipment_code=%s'

        print(sql)
        child_sql = []
        child_params = []
        if begin_time_first:
            child_sql.append(a)
            child_params.append(begin_time)
        if end_time_first:
            child_sql.append(b)
            child_params.append(end_time)
        if engine_code:
            child_sql.append(c)
            child_params.append(engine_code)
        if equipment_code:
            child_sql.append(d)
            child_params.append(equipment_code)

        length = len(child_sql)
        if length == 0:
            pass
        elif length == 1:
            sql = sql + ' where ' + child_sql[0]
        else:
            n = 1
            for i in child_sql:
                if n == 1:
                    sql = sql + ' where ' + i
                    n += 1
                else:
                    sql = sql + ' and ' + i

        sql = sql + ' order by alert_time desc'

        if len(child_params) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, child_params)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


# 设备调拨记录查询和搜索
def equipmentallocationretrieve(request):
    # http://10.21.1.106:8000/app/equipment_allocation_retrieve/?currentPage=&size=&status=&transfer_unit=&begin_time=&end_time=&
    if request.method == 'GET':
        transfer_unit = request.GET.get('transfer_unit')
        status = request.GET.get('status')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        begin_time_first = request.GET.get('begin_time')
        end_time_first = request.GET.get('end_time')
        time_second_begin = 'T00:00:00'
        time_second_end = 'T23:59:59'
        if begin_time_first:
            begin_time = begin_time_first + time_second_begin
        if end_time_first:
            end_time = end_time_first + time_second_end

        sql = "SELECT * FROM (SELECT DISTINCT equipment_allocation.aid,equipment_id,equipment.equipment_code,equipment.`status`,equipment_allocation.applicant_time,equipment_allocation.applicant,equipment_allocation.transfer_unit,equipment_allocation.transfer_unit_tel,equipment_allocation.transfer_unit_ads,equipment_allocation.allocation_reason,applicant_tel,equipment_allocation.remark " \
              "FROM equipment_allocation " \
              "INNER JOIN equipment ON equipment_allocation.equipment_id=equipment.aid) AS a "

        sql_1 = "SELECT DISTINCT equipment_allocation.aid,equipment_id,equipment.equipment_code,equipment.`status`,equipment_allocation.applicant_time,equipment_allocation.applicant,equipment_allocation.transfer_unit,equipment_allocation.transfer_unit_tel,equipment_allocation.transfer_unit_ads,equipment_allocation.allocation_reason,applicant_tel,equipment_allocation.remark " \
                "FROM equipment_allocation " \
                "INNER JOIN equipment ON equipment_allocation.equipment_id=equipment.aid"
        a = 'applicant_time>=%s'
        b = 'applicant_time<=%s'
        c = 'transfer_unit=%s'
        d = 'status=%s'

        child_sql = []
        child_params = []
        if begin_time_first:
            child_sql.append(a)
            child_params.append(begin_time)
        if end_time_first:
            child_sql.append(b)
            child_params.append(end_time)
        if transfer_unit:
            child_sql.append(c)
            child_params.append(transfer_unit)
        if status:
            child_sql.append(d)
            child_params.append(status)

        length = len(child_sql)
        if length == 0:
            sql = sql_1
        elif length == 1:
            sql = sql + ' where ' + child_sql[0]
        else:
            n = 1
            for i in child_sql:
                if n == 1:
                    sql = sql + ' where ' + i
                    n += 1
                else:
                    sql = sql + ' and ' + i

        sql = sql + ' order by applicant_time desc'

        if len(child_params) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, child_params)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
        return JsonResponse(data=data)  # 对象


@csrf_exempt
def equipmentallocatefactory(request):
    # http://10.21.1.106:8000/app/equipment_allocate_factory/
    if request.method == 'POST':
        equipment_id = json.loads(request.body.decode().replace("'", "\"")).get('equipment_id')
        storehouse = json.loads(request.body.decode().replace("'", "\"")).get('storehouse')
        storage_location = json.loads(request.body.decode().replace("'", "\"")).get('storage_location')
        print(equipment_id)
        equipment_obj = Equipment.objects.filter(aid=equipment_id).first()  # 找出调拨回厂的设备对象
        equipment_obj.status = stop_run  # 设置该设备的状态为停运
        if storehouse:
            equipment_obj.storehouse = storehouse
        if storage_location:
            equipment_obj.storage_location = storage_location
        equipment_obj.save()

    data = {
        'msg': "success"
    }

    return JsonResponse(data=data)


# 前端发送设备对象或用户对象id，返回给前端这个对象的websocket_id（前提是已登录）
def websocketrelation(request):
    # http://10.21.1.106:8000/app/websocket_relation/?object_code=&distinguish_code=&
    if request.method == 'GET':
        object_code = request.GET.get('object_code')
        distinguish_code = request.GET.get('distinguish_code')
        obj = WebsocketRelation.objects.filter(object_id=object_code).filter(distinguish_code=distinguish_code).first()
        if obj:
            websocket_id = obj.websocket_id
            data = {
                'websocket_id': websocket_id
            }
        else:
            data = {
                'msg': '该设备/用户未登录'
            }
    return JsonResponse(data=data, safe=False)


def logout(request):
    # http://127.0.0.1:8000/app/logout/?user_id=
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        user_object = User.objects.filter(aid=user_id).first()  # 找到该用户对象
        user_object.login_status = -1  # 将该用户的登录状态设置为未登录
        user_object.save()
        data = {
            'msg': '登出成功'
        }
    return JsonResponse(data=data, safe=False)


def getequippedpump1(request):
# http://127.0.0.1:8000/app/get_equipped_pump/?equipment_code=
    if request.method == 'GET':
        equipment_code = request.GET.get('equipment_code')
        if equipment_code:
            pump_query = Pump.objects.filter(status=equipped).filter(equipment_code=equipment_code)
            if pump_query:
                pump_object_list = []
                for object in pump_query:
                    dic = {}
                    dic['pump_name'] = object.pump_name
                    dic['pump_code'] = object.pump_code
                    dic['fluid_flow'] = object.fluid_flow
                    dic['note'] = object.note
                    pump_object_list.append(dic)
                data = {
                    'msg': '获取成功',
                    'count':len(pump_object_list),
                    'pump_object_list':pump_object_list,
                }
            else:
                data = {
                    'msg':'未获取到该设备上的泵'
                }
        else:
            pump_query = Pump.objects.filter(status=equipped)
            if pump_query:
                pump_object_list = []
                for object in pump_query:
                    dic = {}
                    dic['pump_id'] = object.pump_id
                    dic['equipment_code'] = object.equipment_code
                    dic['pump_name'] = object.pump_name
                    dic['pump_code'] = object.pump_code
                    dic['fluid_flow'] = object.fluid_flow
                    dic['note'] = object.note
                    pump_object_list.append(dic)
                data = {
                    'msg': '获取成功',
                    'count': len(pump_object_list),
                    'pump_object_list': pump_object_list,
                }
            else:
                data = {
                    'msg': '目前没有可分配权限的泵'
                }
    return JsonResponse(data=data, safe=False)


def pumpanduser1(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        pump_id = request.GET.get('pump_id')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5

        sql_1 = "SELECT * FROM (SELECT permission_id,user_id,pump_permission.pump_id,pump.pump_code,pump_name,equipment_code,fluid_flow,pump.`status` as pump_status,account,`name` as user_name, user.`status`AS user_status,role.role_name " \
                "FROM pump_permission " \
              "INNER JOIN pump ON pump_permission.pump_id=pump.pump_id " \
              "INNER JOIN `user` ON pump_permission.user_id=user.aid " \
              "INNER JOIN role ON role.aid=user.role_id) as a"

        table_1 = []
        table_2 = []
        if user_id:
            table_1.append("user_id=%s")
            table_2.append(user_id)
        if pump_id:
            table_1.append("pump_id=%s")
            table_2.append(pump_id)

        if len(table_1) == 0:
            sql = sql_1
        elif len(table_1) == 1:
            sql = sql_1 + " where "+table_1[0]
        else:
            sql = sql_1 + " where "+table_1[0]+ " and "+table_2[1]

        if len(table_1) == 0:
            results = maintenance(sql)
        else:
            results = maintenances(sql, table_2)
        num = len(results)  # 共计几个对象
        paginator = Paginator(results, size)  # 转为限制行数的paginator对象
        queryset = paginator.page(page)  # 根据前端的页数选择对应的返回结果
        data = {
            "count": num,
            "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
        }
    return JsonResponse(data=data)  # 对象


# 将时序数据库中的数据以Excel的形式导出
@csrf_exempt
def exportexcel(request):
    if request.method == 'POST':
        deviceNum = json.loads(request.body.decode().replace("'", "\"")).get('deviceNum')
        begin_time_first = json.loads(request.body.decode().replace("'", "\"")).get('begin_time')
        end_time_first = json.loads(request.body.decode().replace("'", "\"")).get('end_time')
        time_begin = "T00:00:00.000000Z"
        time_end = "T23:59:59.000000Z"
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        tomorrow = today + oneday
        if not begin_time_first:
            if not end_time_first:
                begin_time_first = str(today)
                end_time_first = str(tomorrow)
                # begin_time_first = '2020-10-10'
                # end_time_first = '2020-10-11'
        begin_time = begin_time_first + time_begin
        end_time = end_time_first + time_end
        print(begin_time, end_time)
        sql = "select * from b where deviceNum='%s' and time >= '%s' and time <= '%s'" % (
            deviceNum, begin_time, end_time)
        data = query(sql)
        for obj in data:
            result_list = obj
            sum = len(result_list)
        # excel导出0.1版本
        row0 = ["检测时间", "电导率传感器", "ORP传感器", "PH传感器", "温度传感器"]
        workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿

        worksheet = workbook.add_sheet('Sheet1')  # 添加名为Sheet1的工作表

        worksheet.write(0, 0, "设备编号")

        worksheet.write(1, 0, deviceNum)

        for i in range(0, len(row0)):  # 生成第一行
            worksheet.write(2, i, row0[i])
        num = 0
        while num < sum:
            for obj in result_list:
                del obj['deviceNum']
                res = [obj[key] for key in obj]
                for i in range(0, len(res)):
                    worksheet.write(num + 3, i, res[i])
                num += 1
        workbook.save('C:/Users/kaiss/Desktop/sensor.xls') # 本机的桌面
        message = {
            'msg': '导出成功'
        }
        return JsonResponse(data=message, safe=False)
