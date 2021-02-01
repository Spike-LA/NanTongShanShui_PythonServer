from rest_framework import serializers

from App.models import EquipmentOperationLog


class EquipmentOperationLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentOperationLog

        fields = '__all__'