import pymysql
from django.http import HttpResponse


def type_model(request):

    if request.method == "GET":
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
        cursor = conn.cursor()
        cursor.execute("SELECT type_name,sensor_model,status FROM sensor_type LEFT JOIN sensor_model ON "
                       "sensor_type.aid=sensor_model.sensor_type_id")
        results = cursor.fetchall()
        print(type(results))
        for result in results:
            print(result)
        return HttpResponse("成功")
