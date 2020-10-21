import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Equipment, Sensor, EquipmentAndSensor
from App.views_constant import working, not_working


class EquipmentSerializer(serializers.ModelSerializer):
    # 写了write_only之后这个字段就不会用于存储了
    equipment_sensor = serializers.CharField(write_only=True)

    class Meta:
        model = Equipment  # 级联的模型#

        fields = '__all__'  # 显示所需要的字段#     #'__all__'显示全部的字段#

        read_only_fields = ('aid','create_time', 'alert_time')

    def create(self, validated_data):  # 需要自定义创建内容时自行创建create方法#
        print(validated_data.get('equipment_sensor'))

        instance = Equipment()

        instance.aid = uuid.uuid4().hex
        instance.engine_code = validated_data.get('engine_code')
        instance.equipment_code = validated_data.get('equipment_code')
        instance.storehouse = validated_data.get('storehouse')
        instance.storage_location = validated_data.get('storage_location')
        instance.note = validated_data.get('note')
        instance.equip_person = validated_data.get('equip_person')
        instance.status = validated_data.get('status')


        instance.save()

        # 设备上的每个传感器id,前端传输格式为"12344,54321"
        ar = validated_data.get('equipment_sensor')
        print(ar)
        # split方法对字符串进行分割，然后形成列表
        arr = ar.split(',')
        print(arr)

        for obj in arr:
            equipment_instance = EquipmentAndSensor()
            equipment_instance.aid = uuid.uuid4().hex
            equipment_instance.equipment_id = instance.aid
            equipment_instance.sensor_id = obj
            equipment_instance.status = working
            equipment_instance.save()

        return instance

    def update(self, instance, validated_data):
        print(instance)
        print(instance.engine_code)
        equipment_id = instance.aid
        print(instance.aid)
        instance.engine_code = validated_data.get('engine_code', instance.engine_code)
        instance.storehouse = validated_data.get('storehouse', instance.storehouse)
        instance.storage_location = validated_data.get('storage_location', instance.storage_location)
        instance.note = validated_data.get('note', instance.note)
        instance.equip_person = validated_data.get('equip_person', instance.equip_person)
        instance.save()
        # 从前端获取设备id
        print(validated_data, equipment_id)
        # 根据设备id在数据库中查找该设备的数据对象
        e_and_s_obj = EquipmentAndSensor.objects.filter(equipment_id=equipment_id)
        print(e_and_s_obj)

        sensor_list = []
        for obj in e_and_s_obj:
            sensor_list.append(obj.sensor_id)
            print(obj.sensor_id)
        # 将字符串转化成列表
        ar = validated_data.get('equipment_sensor')
        arr = ar.split(',')

        # 对列表进行遍历，更新新的传感器
        for obj in arr:
            if obj in sensor_list:
                pass
            else:
                equipment_instance = EquipmentAndSensor()
                equipment_instance.aid = uuid.uuid4().hex
                equipment_instance.equipment_id = equipment_id
                equipment_instance.sensor_id = obj
                equipment_instance.status = working
                equipment_instance.save()
        # 将淘汰的传感器状态设为不在设备上工作
        for obj in sensor_list:
            sensor_obj = EquipmentAndSensor.objects.filter(sensor_id=obj).first()
            sensor_obj.status = not_working
            sensor_obj.save()
        return instance
