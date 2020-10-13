import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Sensor
from App.views_constant import on_using, stop_using


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ('aid', 'sensor_code', 'sensor_model_id',)

    def create(self, validated_data):

        instance = Sensor()

        instance.aid = uuid.uuid4().hex
        instance.sensor_model_id = validated_data.get('sensor_model_id')
        instance.sensor_threshold = validated_data.get('sensor_threshold')
        instance.notice_content = validated_data.get('notice_content')
        instance.status = validated_data.get('status')
        instance.note = validated_data.get('note')
        now = datetime.now()  # 时间模块  现在时间
        instance.sensor_code = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))  # 导入事件模块和随机模块生成编号

        instance.save()

        return instance

    def update(self, instance, validated_data):

        instance.sensor_threshold = validated_data.get('sensor_threshold', instance.sensor_threshold)
        instance.notice_content = validated_data.get('notice_content', instance.notice_content)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.alert_time = validated_data.get('alert_time', instance.alert_time)
        instance.offset = validated_data.get('offset', instance.offset)
        instance.note = validated_data.get('note', instance.note)
        status = validated_data.get('status')
        if status == '可以使用':
            instance.status = on_using
        else:
            instance.status = stop_using
        instance.save()
        return instance
