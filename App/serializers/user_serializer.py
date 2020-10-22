import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import User, PowerRelation, Power
from App.views_constant import  not_Delete


class UserSerializer(serializers.ModelSerializer):
    power_id_str = serializers.CharField(write_only=False, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('aid', 'add_time', 'mod_time', 'account', 'status')

    def create(self, validated_data):
        instance = User()

        instance.aid = uuid.uuid4().hex
        instance.name = validated_data.get('name')
        que = User.objects.all()
        table = []
        for obj in que:
            table.append(obj.aid)
        now = datetime.now()
        instance.account = now.strftime("%Y%m%d")+str(len(table))
        instance.password = validated_data.get('password')
        instance.telephone_num = validated_data.get('telephone_num')
        instance.status = not_Delete
        instance.role_id = validated_data.get('role_id')
        instance.add_by = validated_data.get('add_by')

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.telephone_num = validated_data.get('telephone_num', instance.telephone_num)
        instance.role_id = validated_data.get('role_id', instance.role_id)
        print(instance.role_id)
        instance.mod_by = validated_data.get('mod_by', instance.mod_by)
        instance.save()


