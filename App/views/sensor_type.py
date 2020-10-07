import pymysql
from rest_framework import viewsets

from App.models import SensorType
from App.serializers.sensor_type_serializer import SensorTypeSerializer


class SensorTypeViewSet(viewsets.ModelViewSet):

    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer

    # @list_route(url_path='typemodel')
    # def type_model(self, request, *args, **kwargs):
    #     conn = pymysql.connect(host="localhost", user="root", password="123456", database='ntss')
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT type_name,sensor_model FROM sensor_type LEFT JOIN sensor_model ON "
    #                    "sensor_type.aid=sensor_model.sensor_type_id")
    #     results = cursor.fetchall()
    #     for result in results:
    #         print(result)
