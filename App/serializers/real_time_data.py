from rest_framework import serializers

from App.models import RealTimeData


class RealTimeDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = RealTimeData
        fields = '__all__'