import uuid

from rest_framework import serializers

from App.models import User, PowerRelation, Power
from App.views_constant import on_the_job, leave_the_job


class UserSerializer(serializers.ModelSerializer):
    power_num_str = serializers.CharField(write_only=True, allow_null=True)

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
        if validated_data.get('status') == '在职':
            instance.status = on_the_job
        else:
            instance.status = leave_the_job
        instance.role_id = validated_data.get('role_id')
        instance.add_by = validated_data.get('add_by')
        instance.mod_by = validated_data.get('mod_by')

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.telephone_num = validated_data.get('telephone_num', instance.telephone_num)
        if validated_data.get('status') == '离职':
            instance.status = leave_the_job
        instance.role_id = validated_data.get('role_id', instance.role_id)
        instance.mod_by = validated_data.get('mod_by', instance.mod_by)
        instance.save()

        # 除角色以外的权限设定
        # power_num的格式为'sensor_calibration_retrieve,client_message_edit,equipment_maintenance_reset'
        power_num_str = validated_data.get('power_num_str')
        print(power_num_str)
        power_num_list = power_num_str.split(',')  # 利用split方法，以,为间隔符进行分割，形成一个由权限代号组成的列表
        print(power_num_list)
        for power_num in power_num_list:
            print(power_num)
            obj_power = Power.objects.filter(power_num=power_num).first()
            instance_power_relation = PowerRelation()
            instance_power_relation.aid = uuid.uuid4().hex
            instance_power_relation.power_id = obj_power.aid
            instance_power_relation.aim_id = instance.aid
            instance_power_relation.save()
        return instance

