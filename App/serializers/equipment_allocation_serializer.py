import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import EquipmentAllocation, Equipment
from App.views_constant import on_line


class EquipmentAllocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentAllocation
        fields = '__all__'
        read_only_fields = ('aid', 'table_id')

    def create(self, validated_data):

        instance = EquipmentAllocation()

        instance.aid = uuid.uuid4().hex
        instance.host_number = validated_data.get('host_number')
        instance.host_name = validated_data.get('host_name')
        instance.equipment_id = validated_data.get('equipment_id')
        obj_equipment = Equipment.objects.filter(aid=instance.equipment_id).first()  # 找到调拨的设备对象
        obj_equipment.status = on_line  # 设置调拨的设备状态为在线
        obj_equipment.save()
        instance.equipment_remark = validated_data.get('equipment_remark')
        instance.applicant_tel = validated_data.get('applicant_tel')
        instance.transfer_unit = validated_data.get('transfer_unit')
        instance.transfer_unit_ads = validated_data.get('transfer_unit_ads')
        instance.transfer_unit_tel = validated_data.get('transfer_unit_tel')
        instance.applicant = validated_data.get('applicant')
        instance.applicant_time = validated_data.get('applicant_time')
        instance.client_id = validated_data.get('client_id')
        instance.allocation_reason = validated_data.get('allocation_reason')
        instance.transport_unit = validated_data.get('transport_unit')
        instance.agent = validated_data.get('agent')
        instance.agent_tel = validated_data.get('agent_tel')
        instance.opinion = validated_data.get('opinion')
        instance.sign = validated_data.get('sign')
        instance.approval_time = validated_data.get('approval_time')
        instance.remark = validated_data.get('remark')
        instance.save()

        return instance
