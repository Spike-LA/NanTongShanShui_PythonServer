import uuid

from rest_framework import serializers

from App.models import PumpPermission


class PumpPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PumpPermission
        fields = '__all__'
        read_only_fields = ('permission_id', 'create_time', 'mod_time')

    def create(self, validated_data):
        instance = PumpPermission()
        instance.permission_id = uuid.uuid4().hex
        instance.user_id = validated_data.get('user_id')
        instance.pump_id = validated_data.get('pump_id')
        instance.create_by = validated_data.get('create_by')
        instance.save()
        return instance

