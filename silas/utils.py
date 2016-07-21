# -*- coding:utf-8 -*-
#author:hjd
from silas import models

def makeroomdic():
    rooms=models.Room.objects.all()
    roomdic={}
    for room_ob in rooms:
        roomdic[room_ob.room_id]={'name':room_ob.name,'idcadmin':room_ob.idcadmin,'tel':room_ob.tel,'qq':room_ob.qq,
                                  'email':room_ob.email,'seats':{}}
        for seat_ob in models.Seat.objects.filter(seat_room=room_ob):
            roomdic[room_ob.room_id]['seats'][seat_ob.seat_id]=seat_ob.name
    return roomdic

def makebusinessdic():
    business_obs=models.Business.objects.all()
    business_dic={}
    for business_ob in business_obs:
        business_dic[business_ob.business_id]={'name':business_ob.name,'superior_business_id':business_ob.superior_business_id}
    return business_dic

def makepactdic():
    pact_obs=models.Pact.objects.all()
    pactdic={}
    for pact_ob in pact_obs:
        pactdic[pact_ob.pacr_id]={'name':pact_ob.name,'sn':pact_ob.sn,'price':pact_ob.price,'file_path':pact_ob.file_path}
    return pactdic

def makeassetclassdic():
    assetfclasss=models.AssetFClass.objects.all()
    assetclassdic={}
    for assetfclass_ob in assetfclasss:
        assetclassdic[assetfclass_ob.assetfclass_id]={'name':assetfclass_ob.name,'assetsclasss':{}}
        for assetsclass_ob in models.AssetSClass.objects.filter(assetfclass_id=assetfclass_ob):
            assetclassdic[assetfclass_ob.assetfclass_id]['assetsclasss'][assetsclass_ob.assetsclass_id]=assetsclass_ob.name
    return assetclassdic

def makeassetadmindic():
    assetadmin_obs=models.AssetsAdmin.objects.all()
    assetadmindic={}
    for assetadmin_ob in assetadmin_obs:
        assetadmindic[assetadmin_ob.assets_admin_id]={'name':assetadmin_ob.name,'tel':assetadmin_ob.tel,
                                                      'qq':assetadmin_ob.qq,'email':assetadmin_ob.email}
    return assetadmindic

def delassets(jsondata):
    models.Assets.objects.filter(assets_id__in=jsondata['rows']).delete()
    return {'result':1}


def delassetadmins(jsondata):
    models.AssetsAdmin.objects.filter(assets_admin_id__in=jsondata['rows']).delete()
    return {'result':1}

