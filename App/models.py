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

    class Meta:
        managed = False
        db_table = 'client'


class ContactPeople(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    contact_person = models.CharField(max_length=50)
    client_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'contact_people'


class CustomerAccount(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    account_id = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    account_password = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=255)
    role = models.CharField(max_length=50, blank=True, null=True)
    add_time = models.DateField(blank=True, null=True)
    add_by = models.CharField(max_length=50, blank=True, null=True)
    mod_time = models.DateField(blank=True, null=True)
    mod_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'customer_account'


class EnterpriseAccount(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    account_id = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    enterprise_number = models.CharField(max_length=50, blank=True, null=True)
    account_password = models.CharField(max_length=50, blank=True, null=True)
    telephone_number = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    add_time = models.DateField(blank=True, null=True)
    add_by = models.CharField(max_length=50, blank=True, null=True)
    mod_time = models.DateField(blank=True, null=True)
    mod_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_account'


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


class EquipmentAndSensor(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    equipment_id = models.CharField(max_length=255)
    sensor_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'equipment and sensor'


class EquipmentAllocation(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    table_id = models.CharField(max_length=50)
    host_number = models.CharField(max_length=50)
    host_name = models.CharField(max_length=50)
    equipment_number = models.CharField(max_length=50)
    equipment_remark = models.CharField(max_length=50, blank=True, null=True)
    applicant = models.CharField(max_length=50, blank=True, null=True)
    applicant_time = models.DateField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    allocation_reason = models.CharField(max_length=50, blank=True, null=True)
    transport_unit = models.CharField(max_length=50, blank=True, null=True)
    agent = models.CharField(max_length=50, blank=True, null=True)
    agent_tel = models.CharField(max_length=50, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    sign = models.CharField(max_length=50, blank=True, null=True)
    approval_time = models.DateField(blank=True, null=True)
    remark = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_allocation'


class EquipmentMaintenance(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    equipment_id = models.CharField(max_length=255)
    repair_time = models.DateField()
    maintain_time = models.DateField()
    maintain_cause = models.CharField(max_length=255)
    fault_description = models.CharField(max_length=255)
    maintain_result = models.CharField(max_length=50)
    maintain_status = models.CharField(max_length=50)
    responsible_person = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'equipment_maintenance'


class EquipmentScrap(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    table_id = models.CharField(max_length=50)
    host_number = models.CharField(max_length=50)
    host_name = models.CharField(max_length=50)
    equipment_number = models.CharField(max_length=50)
    equipment_remark = models.CharField(max_length=50, blank=True, null=True)
    warehouse = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    applicant = models.CharField(max_length=50, blank=True, null=True)
    applicant_time = models.DateField(blank=True, null=True)
    applicant_tel = models.CharField(max_length=50, blank=True, null=True)
    applicant_department = models.CharField( max_length=50, blank=True, null=True)
    scrapping_reasons = models.CharField(max_length=50, blank=True, null=True)
    opinion = models.CharField(max_length=50, blank=True, null=True)
    sign = models.CharField(max_length=50, blank=True, null=True)
    approval_time = models.DateField(blank=True, null=True)
    remark = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_scrap'


class MainEngine(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    engine_code = models.CharField(max_length=50)
    engine_name = models.CharField(max_length=50)
    begin_time = models.DateField()
    end_time = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_engine'


class Sensor(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_model_id = models.CharField(max_length=255)
    sensor_code = models.CharField(max_length=50)
    create_time = models.DateField()
    alert_time = models.DateField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorModel(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    sensor_type_id = models.CharField(max_length=255)
    sensor_model = models.CharField(max_length=50)
    sensor_threshold = models.CharField(max_length=50)
    notice_content = models.CharField(max_length=50)
    create_time = models.DateField(auto_now_add=True)
    create_people = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sensor_model'


class SensorType(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    type_name = models.CharField(max_length=50)
    create_time = models.DateField(auto_now_add=True)
    create_people = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sensor_type'


class WaterQualityNotice(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    target = models.CharField(max_length=50)
    measurement = models.CharField(max_length=50)
    notice_time = models.CharField(max_length=50)
    deal_time = models.CharField(max_length=50)
    deal_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'water_quality_notice'
