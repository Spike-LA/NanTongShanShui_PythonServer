import uuid

from rest_framework import serializers

from App.models import AutoOperationInfo
from App.views_constant import time_operation, opration_not_finish


class AutoOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoOperationInfo
        fields = '__all__'
        read_only_fields = ('uuid', 'create_time')

    def create(self, validated_data):
        instance = AutoOperationInfo()
        instance.uuid = uuid.uuid4().hex
        instance.pump_code = validated_data.get('pump_code')
        instance.operation_time = validated_data.get('operation_time')
        instance.operation_type = validated_data.get('operation_type')
        instance.begin_time = validated_data.get('begin_time')
        if instance.operation_type == time_operation:
            instance.end_time = ''
            instance.period = ''
        else:
            instance.end_time = validated_data.get('end_time')
            instance.period = validated_data.get('period')
        instance.status = opration_not_finish
        instance.create_by = validated_data.get('create_by')
        instance.save()
        return instance
