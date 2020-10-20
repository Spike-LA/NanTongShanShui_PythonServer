import uuid

from rest_framework import serializers

from App.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('aid', 'add_time', 'mod_time', )

    def create(self, validated_data):
        instance = User()

        instance.aid = uuid.uuid4().hex
        instance.name = validated_data.get('name')
        instance.account = validated_data.get('account')
        instance.password = validated_data.get('password')
        instance.telephone_num = validated_data.get('telephone_num')
        instance.status = validated_data.get('status')
        instance.role_id = validated_data.get('role_id')
        instance.add_by = validated_data.get('add_by')
        instance.mod_by = validated_data.get('mod_by')

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.telephone_num = validated_data.get('telephone_num', instance.telephone_num)
        instance.status = validated_data.get('status', instance.status)
        instance.role_id = validated_data.get('role_id', instance.role_id)
        instance.mod_by = validated_data.get('mod_by', instance.mod_by)
        instance.save()
        return instance

