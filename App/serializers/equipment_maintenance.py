import uuid

from rest_framework import serializers

from App.models import EquipmentMaintenance
from App.views_constant import not_stop_maintenance


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentMaintenance
        fields = '__all__'
        read_only_fields = ('aid', 'equipment_id', 'repair_time', 'maintain_time', 'maintain_status')

    def create(self, validated_data):
        instance = EquipmentMaintenance()
        instance.aid = uuid.uuid4().hex
        instance.equipment_id = validated_data.get('equipment_id')
        instance.repair_time = validated_data.get('repair_time')
        instance.maintain_time = validated_data.get('maintain_time')
        instance.maintain_cause = validated_data.get('maintain_cause')
        instance.fault_description = validated_data.get('fault_description')
        instance.maintain_result = validated_data.get('maintain_result')
        instance.responsible_person = validated_data.get('responsible_person')
        instance.status = not_stop_maintenance
        instance.save()

        return instance