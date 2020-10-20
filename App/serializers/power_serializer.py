import uuid

from rest_framework import serializers

from App.models import Power


class PowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Power
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):
        instance = Power()
        instance.aid = uuid.uuid4().hex
        instance.power = validated_data.get('power')
        instance.power_num = validated_data.get('power_num')

        instance.save()
        return instance
