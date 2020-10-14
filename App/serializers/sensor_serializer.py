import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Sensor
from App.views_constant import is_using, not_using


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ('aid', 'sensor_code',)

    def create(self, validated_data):

        instance = Sensor()

        instance.aid = uuid.uuid4().hex
        instance.sensor_model_id = validated_data.get('sensor_model_id')
        instance.sensor_threshold = validated_data.get('sensor_threshold')
        instance.notice_content = validated_data.get('notice_content')
        instance.default_compensation = validated_data.get('default_compensation')
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
        instance.note = validated_data.get('note', instance.note)
        if validated_data.get('status') == '停止使用':
            instance.status = not_using
        else:
            pass
        instance.save()
        return instance
