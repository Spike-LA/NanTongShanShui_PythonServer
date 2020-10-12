import json

from django.core.paginator import Paginator
from django.http import JsonResponse

from App.functions.condition_search import maintenances, maintenance
from App.models import EquipmentMaintenance, ContactPeople, SensorType, SensorModel
from App.serializers.client_serializer import ClientSerializer
from App.serializers.contact_people_serializer import ContactPeopleSerializer
from App.serializers.equipment_maintenance_serializer import EquipmentMaintenanceSerializer


def type_model(request):  # 设备类型与设备型号进行连表搜索，显示类型名、型号名、状态、备注。用原生sql分页并转换为分页对象再格式化成json传给前端
    # http://10.21.1.48:8000/app/typemodel/?type_name=COD传感器&sensor_model=COD8-G07&page=2&size=2
    if request.method == "GET":

        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回
            page = 1
            size = 5
        type_name = request.GET.get("type_name")
        sensor_model = request.GET.get("sensor_model")
        sql_1 = "SELECT * FROM (SELECT type_name,sensor_model,status,note,sensor_code FROM sensor_type" \
                      " INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id INNER JOIN sensor" \
                      " ON sensor_model.aid=sensor.sensor_model_id) AS a"
        a = "type_name=%s"
        b = "sensor_model=%s"

        if type_name:
            if sensor_model:
                sql = sql_1 + " where "+a + " and " + b
                table = [type_name, sensor_model]
            else:
                sql = sql_1 + " where " + a
                table = [type_name]
        else:
            if sensor_model:
                sql = sql_1 + " where " + b
                table = [sensor_model]

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
        "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
    }
    return JsonResponse(data=data)  # 对象



def operation(request):  # 设备表、调拨表、客户表进行连表操作，显示设备编码、设备状态、客户单位、客户单位所在地区
    # http://10.21.1.106:8000/app/operation/?region=地区&status=设备状态&client_unit=客户单位&page=2&size=2
    if request.method == "GET":
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回（page和size有一个为空则为True,执行默认分页)
            page = 1
            size = 5
        region = request.GET.get('region')
        status = request.GET.get('status')
        client_unit = request.GET.get('client_unit')
        sql_1 = "SELECT * from (SELECT equipment.aid,equipment.status,equipment.equipment_code,client.client_unit," \
                          "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
                          "INNER JOIN client ON equipment_allocation.client_id=client.aid) AS a"
        a = "region=%s"
        b = "status=%s"
        c = "client_unit=%s"
        if region:
            if status:
                if client_unit:
                    sql = sql_1 + " where "+a+" and "+b+" and "+c
                    table = [region, status, client_unit]
                else:
                    sql = sql_1 + " where "+a+" and "+b
                    table = [region, status]
            else:
                if client_unit:
                    sql = sql_1 + " where "+a+" and "+c
                    table = [region, client_unit]
                else:
                    sql = sql_1 + " where " + a
                    table = [region]
        else:
            if status:
                if client_unit:
                    sql = sql_1 + " where " + b + " and " + c
                    table = [status, client_unit]
                else:
                    sql = sql_1 + " where " + b
                    table = [status]
            else:
                if client_unit:
                    sql = sql_1 + " where " + c
                    table = [client_unit]
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
        "data": list(queryset)  # JsonResponse消除返回的结果中带的反斜杠
    }
    return JsonResponse(data=data)  # 对象


# 用于查询单个设备的维护报修记录
def equipmentmaintenance(request):
    if request.method == "GET":
        begin_time = request.GET.get('begin_time')
        end_time = request.GET.get('end_time')
        maintain_cause = request.GET.get('maintain_cause')
        equipment_id = request.GET.get('equipment_id')
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回（page和size有一个为空则为True,执行默认分页)
            page = 1
            size = 5
        if begin_time is None or end_time is None:  # 自定义时间范围查找
            if maintain_cause:  # 通过维护原因查找
                que = EquipmentMaintenance.objects.filter(equipment_id=equipment_id).filter(maintain_cause=maintain_cause)
            else:  # 无条件查找
                que = EquipmentMaintenance.objects.filter(equipment_id=equipment_id)
        else:
            if maintain_cause:  # 通过维护原因和时间范围查找
                que = EquipmentMaintenance.objects.filter(equipment_id=equipment_id).filter(
                    repair_time__gte=begin_time).filter(repair_time__lte=end_time).filter(maintain_cause=maintain_cause)
            else:  # 通过时间范围查找
                que = EquipmentMaintenance.objects.filter(equipment_id=equipment_id).filter(repair_time__gte=begin_time).filter(repair_time__lte=end_time)
        num = len(que)  # 共计几个对象
        serializer = EquipmentMaintenanceSerializer(instance=que, many=True)  # 利用序列化器将查询集转化为有序字典
        data_1 = serializer.data
        paginator = Paginator(data_1, size)  # 确定分页器对象
        data_2 = paginator.page(page)  # 当前页的数据
        data = {
            "count": num,
            "data": list(data_2)
        }
    return JsonResponse(data=data)

# 每个用户对应的各个联系人的信息查询
def clientcontactpeople(request):
    if request.method == 'GET':
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回（page和size有一个为空则为True,执行默认分页)
            page = 1
            size = 5
        client_id = request.GET.get('client_id')
        que = ContactPeople.objects.filter(client_id=client_id)
        num = len(que)  # 共计几个对象
        serializer = ContactPeopleSerializer(instance=que, many=True)
        data_1 = serializer.data
        paginator = Paginator(data_1, size)  # 确定分页器对象
        data_2 = paginator.page(page)  # 当前页的数据
        data = {
            "count": num,
            "data": list(data_2)
        }
    return JsonResponse(data=data)


def real_time_monitoring(request):
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        page = request.GET.get("page")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if page is None or size is None:  # 默认返回（page和size有一个为空则为True,执行默认分页)
            page = 1
            size = 5
        sql = "SELECT * from (SELECT equipment.aid,equipment.status,equipment.equipment_code,client.client_unit," \
                "client.region FROM equipment INNER JOIN equipment_allocation ON equipment.aid=equipment_allocation.equipment_id " \
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
            data.append(data_1)
    return JsonResponse(data=data, safe=False)

# 用于获取对应传感器类型下的传感器型号和型号id
def sensortypetomodel(request):
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
                data_2.append(data_3)

    return JsonResponse(data=data_2, safe=False)

