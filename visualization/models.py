# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BerthBelong(models.Model):
    berth = models.CharField(primary_key=True, max_length=6)
    block = models.ForeignKey('BlocksCapacity', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'berth_belong'


class BlocksCapacity(models.Model):
    block_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=3, blank=True, null=True)
    area = models.CharField(max_length=10, blank=True, null=True)
    road = models.CharField(max_length=12, blank=True, null=True)
    left_or_right = models.CharField(max_length=2, blank=True, null=True)
    direction = models.CharField(max_length=2, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    type = models.CharField(max_length=4, blank=True, null=True)
    strategy = models.CharField(max_length=8, blank=True, null=True)
    capacity = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'blocks_capacity'


class OccupancyList(models.Model):
    record_id = models.AutoField(primary_key=True)
    admin_region = models.CharField(max_length=10, blank=True, null=True)
    berthage = models.CharField(max_length=8, blank=True, null=True)
    in_time = models.DateTimeField(blank=True, null=True)
    out_time = models.DateTimeField(blank=True, null=True)
    section = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'occupancy_list'


class RoadList(models.Model):
    road = models.CharField(primary_key=True, max_length=12)
    longitude = models.CharField(max_length=18, blank=True, null=True)
    latitude = models.CharField(max_length=18, blank=True, null=True)
    area = models.CharField(max_length=3, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_list'


class RoadShape(models.Model):
    block = models.CharField(max_length=12)
    shape = models.TextField()

    class Meta:
        managed = True