def addassetadmins(jsondata):
    try:
        models.AssetsAdmin.objects.create(name=jsondata['name'],tel=jsondata['tel'],
                                          email=jsondata.get('email'),qq=jsondata.get('qq'),
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changeassetadmins(jsondata):
    try:
        models.AssetsAdmin.objects.filter(assets_admin_id=jsondata['id']).update(name=jsondata['name'],tel=jsondata['tel'],
                                          email=jsondata.get('email'),qq=jsondata.get('qq'),
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delrooms(jsondata):
    models.Room.objects.filter(room_id__in=jsondata['rows']).delete()
    return {'result':1}

def addroom(jsondata):
    try:
        models.Room.objects.create(name=jsondata['name'],tel=jsondata.get('tel'),
                                          idcadmin=jsondata.get('idcadmin'),
                                          email=jsondata.get('email'),qq=jsondata.get('qq'),
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changeroom(jsondata):
    try:
        models.Room.objects.filter(room_id=jsondata['id']).update(name=jsondata['name'],tel=jsondata.get('tel'),
                                          idcadmin=jsondata.get('idcadmin'),
                                          email=jsondata.get('email'),qq=jsondata.get('qq'),
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delpacts(jsondata):
    models.Pact.objects.filter(pacr_id__in=jsondata['rows']).delete()
    return {'result':1}

def addpact(jsondata):
    try:
        models.Pact.objects.create(name=jsondata['name'],sn=jsondata['sn'],
                                   price=jsondata.get('price'),
                                   file_path=jsondata.get('file_path'),
                                   remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changepact(jsondata):
    try:
        models.Pact.objects.filter(pacr_id=jsondata['id']).update(name=jsondata['name'],sn=jsondata['sn'],
                                   price=jsondata.get('price'),
                                   file_path=jsondata.get('file_path'),
                                   remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}


def delracks(jsondata):
    models.Seat.objects.filter(seat_id__in=jsondata['rows']).delete()
    return {'result':1}

def addrack(jsondata):
    try:
        room_ob=models.Room.objects.get(room_id=jsondata['roomid'])
        models.Seat.objects.create(name=jsondata['name'],seat_room=room_ob,
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changerack(jsondata):
    try:
        room_ob = models.Room.objects.get(room_id=jsondata['roomid'])
        models.Seat.objects.filter(seat_id=jsondata['id']).update(name=jsondata['name'],seat_room=room_ob,
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delbusinesss(jsondata):
    models.Business.objects.filter(business_id__in=jsondata['rows']).delete()
    return {'result':1}

def addbusiness(jsondata):
    if jsondata.get('SBusiness'):
        sbusiness_ob = models.Business.objects.get(business_id=int(jsondata['SBusiness']))
    else:
        sbusiness_ob = None
    try:
        models.Business.objects.create(name=jsondata['name'],superior_business=sbusiness_ob,
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changebusiness(jsondata):
    if jsondata.get('SBusiness'):
        sbusiness_ob = models.Business.objects.get(business_id=int(jsondata['SBusiness']))
    else:
        sbusiness_ob = None
    try:
        models.Business.objects.filter(business_id=jsondata['id']).update(name=jsondata['name'],superior_business=sbusiness_ob,
                                          remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delcpus(jsondata):
    models.CPU.objects.filter(CPU_id__in=jsondata['rows']).delete()
    return {'result':1}

def addcpu(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.CPU.objects.create(model=jsondata['model'],sn=jsondata.get('sn'),corenum=jsondata['corenum'],
                                  nowspeed=jsondata['nowspeed'],slot=jsondata.get('slot'),manufactor=jsondata['manufactor'],
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changecpu(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.CPU.objects.filter(CPU_id=jsondata['id']).update(model=jsondata['model'],sn=jsondata.get('sn'),corenum=jsondata['corenum'],
                                  nowspeed=jsondata['nowspeed'],slot=jsondata.get('slot'),manufactor=jsondata['manufactor'],
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delmems(jsondata):
    models.MEM.objects.filter(MEM_id__in=jsondata['rows']).delete()
    return {'result':1}

def addmem(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.MEM.objects.create(model=jsondata['model'],sn=jsondata.get('sn'),capacity=jsondata['capacity'],
                                  nowspeed=jsondata.get('nowspeed'),slot=jsondata.get('slot'),manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'),interface=jsondata.get('interface'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changemem(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.MEM.objects.filter(MEM_id=jsondata['id']).update(model=jsondata['model'],sn=jsondata.get('sn'),capacity=jsondata['capacity'],
                                  nowspeed=jsondata.get('nowspeed'),slot=jsondata.get('slot'),manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'),interface=jsondata.get('interface'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def deldisks(jsondata):
    models.Disk.objects.filter(disk_id__in=jsondata['rows']).delete()
    return {'result':1}

def adddisk(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.Disk.objects.create(model=jsondata['model'],sn=jsondata.get('sn'),capacity=jsondata['capacity'],
                                  nowspeed=jsondata.get('nowspeed'),slot=jsondata.get('slot'),manufactor=jsondata.get('manufactor'),
                                  type=jsondata['type'],
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'),interface=jsondata.get('interface'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changedisk(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.Disk.objects.filter(disk_id=jsondata['id']).update(model=jsondata['model'],sn=jsondata.get('sn'),capacity=jsondata['capacity'],
                                  nowspeed=jsondata.get('nowspeed'),slot=jsondata.get('slot'),manufactor=jsondata.get('manufactor'),
                                                                  type=jsondata['type'],
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'),interface=jsondata.get('interface'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delnets(jsondata):
    models.Net.objects.filter(net_id__in=jsondata['rows']).delete()
    return {'result':1}

def addnet(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.Net.objects.create(model=jsondata['model'],sn=jsondata.get('sn'),name=jsondata.get('name'),
                                  nowspeed=jsondata.get('nowspeed'),mac=jsondata.get('mac'),ip=jsondata.get('ip'),
                                  manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changenet(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.Net.objects.filter(net_id=jsondata['id']).update(model=jsondata['model'],sn=jsondata.get('sn'),name=jsondata.get('name'),
                                  nowspeed=jsondata.get('nowspeed'),mac=jsondata.get('mac'),ip=jsondata.get('ip'),
                                  manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def delotherparts(jsondata):
    models.OtherPart.objects.filter(other_part_id__in=jsondata['rows']).delete()
    return {'result':1}

def addotherpart(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.OtherPart.objects.create(model=jsondata['model'],sn=jsondata.get('sn'),name=jsondata.get('name'),
                                  manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changeotherpart(jsondata):
    if jsondata.get('asset_id'):
        asset_ob=models.Assets.objects.get(assets_id=jsondata['asset_id'])
    else:
        asset_ob=None
    try:
        models.OtherPart.objects.filter(other_part_id=jsondata['id']).update(model=jsondata['model'],sn=jsondata.get('sn'),name=jsondata.get('name'),
                                  manufactor=jsondata.get('manufactor'),
                                  asset_id=asset_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def deldatabases(jsondata):
    models.Database.objects.filter(database_id__in=jsondata['rows']).delete()
    return {'result':1}

def adddatabase(jsondata):
    try:
        database_ob=models.Database.objects.get_or_create(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        if database_ob[1]:
            asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
            database_ob[0].asset_id.add(*asset_obs)
        else:
            raise Exception(' ')

    except:
        return {'result':0}
    else:
        return {'result':1}

def changedatabase(jsondata):
    try:
        models.Database.objects.filter(database_id=jsondata['id']).update(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
        database_ob=models.Database.objects.get(database_id=jsondata['id'])
        database_ob.asset_id.remove(*database_ob.asset_id.all())
        database_ob.asset_id.add(*asset_obs)
    except:
        return {'result':0}
    else:
        return {'result':1}

def delmiddlewares(jsondata):
    models.Middleware.objects.filter(middleware_id__in=jsondata['rows']).delete()
    return {'result':1}

def addmiddleware(jsondata):
    try:
        middleware_ob=models.Middleware.objects.get_or_create(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        if middleware_ob[1]:
            asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
            middleware_ob[0].asset_id.add(*asset_obs)
        else:
            raise Exception(' ')

    except:
        return {'result':0}
    else:
        return {'result':1}

def changemiddleware(jsondata):
    try:
        models.Middleware.objects.filter(middleware_id=jsondata['id']).update(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
        middleware_ob=models.Middleware.objects.get(middleware_id=jsondata['id'])
        middleware_ob.asset_id.remove(*middleware_ob.asset_id.all())
        middleware_ob.asset_id.add(*asset_obs)
    except:
        return {'result':0}
    else:
        return {'result':1}

def delapps(jsondata):
    models.App.objects.filter(app_id__in=jsondata['rows']).delete()
    return {'result':1}

def addapp(jsondata):
    try:
        app_ob=models.App.objects.get_or_create(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                                language=jsondata.get('language'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        if app_ob[1]:
            asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
            app_ob[0].asset_id.add(*asset_obs)
        else:
            raise Exception(' ')

    except:
        return {'result':0}
    else:
        return {'result':1}

def changeapp(jsondata):
    try:
        models.App.objects.filter(app_id=jsondata['id']).update(name=jsondata['name'],remarks=jsondata.get('remarks'),
                                                                language=jsondata.get('language'),
                                               port=jsondata.get('port'),version=jsondata.get('version'))
        asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
        app_ob=models.App.objects.get(app_id=jsondata['id'])
        app_ob.asset_id.remove(*app_ob.asset_id.all())
        app_ob.asset_id.add(*asset_obs)
    except:
        return {'result':0}
    else:
        return {'result':1}

def deloss(jsondata):
    models.OS.objects.filter(os_id__in=jsondata['rows']).delete()
    return {'result':1}

def addos(jsondata):
    try:
        os_ob=models.OS.objects.get_or_create(version=jsondata['version'],remarks=jsondata.get('remarks'),
                                               bit=jsondata['bit'],os_class=jsondata['os_class'])
        if os_ob[1]:
            asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
            os_ob[0].asset_id.add(*asset_obs)
        else:
            raise Exception(' ')

    except:
        return {'result':0}
    else:
        return {'result':1}

def changeos(jsondata):
    try:
        models.OS.objects.filter(os_id=jsondata['id']).update(version=jsondata['version'],remarks=jsondata.get('remarks'),
                                               bit=jsondata['bit'],os_class=jsondata['os_class'])
        asset_obs = models.Assets.objects.filter(assets_id__in=jsondata['asset_ids'])
        os_ob=models.OS.objects.get(os_id=jsondata['id'])
        os_ob.asset_id.remove(*os_ob.asset_id.all())
        os_ob.asset_id.add(*asset_obs)
    except:
        return {'result':0}
    else:
        return {'result':1}

def delassetfclasss(jsondata):
    models.AssetFClass.objects.filter(assetfclass_id__in=jsondata['rows']).delete()
    return {'result':1}

def addassetfclass(jsondata):
    try:
        models.AssetFClass.objects.create(name=jsondata['name'],remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changeassetfclass(jsondata):
    try:
        models.AssetFClass.objects.filter(assetfclass_id=jsondata['id']).update(name=jsondata['name'],remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}


def delassetsclasss(jsondata):
    models.AssetSClass.objects.filter(assetsclass_id__in=jsondata['rows']).delete()
    return {'result':1}

def addassetsclass(jsondata):
    try:
        asserfclass_ob = models.AssetFClass.objects.get(assetfclass_id=jsondata['asserfclass_id'])
        models.AssetSClass.objects.create(name=jsondata['name'],assetfclass_id=asserfclass_ob,remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}

def changeassetsclass(jsondata):
    try:
        asserfclass_ob=models.AssetFClass.objects.get(assetfclass_id=jsondata['asserfclass_id'])
        models.AssetSClass.objects.filter(assetsclass_id=jsondata['id']).update(name=jsondata['name'],
                                                                                assetfclass_id=asserfclass_ob,
                                                                                remarks=jsondata.get('remarks'))
    except:
        return {'result':0}
    else:
        return {'result':1}
