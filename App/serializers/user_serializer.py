import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import User, PowerRelation, Power
from App.views_constant import not_Delete


class UserSerializer(serializers.ModelSerializer):
    power_id_str = serializers.CharField(write_only=True, allow_null=True)
    alter_power = serializers.CharField(write_only=True, allow_null=True)

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
        instance.mod_by = validated_data.get('mod_by', instance.mod_by)
        instance.save()

        alter_power = validated_data.get('alter_power')
        if alter_power == 'yes':
            # 除角色以外的权限设定
            que_power_relation = PowerRelation.objects.filter(aim_id=instance.aid)
            old_power_id_list = []  # 找出该用户原有的权限（角色之外）id，生成一个列表
            for obj_power_relation in que_power_relation:
                old_power_id_list.append(obj_power_relation.power_id)

            for old_power_id in old_power_id_list:  # 删除全部旧权限
                old_user_power_relation_obj = PowerRelation.objects.filter(aim_id=instance.aid).filter(power_id=old_power_id).first()
                old_user_power_relation_obj.delete()

            # power_id_str的格式为'id1,id2,id3'
            power_id_str = validated_data.get('power_id_str')
            if power_id_str:
                new_power_id_list = power_id_str.split(',')  # 利用split方法，以,为间隔符进行分割，形成一个由新权限id组成的列表
                for new_power_id in new_power_id_list:  # 增加全部新权限
                    instance_power_relation = PowerRelation()
                    instance_power_relation.aid = uuid.uuid4().hex
                    instance_power_relation.power_id = new_power_id
                    instance_power_relation.aim_id = instance.aid
                    instance_power_relation.save()

        return instance
