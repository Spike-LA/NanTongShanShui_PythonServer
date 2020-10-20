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
from App.views.customer_account import CustomerAccountViewSet
from App.views.enterprise_account import EnterpriseAccountViewSet
from App.views.equipment import EquipmentViewSet
from App.views.equipment_allocation import EquipmentAllocationViewSet
from App.views.equipment_maintenance import EquipmentMaintenanceViewSet
from App.views.main_engine import MainEngineViewSet
from App.views.power import PowerViewSet
from App.views.power_role import PowerRoleViewSet
from App.views.role import RoleViewSet
from App.views.sensor import SensorViewSet
from App.views.sensor_model import SensorModelViewSet
from App.views.sensor_type import SensorTypeViewSet

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
router.register('enterprise_account', EnterpriseAccountViewSet)
router.register('customer_account', CustomerAccountViewSet)
router.register('role', RoleViewSet)
router.register('power', PowerViewSet)
router.register('power_role', PowerRoleViewSet)


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
    # path传参路由可以直接接着写 /？xxx 而不用在urls中添加<str:yyy>，views中直接request.GET.get("yyy")
]

