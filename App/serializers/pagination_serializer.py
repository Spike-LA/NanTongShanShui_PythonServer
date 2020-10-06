from App.models import MainEngine
from rest_framework import serializers


class PagerSerializer(serializers.ModelSerializer):  # main_engine分页
    class Meta:
        model = MainEngine
        fields = "__all__"
