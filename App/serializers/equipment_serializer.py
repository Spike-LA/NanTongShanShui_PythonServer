import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment  # 级联的模型#

        fields = '__all__'  # 显示所需要的字段#     #'__all__'显示全部的字段#

        read_only_fields = ('aid', 'engine_code',)

    def create(self, validated_data):  # 需要自定义创建内容时自行创建create方法#

        instance = Equipment()

        instance.aid = uuid.uuid4().hex
        instance.engine_code = validated_data.get('equipment_code')
        now = datetime.now()
        instance.equipment_code = now.strftime("%Y%m%d") + str(random.randint(100, 999))
        instance.storehouse = validated_data.get('storehouse')
        instance.storage_location = validated_data.get('storage_location')
        instance.note = validated_data.get('note')
        instance.equip_person = validated_data.get('equip_person')

        instance.save()

        return instance

    def update(self, instance, validated_data):

        instance.storehouse = validated_data.get('storehouse', instance.storehouse)
        instance.storage_location = validated_data.get('storage_location', instance.storage_location)
        instance.note = validated_data.get('note', instance.note)
        instance.equip_person = validated_data.get('equip_person', instance.equip_person)

        instance.save()

        return instance
