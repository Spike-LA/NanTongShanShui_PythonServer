from rest_framework import serializers

from App.models import WaterQualityNotice
from App.views_constant import is_dealt


class WaterQualityNoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterQualityNotice
        fields = '__all__'
        read_only_fields = ('aid', 'notice_time',)

    def update(self, instance, validated_data):
        instance.deal_status = is_dealt
        instance.save()
        return instance


