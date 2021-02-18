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
        read_only_fields = ('aid',)

    def create(self, validated_data):

        instance = EquipmentAllocation()

        instance.aid = uuid.uuid4().hex
        instance.engine_id = validated_data.get('engine_id')
        instance.equipment_id = validated_data.get('equipment_id')
        instance.applicant = validated_data.get('applicant')
        obj_equipment = Equipment.objects.filter(aid=instance.equipment_id).first()  # 找到调拨的设备对象
        obj_equipment.status = on_line  # 设置调拨的设备状态为在线
        obj_equipment.save()
        instance.applicant_tel = validated_data.get('applicant_tel')
        instance.client_id = validated_data.get('client_id')
        instance.transfer_unit = validated_data.get('transfer_unit')
        instance.transfer_unit_ads = validated_data.get('transfer_unit_ads')
        instance.transfer_unit_tel = validated_data.get('transfer_unit_tel')
        instance.allocation_reason = validated_data.get('allocation_reason')
        instance.remark = validated_data.get('remark')
        instance.save()

        return instance
