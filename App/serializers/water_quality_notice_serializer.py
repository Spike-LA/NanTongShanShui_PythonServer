import uuid

from rest_framework import serializers

from App.models import WaterQualityNotice
from App.views_constant import is_dealt, wait_deal


class WaterQualityNoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterQualityNotice
        fields = '__all__'
        read_only_fields = ('aid', 'notice_time',)

    def update(self, instance, validated_data):
        instance.deal_status = is_dealt
        instance.save()
        return instance

    def create(self, validated_data):
        instance = WaterQualityNotice()
        instance.aid = uuid.uuid4().hex
        instance.sensor_id=validated_data.get('sensor_id')
        instance.notice_time=validated_data.get('notice_time')
        instance.measurement=validated_data.get('measurement')
        instance.deal_status= wait_deal
        instance.save()
        return instance


