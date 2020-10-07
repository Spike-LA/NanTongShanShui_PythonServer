"""ntss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from App import views
from App.views.client import ClientViewSet
from App.views.contact_people import ContactPeopleViewSet
from App.views.equipment import EquipmentViewSet
from App.views.main_engine import MainEngineViewSet
from App.views.sensor_model import SensorModelViewSet
from App.views.sensor_type import SensorTypeViewSet

router = DefaultRouter()

router.register('main_engine', MainEngineViewSet)
router.register('equipment', EquipmentViewSet)
router.register('sensor_type', SensorTypeViewSet)
router.register('sensor_model', SensorModelViewSet)
router.register('client', ClientViewSet)
router.register('contact_people', ContactPeopleViewSet)


app_name = "App"
urlpatterns = [
    path('typemodel/', views.type_model, name='type_model'),  # 连表路由
]
