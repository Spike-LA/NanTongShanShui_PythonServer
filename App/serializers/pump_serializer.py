import uuid

from rest_framework import serializers

from App.models import Pump
from App.views_constant import not_equipped


class PumpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pump
        fields = '__all__'
        read_only_fields = ('pump_id', 'create_time', 'mod_time')

    def create(self, validated_data):
        instance = Pump()
        instance.pump_id = uuid.uuid4().hex
        instance.pump_code = validated_data.get('pump_code')
        instance.pump_name = validated_data.get('pump_name')
        instance.fluid_flow = validated_data.get('fluid_flow')
        instance.create_by = validated_data.get('create_by')
        instance.note = validated_data.get('note')
        instance.status = not_equipped
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.fluid_flow = validated_data.get('fluid_flow', instance.fluid_flow)
        instance.mod_by = validated_data.get('mod_by', instance.mod_by)
        instance.save()
        return instance