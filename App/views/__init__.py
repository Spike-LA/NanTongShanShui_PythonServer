import pymysql
from django.http import HttpResponse, JsonResponse

from App.views_constant import a


def type_model(request):  # 设备类型与设备型号进行连表搜索，显示类型名、型号名、状态、备注。

    if request.method == "GET":
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
        cursor = conn.cursor()
        cursor.execute("SELECT type_name,sensor_model,status,remark FROM sensor_type LEFT JOIN sensor_model ON "
                       "sensor_type.aid=sensor_model.sensor_type_id")
        results = cursor.fetchall()

        data_list_json = []

        for result in results:

            d = zip(a, result)

            data = dict(d)

            data_list_json.append(data)

        data = {
            "data": data_list_json
        }

        return JsonResponse(data=data)  # 对象
