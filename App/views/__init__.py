from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from influxdb_metrics.utils import query

from App.functions.condition_search import maintenances, maintenance
from App.models import EquipmentMaintenance, ContactPeople, SensorType, SensorModel, Sensor
from App.serializers.contact_people_serializer import ContactPeopleSerializer
from App.serializers.equipment_maintenance_serializer import EquipmentMaintenanceSerializer
from App.serializers.sensor_serializer import SensorSerializer


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
        sql_1 = "SELECT * FROM (SELECT sensor.aid,type_name,sensor_model,note,sensor_code,status FROM sensor_type" \
                      " INNER JOIN sensor_model ON sensor_type.aid=sensor_model.sensor_type_id INNER JOIN sensor" \
                      " ON sensor_model.aid=sensor.sensor_model_id) AS a"
        a = "type_name=%s"
        b = "sensor_model=%s"
        c = "sensor_code=%s"
        if type_name:
            if sensor_model:
                if sensor_code:  # 111
                    sql = sql_1 + " where "+a + " and " + b + " and " + c
                    table = [type_name, sensor_model, sensor_code]
                else:  # 110
                    sql = sql_1 + " where "+a + " and " + b
                    table = [type_name, sensor_model]
            else:
                if sensor_code: # 101
                    sql = sql_1 + " where "+a + " and " + c
                    table = [type_name, sensor_code]
                else:  # 100
                    sql = sql_1 + " where " + a
                    table = [type_name]
        else:
            if sensor_model:
                if sensor_code:  # 011
                    sql = sql_1 + " where " + b + " and " + c
                    table = [sensor_model, sensor_code]
                else:  # 010
                    sql = sql_1 + " where " + b
                    table = [sensor_model]
            else:
                if sensor_code: # 001
                    sql = sql_1 + " where " + c
                    table = [sensor_code]
                else:  # 000
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
        if not page:
            page = 1
            size = 5
        if not size:
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
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter(maintain_cause=maintain_cause)
                else:  # 无条件查找 000
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id)
            else:
                if maintain_cause:  # 通过维护原因和end_time查找 011
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).\
                        filter(repair_time__lte=end_time).filter(maintain_cause=maintain_cause)
                else:  # 通过end_time查找 010
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter\
                        (repair_time__lte=end_time)
        else:
            if not end_time:
                if maintain_cause:  # 通过维护原因和begin_time查找 101
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter\
                        (repair_time__gte=begin_time).filter(maintain_cause=maintain_cause)
                else:  # 通过begin_time查找 100
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter\
                        (repair_time__gte=begin_time)
            else:
                if maintain_cause:  # 通过维护原因和时间范围查找 111
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter\
                        (repair_time__gte=begin_time).filter(repair_time__lte=end_time).filter(maintain_cause=maintain_cause)
                else:  # 通过维护原因、begin_time查找 110
                    que = EquipmentMaintenance.objects.order_by('-repair_time').filter(equipment_id=equipment_id).filter\
                        (repair_time__gte=begin_time)
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
        serializer = ContactPeopleSerializer(instance=que, many=True)
        data_1 = serializer.data
        paginator = Paginator(data_1, size)  # 确定分页器对象
        data_2 = paginator.page(page)  # 当前页的数据
        data = {
            "count": num,
            "data": list(data_2)
        }
    return JsonResponse(data=data)

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

# 设备信息页面的查询和搜索
def equipmenttoenginename(request):
    # http://10.21.1.106:8000/app/equipment_to_engine_name/?engine_code=&equipment_code=&currentPage=&size=
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
        sql_1 = "SELECT * from (SELECT equipment.aid,equipment.engine_code,equipment.equipment_code,main_engine.engine_name,equipment.storehouse,equipment.storage_location,equipment.note " \
              "FROM equipment INNER JOIN main_engine ON equipment.engine_code=main_engine.engine_code) AS a "
        a = "engine_code = %s"
        b = "equipment_code = %s"
        if engine_code:
            if equipment_code:  # 11
                sql = sql_1 + " where "+a+" and "+b
                table = [engine_code,equipment_code]
            else:  # 10
                sql = sql_1 + " where " + a
                table = [engine_code]
        else:
            if equipment_code:  # 01
                sql = sql_1 + " where " + b
                table = [equipment_code]
            else:  # 00
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

        return JsonResponse(data=data)

# 设备表、传感器表、传感器类型表、传感器型号表四表级联
# 用于通过设备id给前端传输对应设备上的传感器编码、传感器型号、传感器类型
def equipmenttosensor3(request):
    # http://10.21.1.106:8000/app/equipment_to_sensor3/?equipment_id=&currentPage=&size=
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        page = request.GET.get("currentPage")  # 第几页
        size = request.GET.get("size")  # 每页多少
        if not page:
            page = 1
            size = 5
        if not size:
            page = 1
            size = 5
        a = 'equipment_id=%s'
        sql_1 = "SELECT * from (SELECT sensor.sensor_code,sensor_model.sensor_model,sensor_type.type_name,equipment_and_sensor.equipment_id " \
              "FROM equipment_and_sensor " \
              "INNER JOIN sensor " \
              "ON equipment_and_sensor.sensor_id=sensor.aid " \
              "INNER JOIN sensor_model " \
              "ON sensor.sensor_model_id=sensor_model.aid " \
              "INNER JOIN sensor_type " \
              "ON sensor_model.sensor_type_id=sensor_type.aid) AS a "
        if equipment_id:
            sql = sql_1+" where "+a
            table = [equipment_id]
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
        time = "T00:00:00.000000Z"
        # today = datetime.date.today()
        # oneday = datetime.timedelta(days=1)
        # tomorrow = today + oneday
        if not begin_time_first:
            if not end_time_first:
                # begin_time_first = str(today)
                # end_time_first = str(tomorrow)
                # 数据库只有10月10号的数据
                begin_time_first = '2020-10-10'
                end_time_first = '2020-10-11'
        begin_time = begin_time_first + time
        end_time = end_time_first + time
        print(begin_time, end_time)
        sql = "select * from b where deviceNum='%s' and time >= '%s' and time <= '%s'" % (deviceNum, begin_time, end_time)
        print(sql)
        data = query(sql)
        for i in data:
            result_list = i
            return JsonResponse(data=result_list, safe=False)

# 通过传感器型号aid给前端发送对应的传感器的全局id和编码
def sensormodeltocode(request):
    if request.method == "GET":
        sensor_model_id = request.GET.get('sensor_model_id')
        que = Sensor.objects.filter(sensor_model_id=sensor_model_id)
        serializer = SensorSerializer(instance=que, many=True)
        data = serializer.data
    return JsonResponse(data=data, safe=False)