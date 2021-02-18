import random
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import Equipment, Sensor, EquipmentAndSensor, Pump

from App.views_constant import working, stop_run, is_using, un_using, equipped, not_equipped


class EquipmentSerializer(serializers.ModelSerializer):
    # 写了write_only之后这个字段就不会用于存储了
    equipment_sensor = serializers.CharField(write_only=True, allow_null=True)
    equipment_pump = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = Equipment  # 级联的模型#

        fields = '__all__'  # 显示所需要的字段#     #'__all__'显示全部的字段#

        read_only_fields = ('aid','create_time', 'alert_time','status')

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
        instance.status = stop_run

        instance.save()

        # 设备上的每个传感器id,前端传输格式为"12344,54321"
        ar = validated_data.get('equipment_sensor')
        if ar != 'false':
            # split方法对字符串进行分割，然后形成列表
            arr = ar.split(',')

            for obj in arr:
                equipment_instance = EquipmentAndSensor()
                equipment_instance.aid = uuid.uuid4().hex
                equipment_instance.equipment_id = instance.aid
                equipment_instance.sensor_id = obj
                sensor_obj = Sensor.objects.filter(aid=obj).first()
                sensor_obj.status = is_using
                sensor_obj.save()
                equipment_instance.status = working
                equipment_instance.save()

        # 设备上装配的每个泵的id，前端传输格式为"12344,54321"
        br = validated_data.get('equipment_pump')
        if br != 'false':
            # split方法对字符串进行分割，然后形成列表
            brr = br.split(',')

            for pump_obj_id in brr:
                pump_obj = Pump.objects.filter(pump_id=pump_obj_id).first() # 找到装配的泵对象
                pump_obj.equipment_code = instance.equipment_code
                pump_obj.status = equipped
                pump_obj.save()

        return instance

    def update(self, instance, validated_data):
        equipment_id = instance.aid
        instance.engine_code = validated_data.get('engine_code', instance.engine_code)
        instance.storehouse = validated_data.get('storehouse', instance.storehouse)
        instance.storage_location = validated_data.get('storage_location', instance.storage_location)
        instance.note = validated_data.get('note', instance.note)
        instance.equip_person = validated_data.get('equip_person', instance.equip_person)
        instance.save()
        # 从前端获取设备id
        # 根据设备id在数据库中查找该设备的数据对象
        e_and_s_obj = EquipmentAndSensor.objects.filter(equipment_id=equipment_id)

        sensor_list = []
        for obj in e_and_s_obj:
            sensor_list.append(obj.sensor_id)
            obj.delete()
        print(sensor_list)
        for obj_2 in sensor_list:
            sensor_obj = Sensor.objects.filter(aid=obj_2).first()
            sensor_obj.status = un_using
            sensor_obj.save()
        # 将字符串转化成列表
        ar = validated_data.get('equipment_sensor')
        if ar != 'false':
            arr = ar.split(',')

            # 对列表进行遍历，更新新的传感器
            print(arr)
            for obj in arr:
                equipment_instance = EquipmentAndSensor()
                equipment_instance.aid = uuid.uuid4().hex
                equipment_instance.equipment_id = equipment_id
                equipment_instance.sensor_id = obj
                sensor_obj = Sensor.objects.filter(aid=obj).first()
                sensor_obj.status = is_using
                sensor_obj.save()
                equipment_instance.status = working
                equipment_instance.save()

         # 获取更新后设备上装配的泵的id
        br = validated_data.get('equipment_pump')
        if br != 'false':
            # split方法对字符串进行分割，然后形成列表
            brr = br.split(',')
        # 获取原来的泵，并修改它们的状态以及将它们从泵上撤下来
        old_equipped_pump_query = Pump.objects.filter(equipment_code=instance.equipment_code)
        for old_pump_object in old_equipped_pump_query:
            old_pump_object.status = not_equipped
            old_pump_object.equipment_code = ''
            old_pump_object.save()

        for new_pump_obj_id in brr:
            new_pump_obj = Pump.objects.filter(pump_id=new_pump_obj_id).first()  # 找到装配的泵对象
            new_pump_obj.equipment_code = instance.equipment_code
            new_pump_obj.status = equipped
            new_pump_obj.save()
        return instance
