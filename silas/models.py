# -*- coding:utf-8 -*-
#author:hjd
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Assets(models.Model):
    assets_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,unique=True)
    sn = models.CharField(max_length=100, null=True)
    assetsclass_id = models.ForeignKey('AssetSClass')
    manufactor=models.CharField(max_length=100,null=True)
    business=models.ForeignKey('Business',null=True,related_name='assets_set')
    assets_admin=models.ForeignKey('AssetsAdmin',null=True,related_name='assets_set')
    seat=models.ForeignKey('Seat',related_name='assets_set')
    pact=models.ForeignKey('Pact',null=True,related_name='assets_set')
    purchasing_date=models.DateField(null=True)
    warranty_date=models.DateField(null=True)
    price=models.FloatField(null=True)
    remarks=models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class AssetFClass(models.Model):
    assetfclass_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,unique=True)
    remarks = models.TextField(null=True)

class AssetSClass(models.Model):
    assetsclass_id=models.AutoField(primary_key=True)
    assetfclass_id=models.ForeignKey('AssetFClass')
    name=models.CharField(max_length=50,unique=True)
    remarks = models.TextField(null=True)

class Business(models.Model):
    business_id=models.AutoField(primary_key=True)
    superior_business=models.ForeignKey('Business',null=True)
    name=models.CharField(max_length=100,unique=True)
    remarks=models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class AssetsAdmin(models.Model):
    assets_admin_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    tel=models.CharField(max_length=20,unique=True)
    qq=models.BigIntegerField(null=True)
    email=models.CharField(max_length=200,null=True)
    remarks=models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class Seat(models.Model):
    seat_id=models.AutoField(primary_key=True)
    seat_room=models.ForeignKey('Room')
    name=models.CharField(max_length=100)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ("seat_room", "name")

class Room(models.Model):
    room_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,unique=True)
    idcadmin=models.CharField(max_length=100,null=True)
    tel=models.CharField(max_length=20,null=True)
    qq=models.BigIntegerField(null=True)
    email=models.CharField(max_length=200,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class Pact(models.Model):
    pacr_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    sn=models.CharField(max_length=100,unique=True)
    price = models.IntegerField(null=True)
    file_path=models.CharField(max_length=200,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class CPU(models.Model):
    CPU_id=models.AutoField(primary_key=True)
    model=models.CharField(max_length=200)
    sn=models.CharField(max_length=100,unique=True,null=True)
    corenum=models.IntegerField()
    nowspeed=models.FloatField()
    slot = models.CharField(max_length=64,null=True)
    asset_id = models.ForeignKey('Assets',null=True)
    manufactor=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class MEM(models.Model):
    MEM_id=models.AutoField(primary_key=True)
    model=models.CharField(max_length=200)
    sn=models.CharField(max_length=100,unique=True,null=True)
    capacity=models.IntegerField()
    nowspeed=models.IntegerField(null=True)
    slot = models.CharField(max_length=64,null=True)
    interface = models.CharField(max_length=64,null=True)
    asset_id = models.ForeignKey('Assets',null=True)
    manufactor=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class Disk(models.Model):
    disk_id=models.AutoField(primary_key=True)
    model=models.CharField(max_length=200)
    type=models.CharField(max_length=64,null=True)
    sn=models.CharField(max_length=100,unique=True,null=True)
    capacity=models.IntegerField()
    nowspeed=models.IntegerField(null=True)
    slot = models.CharField(max_length=64,null=True)
    interface = models.CharField(max_length=64,null=True)
    asset_id = models.ForeignKey('Assets',null=True)
    manufactor=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class Net(models.Model):
    net_id=models.AutoField(primary_key=True)
    model=models.CharField(max_length=200)
    sn=models.CharField(max_length=100,unique=True,null=True)
    name=models.CharField(max_length=65,null=True)
    nowspeed=models.IntegerField(null=True)
    mac = models.CharField(max_length=64,null=True)
    ip = models.GenericIPAddressField(protocol='both',null=True)
    asset_id = models.ForeignKey('Assets',null=True)
    manufactor=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)


class OtherPart(models.Model):
    other_part_id=models.AutoField(primary_key=True)
    model=models.CharField(max_length=200)
    sn=models.CharField(max_length=100,unique=True,null=True)
    name=models.CharField(max_length=65,null=True)
    asset_id = models.ForeignKey('Assets',null=True)
    manufactor=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

class Database(models.Model):
    database_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    version=models.CharField(max_length=100,null=True)
    port=models.IntegerField(null=True)
    remarks = models.TextField(null=True)
    asset_id = models.ManyToManyField('Assets')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "version",'port')


class Middleware(models.Model):
    middleware_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    version=models.CharField(max_length=100,null=True)
    port=models.IntegerField(null=True)
    remarks = models.TextField(null=True)
    asset_id = models.ManyToManyField('Assets')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "version",'port')

class App(models.Model):
    app_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    version=models.CharField(max_length=100,null=True)
    port=models.IntegerField(null=True)
    language=models.CharField(max_length=100,null=True)
    remarks = models.TextField(null=True)
    asset_id = models.ManyToManyField('Assets')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "version",'port','language')

class OS(models.Model):
    os_id=models.AutoField(primary_key=True)
    os_class_dic=(
        ('Linux','Linux'),
        ('UNIX', 'UNIX'),
        ('Windows','Windows')
    )
    bit_dic=(
        ('X86','X86'),
        ('X64', 'X64'),
    )
    os_class = models.CharField(choices=os_class_dic, max_length=100)
    version=models.CharField(max_length=100)
    bit=models.CharField(choices=bit_dic, max_length=50)
    remarks = models.TextField(null=True)
    asset_id = models.ManyToManyField('Assets')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("os_class", "version",'bit')
