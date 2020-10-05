import random
import time, datetime
import uuid
from datetime import datetime

from rest_framework import serializers

from App.models import MainEngine
from App.views_constant import on_production, stop_production


class MainEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainEngine
        fields = '__all__'
        read_only_fields = ('aid', 'engine_code',)

    def create(self, validated_data):
        instance = MainEngine()
        instance.aid = uuid.uuid4().hex
        now = datetime.now()  # 时间模块  现在时间
        instance.engine_code = now.strftime("%Y%m%d")+str(random.randint(100, 999))   # 导入事件模块和随机模块生成编号
        instance.engine_name = validated_data.get('engine_name')
        # 前端传字符串时，将其转化为datetime.date格式的方法
        # begin_time = validated_data.get('begin_time')
        # end_time = validated_data.get('end_time')
        # frt = '%Y-%m-%d'
        # time_tuple_begin = time.strptime(begin_time, frt)
        # time_tuple_end = time.strptime(end_time, frt)
        # year_begin, month_begin, day_begin = time_tuple_begin[:3]
        # year_end, month_end, day_end = time_tuple_end[:3]
        # instance.begin_time = datetime.date(year_begin, month_begin, day_begin)
        # instance.end_time = datetime.date(year_end, month_end, day_end)
        instance.begin_time=validated_data.get('begin_time')
        instance.end_time=validated_data.get('end_time')
        status = validated_data.get('status')
        if status == '在产':
            instance.status = on_production
        else:
            instance.status = stop_production
        instance.note = validated_data.get('note')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.engine_name = validated_data.get('engine_name', instance.engine_name)
        # 前端传字符串时，将其转化为datetime.date格式的方法
        # begin_time = validated_data.get('begin_time')
        # end_time = validated_data.get('end_time')
        # frt = '%Y-%m-%d'
        # time_tuple_begin = time.strptime(begin_time, frt)
        # time_tuple_end = time.strptime(end_time, frt)
        # year_begin, month_begin, day_begin = time_tuple_begin[:3]
        # year_end, month_end, day_end = time_tuple_end[:3]
        # instance.begin_time = datetime.date(year_begin, month_begin, day_begin)
        # instance.end_time = datetime.date(year_end, month_end, day_end)
        instance.begin_time = validated_data.get('begin_time',instance.begin_time)
        instance.end_time = validated_data.get('end_time',instance.end_time)
        instance.note = validated_data.get('note', instance.note)
        status = validated_data.get('status')
        if status == '在产':
            instance.status = on_production
        else:
            instance.status = stop_production
        instance.save()
        return instance
