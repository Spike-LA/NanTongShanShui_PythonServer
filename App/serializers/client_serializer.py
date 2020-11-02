from datetime import datetime
import random
import uuid

from rest_framework import serializers

from App.models import Client
from App.views_constant import on_using


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('aid', 'client_code',)

    def create(self, validated_data):

        instance = Client()

        instance.aid = uuid.uuid4().hex
        now = datetime.now()
        instance.client_code = now.strftime("%Y%m%d") + str(random.randint(100000, 999999))
        instance.client_unit = validated_data.get('client_unit')
        instance.client_address = validated_data.get('client_address')
        instance.client_zip_code = validated_data.get('client_zip_code')
        instance.client_industry = validated_data.get('client_industry')
        instance.unit_phone = validated_data.get('unit_phone')
        instance.unit_fax = validated_data.get('unit_fax')
        instance.note = validated_data.get('note')
        instance.region = validated_data.get('region')  # 地区
        instance.status = on_using

        instance.save()

        return instance
