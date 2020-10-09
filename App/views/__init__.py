import pymysql
from django.http import JsonResponse

from App.functions import maintenance
from App.views_constant import a

def type_model(request):  # 设备类型与设备型号进行连表搜索，显示类型名、型号名、状态、备注。

    if request.method == "GET":
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
        cursor = conn.cursor()
        cursor.execute("SELECT type_name,sensor_model,status,remark FROM sensor_type LEFT JOIN sensor_model ON "
                       "sensor_type.aid=sensor_model.sensor_type_id")
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        data_list_json = []

        for result in results:
            d = zip(a, result)

            data = dict(d)

            data_list_json.append(data)

        data = {
            "data": data_list_json
        }

        return JsonResponse(data=data)  # 对象


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






