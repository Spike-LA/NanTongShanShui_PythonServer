import uuid

from rest_framework import serializers

from App.models import SensorModel
from App.views_constant import is_using


class SensorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorModel
        fields = '__all__'
        read_only_fields = ('aid', 'create_time')

    def create(self, validated_data):

        instance = SensorModel()

        instance.aid = uuid.uuid4().hex
        instance.sensor_type_id = validated_data.get('sensor_type_id')
        instance.sensor_model = validated_data.get('sensor_model')
        instance.sensor_threshold = validated_data.get('sensor_threshold')
        instance.notice_content = validated_data.get('notice_content')
        instance.states = is_using
        instance.save()

        return instance

