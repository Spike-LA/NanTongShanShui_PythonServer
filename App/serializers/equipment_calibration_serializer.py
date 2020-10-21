import uuid

from rest_framework import serializers

from App.models import SensorCalibration


class EquipmentCalibrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorCalibration
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):
        instance = SensorCalibration()
        instance.aid = uuid.uuid4().hex
        instance.sensor_id = validated_data.get('sensor_id')
        instance.actual_value = validated_data.get('actual_value')
        instance.calibrate_compensation = validated_data.get('calibrate_compensation')
        instance.save()

        return instance

