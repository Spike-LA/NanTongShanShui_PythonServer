import datetime
import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from influxdb_metrics.utils import query

from App.functions.condition_search import maintenances, maintenance
from App.models import EquipmentMaintenance, ContactPeople, SensorType, SensorModel, Sensor, Equipment, \
    EquipmentAndSensor, MainEngine, User, Role, PowerRelation, Power
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
        sql_1 = "SELECT * from (SELECT equipment.equip_person,equipment.aid,equipment.engine_code,equipment.equipment_code,main_engine.engine_name,equipment.storehouse,equipment.storage_location,equipment.note " \
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
# 用于通过设备id给前端传输对应设备上的传感器编码、传感器型号、传感器类型、默认阈值
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
        sql_1 = "SELECT * from (SELECT sensor.sensor_code,sensor_model.sensor_model,sensor_model.sensor_threshold,sensor_type.type_name,equipment_and_sensor.equipment_id " \
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
                # 数据库只有10月10号的数据,之后完成的时候是用上面两行代码
                begin_time_first = '2020-10-10'
                end_time_first = '2020-10-11'
        begin_time = begin_time_first + time
        end_time = end_time_first + time
        print(begin_time, end_time)
        sql = "select * from b where deviceNum='%s' and time >= '%s' and time <= '%s'" % (deviceNum, begin_time, end_time)
        print(sql)
        data = query(sql)
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
        query_2 = EquipmentAndSensor.objects.filter(equipment_id=query_1.aid)
        table_1 = []
        for obj_1 in query_2:
            table_1.append(obj_1.sensor_id)   # 获取该设备上的各个传感器id
        print(table_1)

        sql = "SELECT * FROM (SELECT sensor.sensor_code,sensor.aid,sensor_type.type_name,sensor_model.sensor_model,sensor.theoretical_value " \
              "FROM sensor " \
              "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
              "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid ) " \
              "AS a where aid=%s"

        data = []
        for obj_2 in table_1:
            results = maintenances(sql, obj_2)
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
            begin_time = begin_time_first+time_second_first
        if end_time_first:
            end_time = end_time_first+time_second_end
        a = 'notice_time >= %s'
        b = 'notice_time <= %s'
        c = 'type_name = %s'

        sql_first = "SELECT * FROM (SELECT equipment_id,measurement,water_quality_notice.sensor_id,type_name,sensor.notice_content,water_quality_notice.notice_time " \
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
                    sql = sql_first+' and '+a +' and '+b+' and '+c
                    table = [equipment_id, begin_time, end_time, type_name]
                else:  # 110
                    sql = sql_first + ' and ' + a + ' and ' + b
                    table = [equipment_id, begin_time, end_time]
            else:
                if type_name: # 101
                    sql = sql_first + ' and ' + a + ' and ' + c
                    table = [equipment_id, begin_time, type_name]
                else:  # 100
                    sql = sql_first + ' and ' + a
                    table = [equipment_id, begin_time]
        else:
            if end_time_first:
                if type_name: # 011
                    sql = sql_first +' and ' + b + ' and ' + c
                    table = [equipment_id, end_time, type_name]
                else:  # 010
                    sql = sql_first +' and ' + b
                    table = [equipment_id, end_time]
            else:
                if type_name:  # 001
                    sql = sql_first +' and '+c
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
            table.append(dic)
    return JsonResponse(data=table, safe=False)

# 实时监控界面的设备详情弹窗
def equipmentdetail(request):
    # http://10.21.1.106:8000/app/equipment_detail/?equipment_id=
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')

        if equipment_id:
            sql = "SELECT * FROM (SELECT equipment_and_sensor.equipment_id,main_engine.engine_code,main_engine.engine_name,contact_people.contact_person,contact_people.contact_tel,sensor_type.type_name,sensor_model.sensor_model " \
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
    # http://127.0.0.1:8000/app/login_in/?account=&password=
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        obj = User.objects.filter(account=account).first()
        if obj:  # 账户存在
            if obj.password == password:  # 账户存在且密码正确

                data = {
                    'user_id': obj.aid,
                    'role_id': obj.role_id,
                    'msg': '登陆成功',
                }
            else:  # 账户存在但密码不正确
                data = {
                    'msg': '密码不正确',
                }
        else:  # 账户不存在
            data = {
                'msg': '账户名不存在',
            }

    return JsonResponse(data=data, safe=False)

# 前端验证登陆状态时，返回给前端这个账号的所有权限别名
def verify(request):
    # http://127.0.0.1:8000/app/verify/?user_id=&role_id=
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        role_id = request.GET.get('role_id')
        query_role_power = PowerRelation.objects.filter(aim_id=role_id)
        query_user_power = PowerRelation.objects.filter(aim_id=user_id)
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

        sql_1 = "SELECT * FROM (SELECT sensor_calibration.calibrate_time,sensor_calibration.actual_value,sensor_calibration.calibrate_compensation,sensor.theoretical_value,sensor_type.type_name,equipment.equipment_code " \
                "FROM sensor_calibration " \
                "INNER JOIN sensor ON sensor_calibration.sensor_id=sensor.aid " \
                "INNER JOIN sensor_model ON sensor.sensor_model_id=sensor_model.aid " \
                "INNER JOIN sensor_type ON sensor_model.sensor_type_id=sensor_type.aid " \
                "INNER JOIN equipment_and_sensor ON sensor.aid=equipment_and_sensor.sensor_id " \
                "INNER JOIN equipment ON equipment_and_sensor.equipment_id=equipment.aid) AS a WHERE equipment_code=%s"

        if begin_time_first:
            if end_time_first:
                if type_name:  # 111
                    sql = sql_1+' and '+a+' and '+b+' and '+c
                    table = [equipment_code, begin_time, end_time, type_name]
                else:  # 110
                    sql = sql_1 + ' and ' + a + ' and ' + b
                    table = [equipment_code, begin_time, end_time]
            else:
                if type_name: # 101
                    sql = sql_1 + ' and ' + a + ' and ' + c
                    table = [equipment_code, begin_time, type_name]
                else:  # 100
                    sql = sql_1 + ' and ' + a
                    table = [equipment_code, begin_time]

        else:
            if end_time_first:
                if type_name:  # 011
                    sql = sql_1+' and '+b+' and '+c
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
    # http://10.21.1.106:8000/app/water_notice_retrieve/?currentPage=&size&&equipment_id=&begin_time=&end_time=&type_name=&deal_status=
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
        sql = "SELECT * FROM (SELECT water_quality_notice.aid,water_quality_notice.deal_status,water_quality_notice.notice_time,water_quality_notice.deal_time,sensor.notice_content,sensor_type.type_name, equipment_and_sensor.equipment_id " \
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
                sql = sql+' and '+i
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
