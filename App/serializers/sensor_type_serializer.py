import uuid

from rest_framework import serializers

from App.models import SensorType


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'
        read_only_fields = ('aid','create_time')

    def create(self, validated_data):

        instance = SensorType()

        instance.aid = uuid.uuid4().hex
        instance.type_name = validated_data.get('type_name')


        instance.save()

        return instance
