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
from django.urls import path
from rest_framework.routers import DefaultRouter

from App import views
from App.views.client import ClientViewSet
from App.views.contact_people import ContactPeopleViewSet
from App.views.equipment import EquipmentViewSet
from App.views.equipment_allocation import EquipmentAllocationViewSet
from App.views.equipment_calibration import EquipmentCalibrationViewSet
from App.views.equipment_maintenance import EquipmentMaintenanceViewSet
from App.views.equipmentscrap import EquipmentScrapViewSet
from App.views.main_engine import MainEngineViewSet
from App.views.power import PowerViewSet
from App.views.power_relation import PowerRelationViewSet

from App.views.role import RoleViewSet
from App.views.sensor import SensorViewSet
from App.views.sensor_model import SensorModelViewSet
from App.views.sensor_type import SensorTypeViewSet
from App.views.user import UserViewSet
from App.views.water_quality_notice import WaterQualityNoticeViewSet

router = DefaultRouter()

router.register('main_engine', MainEngineViewSet)
router.register('equipment', EquipmentViewSet)
router.register('sensor_type', SensorTypeViewSet)
router.register('sensor_model', SensorModelViewSet)
router.register('client', ClientViewSet)
router.register('contact_people', ContactPeopleViewSet)
router.register('equipment_allocation', EquipmentAllocationViewSet)
router.register('equipment_maintenance', EquipmentMaintenanceViewSet)
router.register('sensor', SensorViewSet)
router.register('role', RoleViewSet)
router.register('power', PowerViewSet)
router.register('power_role', PowerRelationViewSet)
router.register('user', UserViewSet)
router.register('equipment_calibration', EquipmentCalibrationViewSet)
router.register('water_quality_notice', WaterQualityNoticeViewSet)
router.register('equipment_scrap', EquipmentScrapViewSet)

app_name = "App"

urlpatterns = [
    path('typemodel/', views.type_model, name='type_model'),  # 设备类型和设备型号连表路由
    path('operation/', views.operation, name='operation'),  # 设备、调拨、客户连表路由
    path('maintenance/', views.equipmentmaintenance, name='equipment_maintenance'),  # 单个设备的维护报修记录
    path('ClientContactPeople/', views.clientcontactpeople, name='clientcontactperson'),  # 每个用户对应的联系人查询
    path('real_time_monitoring_high/', views.real_time_monitoring_high, name='real_time_monitoring_high'),
    path('real_time_monitoring_down/', views.real_time_monitoring_down, name='real_time_monitoring_down'),
    path('sensor_type/', views.sensortype, name='sensor_type'),
    path('sensor_type_to_model/', views.sensortypetomodel, name='sensor_type_to_model'),
    path('equipment_to_engine_name/', views.equipmenttoenginename, name='equipment_to_engine_name'),
    path('equipment_to_sensor3/', views.equipmenttosensor3, name='equipment_to_sensor3'),
    path('sensor_model_to_code/', views.sensormodeltocode, name='sensor_model_to_code'),
    path('deviceNum_to_typename/', views.deviceNumtotypename, name='deviceNum_to_typename'),
    path('water_quality_notice/', views.waterqualitynotice, name='water_quality_notice'),
    path('main_engine_code_and_name/', views.mainenginecodeandname, name='main_engine_code_and_name'),
    path('equipment_detail/', views.equipmentdetail, name='equipment_detail'),
    path('login_in/', views.loginin, name='login_in'),
    path('verify/', views.verify, name='verify'),
    path('sensor_calibration_retrieve/', views.sensorcalibrationretrieve, name='sensor_calibration_retrieve'),
    path('role_power/', views.rolepowers, name='role_power'),
    path('water_notice_retrieve/', views.waternoticeretrieve, name='water_notice_retrieve'),
    path('equipment_scrap_retrieve/', views.equipmentscrapretrieve, name='equipment_scrap_retrieve'),
    path('equipment_configuration_retrieve/', views.equipmentconfigurationretrieve, name='equipment_configuration_retrieve'),
    path('equipment_allocation_retrieve/', views.equipmentallocationretrieve, name='equipment_allocation_retrieve'),
    path('equipment_allocate_factory/', views.equipmentallocatefactory, name='equipment_allocate_factory'),
    path('websocket_relation/',views.websocketrelation, name='websocket_relation')
    # path传参路由可以直接接着写 /？xxx 而不用在urls中添加<str:yyy>，views中直接request.GET.get("yyy")
]