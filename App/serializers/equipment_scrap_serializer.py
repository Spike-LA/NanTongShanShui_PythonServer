import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import EquipmentScrap



class EquipmentScrapSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentScrap
        fields = '__all__'
        read_only_fields = ('aid', 'table_id', 'applicant_time')

    def create(self, validated_data):
        instance = EquipmentScrap()
        instance.aid = uuid.uuid4().hex
        now = datetime.now()  # 时间模块  现在时间
        instance.table_id = now.strftime("%Y%m%d") + str(random.randint(1000, 9999))  # 导入事件模块和随机模块生成编号
        instance.host_number = validated_data.get('host_number')
        instance.equipment_id = validated_data.get('equipment_id')
        instance.equipment_number = validated_data.get('equipment_number')
        instance.equipment_remark = validated_data.get('equipment_remark')
        instance.applicant = validated_data.get('applicant')
        instance.client_id = validated_data.get('client_id')
        instance.allocation_reason = validated_data.get('allocation_reason')
        instance.transport_unit = validated_data.get('transport_unit')
        instance.agent = validated_data.get('agent')
        instance.agent_tel = validated_data.get('agent_tel')
        instance.opinion = validated_data.get('opinion')
        instance.sign = validated_data.get('sign')
        instance.approval_time = validated_data.get('approval_time')
        instance.applicant_time = validated_data.get('applicant_time')
        instance.remark = validated_data.get('remark')
        instance.save()

        return instance
