from datetime import datetime
import random
import uuid

from rest_framework import serializers

from App.models import EquipmentScrap, Equipment
from App.views_constant import scraped


class EquipmentScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentScrap
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):

        instance = EquipmentScrap()

        instance.aid = uuid.uuid4().hex
        now = datetime.now()
        instance.table_id = now.strftime("%Y%m%d") + str(random.randint(10000, 99999))
        instance.host_number = validated_data.get('host_number')
        instance.host_name = validated_data.get('host_name')
        instance.equipment_id = validated_data.get('equipment_id')
        instance1 = Equipment.objects.filter(aid=instance.equipment_id).first()
        instance1.status = scraped
        instance1.save()
        instance.applicant = validated_data.get('applicant')
        instance.applicant_time = validated_data.get('applicant_time')
        instance.applicant_tel = validated_data.get('applicant_tel')
        instance.applicant_department = validated_data.get('applicant_department')
        instance.scrapping_reasons = validated_data.get('scrapping_reasons')
        instance.opinion = validated_data.get('opinion')
        instance.sign = validated_data.get('sign')
        instance.approval_time = validated_data.get('approval_time')
        instance.remark = validated_data.get('remark')

        instance.save()

        return instance
