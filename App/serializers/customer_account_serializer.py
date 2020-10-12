import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import CustomerAccount
from App.views_constant import activated


class CustomerAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerAccount
        fields = "__all__"
        read_only_fields = ('aid', 'account_id', 'add_time', 'mod_time')

    def create(self, validated_data):
        instance = CustomerAccount()
        instance.aid = uuid.uuid4().hex
        now = datetime.now()
        instance.account_id = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))
        instance.account_number = validated_data.get('account_number')
        instance.account_password = validated_data.get('account_password')
        instance.customer_id = validated_data.get('customer_id')
        instance.role = validated_data.get('role')
        instance.role_number = validated_data.get('role_number')
        instance.add_by = validated_data.get('add_by')
        instance.status = activated  # 设置新创建的账户为已激活
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.account_number = validated_data.get('account_number')
        instance.account_password = validated_data.get('account_password')
        instance.role = validated_data.get('role')
        instance.role_number = validated_data.get('role_number')
        instance.mod_by = validated_data.get('mod_by')
        instance.status = validated_data.get('status')
        instance.save()
        return instance

