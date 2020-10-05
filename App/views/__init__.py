import pymysql
from django.http import HttpResponse, JsonResponse

from App.views_constant import a


def type_model(request):

    if request.method == "GET":
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
        cursor = conn.cursor()
        cursor.execute("SELECT type_name,sensor_model,status FROM sensor_type LEFT JOIN sensor_model ON "
                       "sensor_type.aid=sensor_model.sensor_type_id")
        results = cursor.fetchall()

        data_list_json = []

        for result in results:
            for data in result:
                data_list_json.append(data)

        d = zip(a, data_list_json)

        # print(type(dict(d)))

        data = dict(d)

        return JsonResponse(data=data)
