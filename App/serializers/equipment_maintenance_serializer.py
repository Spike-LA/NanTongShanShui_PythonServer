import uuid

from rest_framework import serializers

from App.models import EquipmentMaintenance
from App.views_constant import wait_maintenance, not_stop_maintenance, stop_maintenance, finish_maintenance


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentMaintenance
        fields = '__all__'
        read_only_fields = ('aid','maintain_result', 'maintain_status')

    def create(self, validated_data):
        instance = EquipmentMaintenance()
        instance.aid = uuid.uuid4().hex
        instance.equipment_id = validated_data.get('equipment_id')
        instance.fault_description = validated_data.get('fault_description')
        instance.maintain_result = wait_maintenance  # 设置维护结果为等待维护
        instance.maintain_status = not_stop_maintenance  # 设置维护状态为维护未结束
        instance.responsible_person = validated_data.get('responsible_person')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.maintain_time = validated_data.get('maintain_time', instance.maintain_time)
        instance.maintain_cause = validated_data.get('maintain_cause', instance.maintain_cause)
        instance.fault_description = validated_data.get('fault_description', instance.maintain_cause)
        instance.maintain_result = finish_maintenance  # 设置维护结果为维护完成
        instance.maintain_status = stop_maintenance  # 设置维护状态为维护结束
        instance.responsible_person = validated_data.get('responsible_person', instance.responsible_person)
        instance.save()
        return instance
