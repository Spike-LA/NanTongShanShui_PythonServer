from datetime import datetime
import random
import uuid

from rest_framework import serializers

from App.models import EquipmentScrap, Equipment, Sensor
from App.views_constant import scraped, un_using


class EquipmentScrapSerializer(serializers.ModelSerializer):

    equipment_sensor = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = EquipmentScrap
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):

        instance = EquipmentScrap()

        instance.aid = uuid.uuid4().hex
        instance.engine_id = validated_data.get('engine_id')
        instance.equipment_id = validated_data.get('equipment_id')
        instance.applicant = validated_data.get('applicant')
        obj_equipment = Equipment.objects.filter(aid=instance.equipment_id).first()  # 找到调拨的设备对象
        obj_equipment.status = scraped  # 设置调拨的设备状态为报废
        obj_equipment.save()
        instance.applicant_tel = validated_data.get('applicant_tel')
        instance.scrapping_reasons = validated_data.get('scrapping_reasons')
        instance.remark = validated_data.get('remark')

        instance.save()

        ar = validated_data.get('equipment_sensor')
        if ar != 'false':
            arr = ar.split(',')

            for obj in arr:
                sensor_obj = Sensor.objects.filter(aid=obj).first()
                sensor_obj.status = un_using
                sensor_obj.save()

        return instance

