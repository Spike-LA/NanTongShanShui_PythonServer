import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ('aid', 'sensor_code',)

    def create(self, validated_data):

        instance = Sensor()

        instance.aid = uuid.uuid4().hex
        instance.sensor_model_id = validated_data.get('sensor_model_id')
        instance.note = validated_data.get('note')
        now = datetime.now()  # 时间模块  现在时间
        instance.sensor_code = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))  # 导入事件模块和随机模块生成编号

        instance.save()

        return instance
