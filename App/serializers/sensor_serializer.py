import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Sensor, SensorCalibration
from App.views_constant import is_using, un_using, sensor_scrap


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ('aid', 'sensor_code')

    def create(self, validated_data):

        instance = Sensor()
        instance.aid = uuid.uuid4().hex
        instance.sensor_model_id = validated_data.get('sensor_model_id')
        instance.sensor_threshold = validated_data.get('sensor_threshold')
        instance.notice_content = validated_data.get('notice_content')
        instance.default_compensation = validated_data.get('default_compensation')
        instance.create_time = validated_data.get('create_time')
        instance.alert_time = validated_data.get('alert_time')
        instance.sensor_threshold = validated_data.get('theoretical_value')
        instance.note = validated_data.get('note')
        now = datetime.now()  # 时间模块  现在时间
        instance.sensor_code = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))  # 导入事件模块和随机模块生成编号
        instance.status = is_using  # 设置传感器状态为可以使用

        instance.save()

        return instance

    def update(self, instance, validated_data):

        instance.sensor_threshold = validated_data.get('sensor_threshold', instance.sensor_threshold)
        instance.notice_content = validated_data.get('notice_content', instance.notice_content)
        instance.default_compensation = validated_data.get('default_compensation', instance.default_compensation)
        instance.theoretical_value = validated_data.get('theoretical_value', instance.theoretical_value)
        instance.note = validated_data.get('note', instance.note)
        if validated_data.get('status') == '报废':
            instance.status = sensor_scrap
        elif validated_data.get('status') == '未使用':
            instance.status = un_using
        else:
            instance.status = is_using
        instance.save()
        return instance
