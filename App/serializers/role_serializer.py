import uuid

from rest_framework import serializers

from App.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):

        instance = Role()

        instance.aid = uuid.uuid4().hex
        instance.role_name = validated_data.get("role_name")
        instance.save()

        return instance
