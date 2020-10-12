import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import EnterpriseAccount
from App.views_constant import activated


class EnterpriseAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnterpriseAccount
        fields = '__all__'
        read_only_fields = ('aid', 'account_id', 'add_time', 'mod_time')

    def create(self, validated_data):
        instance = EnterpriseAccount()
        instance.aid = uuid.uuid4().hex
        now = datetime.now()
        instance.account_id = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))
        instance.enterprise_number = validated_data.get('enterprise_number')
        instance.account_password = validated_data.get('account_password')
        instance.telephone_number = validated_data.get('telephone_number')
        instance.position = validated_data.get('position')
        instance.role = validated_data.get('role')
        instance.role_number = validated_data.get('role_number')
        instance.add_by = validated_data.get('add_by')
        instance.status = activated  # 设置新创建的账户为已激活
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.enterprise_number = validated_data.get('enterprise_number')
        instance.account_password = validated_data.get('account_password')
        instance.telephone_number = validated_data.get('telephone_number')
        instance.position = validated_data.get('position')
        instance.role = validated_data.get('role')
        instance.role_number = validated_data.get('role_number')
        instance.mod_by = validated_data.get('mod_by')
        instance.status = validated_data.get('status')
        instance.save()
        return instance
