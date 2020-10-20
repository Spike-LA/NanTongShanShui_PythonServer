import uuid

from rest_framework import serializers

from App.models import PowerRole


class PowerRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerRole
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):
        instance = PowerRole()
        instance.aid = uuid.uuid4().hex
        instance.power_id = validated_data.get('power_id')
        instance.role_id = validated_data.get('role_id')

        instance.save()
        return instance
