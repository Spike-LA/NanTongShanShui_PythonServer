# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Client(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    client_code = models.CharField(max_length=50)
    client_unit = models.CharField(max_length=50)
    client_address = models.CharField(max_length=50)
    client_zip_code = models.CharField(max_length=50, blank=True, null=True)
    client_industry = models.CharField(max_length=50)
    unit_phone = models.CharField(max_length=50)
    unit_fax = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class ContactPeople(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    contact_person = models.CharField(max_length=50)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    contact_position = models.CharField(max_length=50)
    contact_tel = models.CharField(max_length=50)
    remark = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_people'


class Equipment(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    equipment_code = models.CharField(max_length=50)
    engine_code = models.CharField(max_length=50)
    storehouse = models.CharField(max_length=50)
    storage_location = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)
    equip_person = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    alert_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment'


class EquipmentAllocation(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    engine_id = models.CharField(max_length=50)
    equipment_id = models.CharField(max_length=255)
    applicant = models.CharField(max_length=50, blank=True, null=True)
    applicant_tel = models.CharField(max_length=50, blank=True, null=True)
    applicant_time = models.DateField(blank=True, null=True, auto_now_add=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    transfer_unit = models.CharField(max_length=50, blank=True, null=True)
    transfer_unit_ads = models.CharField(max_length=50, blank=True, null=True)
    transfer_unit_tel = models.CharField(max_length=50, blank=True, null=True)
    allocation_reason = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_allocation'


class EquipmentAndSensor(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    equipment_id = models.CharField(max_length=255)
    sensor_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'equipment_and_sensor'


class EquipmentMaintenance(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    equipment_id = models.CharField(max_length=255, blank=True, null=True)
    repair_time = models.DateField(blank=True, null=True, auto_now_add=True)
    maintain_time = models.DateField(blank=True, null=True)
    maintain_cause = models.CharField(max_length=255, blank=True, null=True)
    fault_description = models.CharField(max_length=255, blank=True, null=True)
    maintain_result = models.CharField(max_length=50, blank=True, null=True)
    maintain_status = models.CharField(max_length=50, blank=True, null=True)
    responsible_person = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_maintenance'


class EquipmentScrap(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    engine_id = models.CharField(max_length=255)
    equipment_id = models.CharField(max_length=255)
    applicant = models.CharField(max_length=50, blank=True, null=True)
    applicant_time = models.DateField(blank=True, null=True, auto_now_add=True)
    applicant_tel = models.CharField(max_length=50, blank=True, null=True)
    scrapping_reasons = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_scrap'


class MainEngine(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    engine_code = models.CharField(max_length=50)
    engine_name = models.CharField(max_length=50)
    begin_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_engine'


class Sensor(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_model_id = models.CharField(max_length=255, blank=True, null=True)
    sensor_code = models.CharField(max_length=50)
    create_time = models.DateField(auto_now_add=True)
    alert_time = models.DateField(auto_now=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    default_compensation = models.CharField(max_length=50, blank=True, null=True)
    theoretical_value = models.CharField(max_length=50, blank=True, null=True)
    high_sensor_threshold = models.CharField(max_length=50, blank=True, null=True)
    down_sensor_threshold = models.CharField(max_length=50, blank=True, null=True)
    notice_content = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorCalibration(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_id = models.CharField(max_length=255, blank=True, null=True)
    actual_value = models.CharField(max_length=50, blank=True, null=True)
    calibrate_compensation = models.CharField(max_length=50, blank=True, null=True)
    calibrate_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    remark = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_calibration'


class SensorModel(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_type_id = models.CharField(max_length=255)
    sensor_model = models.CharField(max_length=50)
    high_sensor_threshold = models.CharField(max_length=50, blank=True, null=True)
    down_sensor_threshold = models.CharField(max_length=50, blank=True, null=True)
    notice_content = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateField(auto_now_add=True)
    states = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_model'


class SensorType(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    type_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_type'


class WaterQualityNotice(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_id = models.CharField(max_length=255, blank=True, null=True)
    measurement = models.CharField(max_length=50, blank=True, null=True)
    notice_time = models.DateTimeField(blank=True, null=True)
    deal_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    deal_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'water_quality_notice'


class User(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=50, blank=True, null=True)
    account = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    telephone_num = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    role_id = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateField(auto_now_add=True, blank=True, null=True)
    add_by = models.CharField(max_length=50, blank=True, null=True)
    mod_time = models.DateField(auto_now=True, blank=True, null=True)
    mod_by = models.CharField(max_length=50, blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    login_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Role(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    role_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class Power(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    power = models.CharField(max_length=50, blank=True, null=True)
    power_num = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'power'


class PowerRelation(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    power_id = models.CharField(max_length=255, blank=True, null=True)
    aim_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'power_relation'


class WebsocketRelation(models.Model):
    wid = models.AutoField(primary_key=True)
    websocket_id = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.CharField(max_length=255, blank=True, null=True)
    distinguish_code = models.CharField(max_length=255, blank=True, null=True)
    equipment_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'websocket_relation'


class EquipmentOperationLog(models.Model):
    command_id = models.CharField(primary_key=True, max_length=255)
    operation_time = models.DateTimeField(blank=True, null=True)
    operation_person_id = models.CharField(max_length=255, blank=True, null=True)
    operation_equipment_code = models.CharField(max_length=255, blank=True, null=True)
    operation_pump_code = models.CharField(max_length=255, blank=True, null=True)
    dosage = models.CharField(max_length=255, blank=True, null=True)
    open_time = models.CharField(max_length=255, blank=True, null=True)
    send_status = models.CharField(max_length=50, blank=True, null=True)
    operate_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_operation_log'


class Pump(models.Model):
    pump_id = models.CharField(primary_key=True, max_length=255)
    pump_name = models.CharField(max_length=50, blank=True, null=True)
    pump_code = models.CharField(max_length=50, blank=True, null=True)
    equipment_code = models.CharField(max_length=50, blank=True, null=True)
    fluid_flow = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateField(blank=True, null=True, auto_now_add=True)
    create_by = models.CharField(max_length=255, blank=True, null=True)
    mod_time = models.DateField(blank=True, null=True, auto_now=True)
    mod_by = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pump'

class PumpPermission(models.Model):
    permission_id = models.CharField(primary_key=True, max_length=255)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    pump_id = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateField(blank=True, null=True, auto_now_add=True)
    create_by = models.CharField(max_length=50, blank=True, null=True)
    mod_time = models.DateField(blank=True, null=True, auto_now=True)
    mod_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pump_permission'

class RealTimeData(models.Model):
    uuid = models.CharField(primary_key=True, max_length=255)
    equipment_code = models.CharField(max_length=50, blank=True, null=True)
    mearsure_type = models.CharField(max_length=50, blank=True, null=True)
    measurement = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'real_time_data'

class AutoOperationInfo(models.Model):
    uuid = models.CharField(primary_key=True, max_length=255)
    pump_code = models.CharField(max_length=50, blank=True, null=True)
    operation_type = models.CharField(max_length=50, blank=True, null=True)
    operation_time = models.CharField(max_length=50, blank=True, null=True)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    period = models.CharField(max_length=50, blank=True, null=True)
    next_run_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    create_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_operation_info'

