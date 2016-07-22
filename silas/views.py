# -*- coding:utf-8 -*-
#author:hjd
from django.shortcuts import render,render_to_response
from django.http import JsonResponse,HttpResponse
from silas import models,form
from django.db.models import Q
import json,time
from silas import utils
from Salvatore.settings import UploadDir
# Create your views here.

# 文件上传
def upload(request):
    result={'filepath':None}
    if request.method == "POST":
        uf = form.FileForm(request.POST,request.FILES)
        if uf.is_valid():
            #获取表单信息
            headImg = uf.cleaned_data.get('UploadFile')
            if headImg:
                filepath = '%s/%s_%s' % (UploadDir,int(time.time()), headImg.name,)
                with open(filepath, mode='wb') as file:
                    for i in headImg.chunks():
                        file.write(i)
                file.close()
                result['filepath']='/%s' % (filepath)
    return JsonResponse(result)

def fclasschartAPI(request):
    fclass_obs=models.AssetFClass.objects.all()
    fclass_list=[]
    fclass_count=[]
    for fclass_ob in fclass_obs:
        fclass_list.append(fclass_ob.name)
        fclass_count.append({'value':models.Assets.objects.filter(assetsclass_id__assetfclass_id=fclass_ob).count(),'name':fclass_ob.name})
    return JsonResponse({'name':fclass_list,'value':fclass_count})

def idcchartAPI(request):
    room_obs=models.Room.objects.all()
    room_list=[]
    room_count=[]
    for room_ob in room_obs:
        room_list.append(room_ob.name)
        room_count.append({
            'value':models.Assets.objects.filter(seat__seat_room=room_ob).count(),
            'name':room_ob.name
        })
    return JsonResponse({'name': room_list, 'value': room_count})

def allobchartAPI(request):
    assetnum=models.Assets.objects.all().count()
    cpunum=models.CPU.objects.all().count()
    memnum=models.MEM.objects.all().count()
    disknum=models.Disk.objects.all().count()
    netnum=models.Net.objects.all().count()
    otherpartnum=models.OtherPart.objects.all().count()
    osnum=models.OS.objects.all().count()
    appnum=models.App.objects.all().count()
    databasenum=models.Database.objects.all().count()
    middlewarenum=models.Middleware.objects.all().count()
    return JsonResponse({'num':[assetnum,cpunum,memnum,disknum,netnum,otherpartnum,osnum,appnum,databasenum,middlewarenum]})

def assetlistAPI(request):
    getmethod=request.GET.get('method')
    if getmethod=='alllist':
        assets_obs=models.Assets.objects.all().order_by('assets_id')
        assetslist=[]
        for assets_ob in assets_obs:
            assetslist.append({
                'id':assets_ob.assets_id,
                'name':assets_ob.name
            })
    else:
        if request.body:
            requestdata = json.loads(request.body)
        else:
            requestdata = {}
        q = Q()
        page = requestdata.get('page', 1)
        rows = requestdata.get('rows', 20)
        if 'seach_name' in requestdata:
            q = Q(name__contains=requestdata['seach_name'])
        if 'seach_sn' in requestdata:
            q = q.add(Q(sn__contains=requestdata['seach_sn']),'AND')
        if 'seach_assetsclass' in requestdata:
            assetsclass_ob=models.AssetSClass.objects.get(assetsclass_id=requestdata['seach_assetsclass'])
            q=q.add(Q(assetsclass_id=assetsclass_ob),'AND')
        elif 'seach_assetfclass' in requestdata:
            print requestdata['seach_assetfclass']
            print models.AssetFClass.objects.get(assetfclass_id=requestdata['seach_assetfclass'])
            assetsclass_obs=models.AssetSClass.objects.filter(
                assetfclass_id=models.AssetFClass.objects.get(assetfclass_id=requestdata['seach_assetfclass'])
            )
            q=q.add(Q(assetsclass_id__in=assetsclass_obs),'AND')
        if 'seach_seat' in requestdata:
            seat_ob=models.Seat.objects.get(seat_id=requestdata['seach_seat'])
            q=q.add(Q(seat=seat_ob),'AND')
        elif 'seach_room' in requestdata:
            seat_obs=models.Seat.objects.filter(
                seat_room=models.Room.objects.get(room_id=requestdata['seach_room'])
            )
            q=q.add(Q(seat__in=seat_obs),'AND')
        orderby = 'name'
        if 'sort' in requestdata:
            if requestdata['order'] == 'desc':
                orderby = '-name'
        assets_obs = models.Assets.objects.filter(q).order_by(orderby)
        assetslist = []
        for asset_ob in assets_obs[(page - 1) * rows:page * rows]:
            assetslist.append({
                'id':asset_ob.assets_id,'name':asset_ob.name,'assetfclass_id':asset_ob.assetsclass_id.assetfclass_id_id,
                'assetsclass_id':asset_ob.assetsclass_id_id,'manufactor':asset_ob.manufactor,'sn':asset_ob.sn,
                'business_id':asset_ob.business_id,'assets_admin_id':asset_ob.assets_admin_id,
                'room_id':asset_ob.seat.seat_room_id,'seat_id':asset_ob.seat_id,'pact_id':asset_ob.pact_id,
                'purchasing_date':asset_ob.purchasing_date,'warranty_date':asset_ob.warranty_date,
                'price':asset_ob.price,'remarks':asset_ob.remarks,'create_date':asset_ob.create_date,
                'update_date':asset_ob.update_date
            })
    return JsonResponse({'total':assets_obs.count(),'rows':assetslist,'roomdic':utils.makeroomdic(),
                         'assetclassdic':utils.makeassetclassdic(),'assetadmindic':utils.makeassetadmindic(),
                         'businessdic':utils.makebusinessdic(),'pactdic':utils.makepactdic()})

def assetHAPI(request):
    asset_ob=models.Assets.objects.get(assets_id=int(request.GET.get('asset_id')))
    cpu_obs=models.CPU.objects.filter(asset_id=asset_ob)
    mem_obs = models.MEM.objects.filter(asset_id=asset_ob)
    disk_obs = models.Disk.objects.filter(asset_id=asset_ob)
    net_obs = models.Net.objects.filter(asset_id=asset_ob)
    otherpart_obs = models.OtherPart.objects.filter(asset_id=asset_ob)
    result={'cpu':{'num':0,'corenum':0,'rows':[]},'mem':{'num':0,'capacity':0,'rows':[]},
            'disk':{'num':0,'capacity':0,'rows':[]},'net':{'num':0,'rows':[]},'otherpart':{'num':0,'rows':[]}}
    for cpu_ob in cpu_obs:
        result['cpu']['num']+=1
        result['cpu']['corenum'] += cpu_ob.corenum
        result['cpu']['rows'].append({'id':cpu_ob.CPU_id,'model':cpu_ob.model,'manufactor':cpu_ob.manufactor,
                               'sn':cpu_ob.sn,'nowspeed':cpu_ob.nowspeed,'slot':cpu_ob.slot,
                               'asset_id':cpu_ob.asset_id_id,'corenum':cpu_ob.corenum,
                               'remarks':cpu_ob.remarks,'create_date':cpu_ob.create_date,
                               'update_date':cpu_ob.update_date})
    for mem_ob in mem_obs:
        result['mem']['num']+=1
        result['mem']['capacity']+=mem_ob.capacity
        result['mem']['rows'].append({'id':mem_ob.MEM_id,'model':mem_ob.model,'manufactor':mem_ob.manufactor,
                               'sn':mem_ob.sn,'nowspeed':mem_ob.nowspeed,'slot':mem_ob.slot,
                               'asset_id':mem_ob.asset_id_id,'capacity':mem_ob.capacity,
                               'remarks':mem_ob.remarks,'create_date':mem_ob.create_date,
                               'update_date':mem_ob.update_date,'interface':mem_ob.interface})
    for disk_ob in disk_obs:
        result['disk']['num'] += 1
        result['disk']['capacity'] += disk_ob.capacity
        result['disk']['rows'].append({'id':disk_ob.disk_id,'model':disk_ob.model,'manufactor':disk_ob.manufactor,
                               'sn':disk_ob.sn,'nowspeed':disk_ob.nowspeed,'slot':disk_ob.slot,
                               'asset_id':disk_ob.asset_id_id,'capacity':disk_ob.capacity,
                               'remarks':disk_ob.remarks,'create_date':disk_ob.create_date,
                               'type':disk_ob.type,
                               'update_date':disk_ob.update_date,'interface':disk_ob.interface})
    for net_ob in net_obs:
        result['net']['num'] += 1
        result['net']['rows'].append({'id':net_ob.net_id,'model':net_ob.model,'manufactor':net_ob.manufactor,
                               'sn':net_ob.sn,'nowspeed':net_ob.nowspeed,'name':net_ob.name,
                               'asset_id':net_ob.asset_id_id,'mac':net_ob.mac,
                               'remarks':net_ob.remarks,'create_date':net_ob.create_date,
                               'update_date':net_ob.update_date,'ip':net_ob.ip})
    for otherpart_ob in otherpart_obs:
        result['otherpart']['num'] += 1
        result['otherpart']['rows'].append({'id':otherpart_ob.other_part_id,'model':otherpart_ob.model,'manufactor':otherpart_ob.manufactor,
                               'sn':otherpart_ob.sn,'name':otherpart_ob.name,'asset_id':otherpart_ob.asset_id_id,
                               'remarks':otherpart_ob.remarks,'create_date':otherpart_ob.create_date,
                               'update_date':otherpart_ob.update_date})
    return JsonResponse(result)

def assetSAPI(request):
    asset_ob=models.Assets.objects.get(assets_id=int(request.GET.get('asset_id')))
    os_obs=asset_ob.os_set.all()
    app_obs=asset_ob.app_set.all()
    database_obs=asset_ob.database_set.all()
    middleware_obs=asset_ob.middleware_set.all()
    os_class_dic={}
    bit_dic={}
    for i in models.OS.os_class_dic:
        os_class_dic[i[0]]=i[1]
    for i in models.OS.bit_dic:
        bit_dic[i[0]]=i[1]
    result={'os':{'num':0,'rows':[],'bit_dic':bit_dic,'os_class_dic':os_class_dic},
            'app':{'num':0,'rows':[]},'database':{'num':0,'rows':[]},'middleware':{'num':0,'rows':[]}}
    for os_ob in os_obs:
        result['os']['num']+=1
        result['os']['rows'].append({'id':os_ob.os_id,'os_class':os_ob.os_class,'version':os_ob.version,
                               'bit':os_ob.bit,
                               'remarks':os_ob.remarks,'create_date':os_ob.create_date,
                               'update_date':os_ob.update_date})

    for app_ob in app_obs:
        result['app']['num'] += 1
        result['app']['rows'].append({'id':app_ob.app_id,'name':app_ob.name,'version':app_ob.version,
                               'port':app_ob.port,'language':app_ob.language,
                               'remarks':app_ob.remarks,'create_date':app_ob.create_date,
                               'update_date':app_ob.update_date})
    for database_ob in database_obs:
        result['database']['num'] += 1
        result['database']['rows'].append({'id':database_ob.database_id,'name':database_ob.name,'version':database_ob.version,
                               'port':database_ob.port,
                               'remarks':database_ob.remarks,'create_date':database_ob.create_date,
                               'update_date':database_ob.update_date})
    for middleware_ob in middleware_obs:
        result['middleware']['num'] += 1
        result['middleware']['rows'].append({'id':middleware_ob.middleware_id,'name':middleware_ob.name,'version':middleware_ob.version,
                               'port':middleware_ob.port,
                               'remarks':middleware_ob.remarks,'create_date':middleware_ob.create_date,
                               'update_date':middleware_ob.update_date})
    print result
    return JsonResponse(result)

def nullHAPI(request):
    cpu_obs=models.CPU.objects.filter(asset_id__isnull=True)
    mem_obs = models.MEM.objects.filter(asset_id__isnull=True)
    disk_obs = models.Disk.objects.filter(asset_id__isnull=True)
    net_obs = models.Net.objects.filter(asset_id__isnull=True)
    otherpart_obs = models.OtherPart.objects.filter(asset_id__isnull=True)
    result={'cpu':{},'mem':{},'disk':{},'net':{},'otherpart':{}}
    for cpu_ob in cpu_obs:
        result['cpu'][cpu_ob.CPU_id]={'model':cpu_ob.model,
                               'sn':cpu_ob.sn}
    for mem_ob in mem_obs:
        result['mem'][mem_ob.MEM_id]={'model':mem_ob.model,
                               'sn':mem_ob.sn}
    for disk_ob in disk_obs:
        result['disk'][disk_ob.disk_id]={'model':disk_ob.model,
                               'sn':disk_ob.sn}
    for net_ob in net_obs:
        result['net'][net_ob.net_id]={'model':net_ob.model,
                               'sn':net_ob.sn,'name':net_ob.name}
    for otherpart_ob in otherpart_obs:
        result['otherpart'][otherpart_ob.other_part_id]={'model':otherpart_ob.model,
                               'sn':otherpart_ob.sn,'name':otherpart_ob.name}
    return JsonResponse(result)

def SoftAPI(request):
    os_obs=models.OS.objects.all()
    app_obs=models.App.objects.all()
    database_obs=models.Database.objects.all()
    middleware_obs=models.Middleware.objects.all()
    os_class_dic={}
    bit_dic={}
    for i in models.OS.os_class_dic:
        os_class_dic[i[0]]=i[1]
    for i in models.OS.bit_dic:
        bit_dic[i[0]]=i[1]
    result={'os':{},'app':{},'database':{},'middleware':{}}
    for os_ob in os_obs:
        result['os'][os_ob.os_id]={'os_class':os_class_dic[os_ob.os_class],'version':os_ob.version,'bit':bit_dic[os_ob.bit]}
    for app_ob in app_obs:
        result['app'][app_ob.app_id]={'name':app_ob.name,'version':app_ob.version,'port':app_ob.port,'language':app_ob.language}
    for database_ob in database_obs:
        result['database'][database_ob.database_id]={'name':database_ob.name,'version':database_ob.version,'port':database_ob.port}
    for middleware_ob in middleware_obs:
        result['middleware'][middleware_ob.middleware_id]={'name':middleware_ob.name,'version':middleware_ob.version,'port':middleware_ob.port}
    return JsonResponse(result)

def assethandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delassets,'add':utils.addasset,'change':utils.changeasset}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def assetadminAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    assetadmins=models.AssetsAdmin.objects.filter(q)
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    assetadmins = assetadmins.order_by(orderby)
    result={'total':assetadmins.count(),'rows':[]}
    for assetadmin in assetadmins:
        result['rows'].append({
            'name':assetadmin.name,'qq':assetadmin.qq,'tel':assetadmin.tel,
            'email':assetadmin.email,'remarks':assetadmin.remarks,'id':assetadmin.assets_admin_id,
            'create_date':assetadmin.create_date,'update_date':assetadmin.update_date
        })
    return JsonResponse(result)

def assetadminhandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delassetadmins,'add':utils.addassetadmins,'change':utils.changeassetadmins}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def roomAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    rooms=models.Room.objects.filter(q)
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    rooms = rooms.order_by(orderby)
    result={'total':rooms.count(),'rows':[]}
    for room_ob in rooms:
        result['rows'].append({'id':room_ob.room_id,'name':room_ob.name,
                               'qq':room_ob.qq,'tel':room_ob.tel,
                                'email':room_ob.email,'idcadmin':room_ob.idcadmin,
                               'remarks':room_ob.remarks,'create_date':room_ob.create_date,
                               'update_date':room_ob.update_date})
    return JsonResponse(result)

def roomhandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delrooms,'add':utils.addroom,'change':utils.changeroom}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def pactAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=q.add(Q(name__contains=requestdata['seach_name']), 'AND')
    if 'seach_sn' in requestdata:
        q=q.add(Q(sn__contains=requestdata['seach_sn']), 'AND')
    pacts=models.Pact.objects.filter(q)
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    pacts = pacts.order_by(orderby)
    result={'total':pacts.count(),'rows':[]}
    for pact_ob in pacts:
        result['rows'].append({'id':pact_ob.pacr_id,'name':pact_ob.name,
                               'sn':pact_ob.sn,'price':pact_ob.price,
                                'file_path':pact_ob.file_path,
                               'remarks':pact_ob.remarks,'create_date':pact_ob.create_date,
                               'update_date':pact_ob.update_date})
    return JsonResponse(result)

def pacthandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delpacts,'add':utils.addpact,'change':utils.changepact}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def rackAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    if 'seach_roomid' in requestdata:
        room_ob=models.Room.objects.filter(room_id=requestdata['seach_roomid'])
        q.add(Q(seat_room=room_ob),'AND')
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    seats = models.Seat.objects.filter(q).order_by(orderby)
    result={'total':seats.count(),'rows':[]}
    for seat_ob in seats:
        result['rows'].append({'id':seat_ob.seat_id,'name':seat_ob.name,
                               'roomid':seat_ob.seat_room_id,
                               'remarks':seat_ob.remarks,'create_date':seat_ob.create_date,
                               'update_date':seat_ob.update_date})
    result['roomdic']=utils.makeroomdic()
    return JsonResponse(result)

def rackhandleAPI(request):
    themethod=request.GET.get('method')
    print themethod,json.loads(request.body)
    methoddic={'del':utils.delracks,'add':utils.addrack,'change':utils.changerack}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def businessAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    business_obs = models.Business.objects.filter(q).order_by(orderby)
    result={'total':business_obs.count(),'rows':[]}
    for business_ob in business_obs:
        result['rows'].append({'id':business_ob.business_id,'name':business_ob.name,
                               'SBusinessid':business_ob.superior_business_id,
                               'remarks':business_ob.remarks,'create_date':business_ob.create_date,
                               'update_date':business_ob.update_date})
    result['businessdic']=utils.makebusinessdic()
    return JsonResponse(result)

def businesshandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delbusinesss,'add':utils.addbusiness,'change':utils.changebusiness}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def cpuAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_model' in requestdata:
        q=Q(model__contains=requestdata['seach_model'])
    orderby='model'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-model'
    cpu_obs = models.CPU.objects.filter(q).order_by(orderby)
    result={'total':cpu_obs.count(),'rows':[],'assetdic':{}}
    for cpu_ob in cpu_obs[(page-1)*rows:page*rows]:
        if cpu_ob.asset_id_id:
            result['assetdic'][cpu_ob.asset_id_id]=cpu_ob.asset_id.name
        result['rows'].append({'id':cpu_ob.CPU_id,'model':cpu_ob.model,'manufactor':cpu_ob.manufactor,
                               'sn':cpu_ob.sn,'nowspeed':cpu_ob.nowspeed,'slot':cpu_ob.slot,
                               'asset_id':cpu_ob.asset_id_id,'corenum':cpu_ob.corenum,
                               'remarks':cpu_ob.remarks,'create_date':cpu_ob.create_date,
                               'update_date':cpu_ob.update_date})
    return JsonResponse(result)

def cpuhandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delcpus,'add':utils.addcpu,'change':utils.changecpu}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def memAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_model' in requestdata:
        q=Q(model__contains=requestdata['seach_model'])
    orderby='model'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-model'
    mem_obs = models.MEM.objects.filter(q).order_by(orderby)
    result={'total':mem_obs.count(),'rows':[],'assetdic':{}}
    for mem_ob in mem_obs[(page-1)*rows:page*rows]:
        if mem_ob.asset_id_id:
            result['assetdic'][mem_ob.asset_id_id]=mem_ob.asset_id.name
        result['rows'].append({'id':mem_ob.MEM_id,'model':mem_ob.model,'manufactor':mem_ob.manufactor,
                               'sn':mem_ob.sn,'nowspeed':mem_ob.nowspeed,'slot':mem_ob.slot,
                               'asset_id':mem_ob.asset_id_id,'capacity':mem_ob.capacity,
                               'remarks':mem_ob.remarks,'create_date':mem_ob.create_date,
                               'update_date':mem_ob.update_date,'interface':mem_ob.interface})
    return JsonResponse(result)

def memhandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delmems,'add':utils.addmem,'change':utils.changemem}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def diskAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_model' in requestdata:
        q=Q(model__contains=requestdata['seach_model'])
    orderby='model'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-model'
    disk_obs = models.Disk.objects.filter(q).order_by(orderby)
    result={'total':disk_obs.count(),'rows':[],'assetdic':{}}
    for disk_ob in disk_obs[(page-1)*rows:page*rows]:
        if disk_ob.asset_id_id:
            result['assetdic'][disk_ob.asset_id_id]=disk_ob.asset_id.name
        result['rows'].append({'id':disk_ob.disk_id,'model':disk_ob.model,'manufactor':disk_ob.manufactor,
                               'sn':disk_ob.sn,'nowspeed':disk_ob.nowspeed,'slot':disk_ob.slot,
                               'asset_id':disk_ob.asset_id_id,'capacity':disk_ob.capacity,
                               'remarks':disk_ob.remarks,'create_date':disk_ob.create_date,
                               'type':disk_ob.type,
                               'update_date':disk_ob.update_date,'interface':disk_ob.interface})
    return JsonResponse(result)

def diskhandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.deldisks,'add':utils.adddisk,'change':utils.changedisk}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def netAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_model' in requestdata:
        q=Q(model__contains=requestdata['seach_model'])
    orderby='model'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-model'
    net_obs = models.Net.objects.filter(q).order_by(orderby)
    result={'total':net_obs.count(),'rows':[],'assetdic':{}}
    for net_ob in net_obs[(page-1)*rows:page*rows]:
        if net_ob.asset_id_id:
            result['assetdic'][net_ob.asset_id_id]=net_ob.asset_id.name
        result['rows'].append({'id':net_ob.net_id,'model':net_ob.model,'manufactor':net_ob.manufactor,
                               'sn':net_ob.sn,'nowspeed':net_ob.nowspeed,'name':net_ob.name,
                               'asset_id':net_ob.asset_id_id,'mac':net_ob.mac,
                               'remarks':net_ob.remarks,'create_date':net_ob.create_date,
                               'update_date':net_ob.update_date,'ip':net_ob.ip})
    return JsonResponse(result)

def nethandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delnets,'add':utils.addnet,'change':utils.changenet}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def otherpartAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_model' in requestdata:
        q=Q(model__contains=requestdata['seach_model'])
    orderby='model'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-model'
    otherpart_obs = models.OtherPart.objects.filter(q).order_by(orderby)
    result={'total':otherpart_obs.count(),'rows':[],'assetdic':{}}
    for otherpart_ob in otherpart_obs[(page-1)*rows:page*rows]:
        if otherpart_ob.asset_id_id:
            result['assetdic'][otherpart_ob.asset_id_id]=otherpart_ob.asset_id.name
        result['rows'].append({'id':otherpart_ob.other_part_id,'model':otherpart_ob.model,'manufactor':otherpart_ob.manufactor,
                               'sn':otherpart_ob.sn,'name':otherpart_ob.name,'asset_id':otherpart_ob.asset_id_id,
                               'remarks':otherpart_ob.remarks,'create_date':otherpart_ob.create_date,
                               'update_date':otherpart_ob.update_date})
    return JsonResponse(result)

def otherparthandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delotherparts,'add':utils.addotherpart,'change':utils.changeotherpart}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def databaseAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    database_obs = models.Database.objects.filter(q).order_by(orderby)
    result={'total':database_obs.count(),'rows':[],'assetdic':{}}
    for database_ob in database_obs[(page-1)*rows:page*rows]:
        asset_obs=database_ob.asset_id.all()
        tmpassetlist=[]
        for asset_ob in asset_obs:
            tmpassetlist.append(asset_ob.assets_id)
            result['assetdic'][asset_ob.assets_id]=asset_ob.name
        result['rows'].append({'id':database_ob.database_id,'name':database_ob.name,'version':database_ob.version,
                               'port':database_ob.port,'asset_ids':tmpassetlist,
                               'remarks':database_ob.remarks,'create_date':database_ob.create_date,
                               'update_date':database_ob.update_date})
    return JsonResponse(result)

def databasehandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.deldatabases,'add':utils.adddatabase,'change':utils.changedatabase}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def middlewareAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    middleware_obs = models.Middleware.objects.filter(q).order_by(orderby)
    result={'total':middleware_obs.count(),'rows':[],'assetdic':{}}
    for middleware_ob in middleware_obs[(page-1)*rows:page*rows]:
        asset_obs=middleware_ob.asset_id.all()
        tmpassetlist=[]
        for asset_ob in asset_obs:
            tmpassetlist.append(asset_ob.assets_id)
            result['assetdic'][asset_ob.assets_id]=asset_ob.name
        result['rows'].append({'id':middleware_ob.middleware_id,'name':middleware_ob.name,'version':middleware_ob.version,
                               'port':middleware_ob.port,'asset_ids':tmpassetlist,
                               'remarks':middleware_ob.remarks,'create_date':middleware_ob.create_date,
                               'update_date':middleware_ob.update_date})
    return JsonResponse(result)

def middlewarehandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delmiddlewares,'add':utils.addmiddleware,'change':utils.changemiddleware}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def appAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    app_obs = models.App.objects.filter(q).order_by(orderby)
    result={'total':app_obs.count(),'rows':[],'assetdic':{}}
    for app_ob in app_obs[(page-1)*rows:page*rows]:
        asset_obs=app_ob.asset_id.all()
        tmpassetlist=[]
        for asset_ob in asset_obs:
            tmpassetlist.append(asset_ob.assets_id)
            result['assetdic'][asset_ob.assets_id]=asset_ob.name
        result['rows'].append({'id':app_ob.app_id,'name':app_ob.name,'version':app_ob.version,
                               'port':app_ob.port,'asset_ids':tmpassetlist,'language':app_ob.language,
                               'remarks':app_ob.remarks,'create_date':app_ob.create_date,
                               'update_date':app_ob.update_date})
    return JsonResponse(result)

def apphandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delapps,'add':utils.addapp,'change':utils.changeapp}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def osAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    page=requestdata.get('page',1)
    rows=requestdata.get('rows',20)
    if 'seach_os_class' in requestdata:
        q=Q(os_class=requestdata['seach_os_class'])
    if 'seach_version' in requestdata:
        q=q.add(Q(version__contains=requestdata['seach_version']),'AND')
    orderby='version'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-version'
    os_obs = models.OS.objects.filter(q).order_by(orderby)
    os_class_dic={}
    bit_dic={}
    print q
    for i in models.OS.os_class_dic:
        os_class_dic[i[0]]=i[1]
    for i in models.OS.bit_dic:
        bit_dic[i[0]]=i[1]
    result={'total':os_obs.count(),'rows':[],'assetdic':{},'bit_dic':bit_dic,'os_class_dic':os_class_dic}
    for os_ob in os_obs[(page-1)*rows:page*rows]:
        asset_obs=os_ob.asset_id.all()
        tmpassetlist=[]
        for asset_ob in asset_obs:
            tmpassetlist.append(asset_ob.assets_id)
            result['assetdic'][asset_ob.assets_id]=asset_ob.name
        result['rows'].append({'id':os_ob.os_id,'os_class':os_ob.os_class,'version':os_ob.version,
                               'bit':os_ob.bit,'asset_ids':tmpassetlist,
                               'remarks':os_ob.remarks,'create_date':os_ob.create_date,
                               'update_date':os_ob.update_date})
    return JsonResponse(result)

def oshandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.deloss,'add':utils.addos,'change':utils.changeos}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def assetfclassAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    assetfclass_obs = models.AssetFClass.objects.filter(q).order_by(orderby)
    result={'total':assetfclass_obs.count(),'rows':[]}
    for assetfclass_ob in assetfclass_obs:
        result['rows'].append({'id':assetfclass_ob.assetfclass_id,'name':assetfclass_ob.name,'remarks':assetfclass_ob.remarks})
    return JsonResponse(result)

def assetfclasshandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delassetfclasss,'add':utils.addassetfclass,'change':utils.changeassetfclass}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def assetsclassAPI(request):
    if request.body:
        requestdata=json.loads(request.body)
    else:
        requestdata = {}
    q=Q()
    if 'seach_name' in requestdata:
        q=Q(name__contains=requestdata['seach_name'])
    if 'seach_assetfclass' in requestdata:
        assetfclass_ob=models.AssetFClass.objects.get(assetfclass_id=requestdata['seach_assetfclass'])
        if assetfclass_ob:
            q=q.add(Q(assetfclass_id=assetfclass_ob),'AND')
    orderby='name'
    if 'sort' in requestdata:
        if requestdata['order']=='desc':
            orderby='-name'
    assetsclass_obs = models.AssetSClass.objects.filter(q).order_by(orderby)
    result={'total':assetsclass_obs.count(),'rows':[],'assetclassdic':utils.makeassetclassdic()}
    for assetsclass_ob in assetsclass_obs:
        result['rows'].append({'id':assetsclass_ob.assetsclass_id,'name':assetsclass_ob.name,'assetfclass_id':assetsclass_ob.assetfclass_id_id,'remarks':assetsclass_ob.remarks})
    return JsonResponse(result)

def assetsclasshandleAPI(request):
    themethod=request.GET.get('method')
    methoddic={'del':utils.delassetsclasss,'add':utils.addassetsclass,'change':utils.changeassetsclass}
    result=methoddic[themethod](json.loads(request.body))
    return JsonResponse(result)

def index(request):
    return render_to_response('index.html',{'title':'首页','index':True})

def assetlist(request):
    data={'title': '资产管理', 'asset':True}
    dataflag=request.GET.get('dataflag')
    if dataflag:
        data['data_flag']=dataflag
        data['data_flagid']=request.GET.get('dataflagid')
    return render_to_response('assetlist.html',data )

def assetadmin(request):
    return render_to_response('others/assetadminlist.html', {'title': '资产管理员管理', 'others':True})

def room(request):
    return render_to_response('others/roomlist.html', {'title': 'IDC管理', 'others':True})

def pact(request):
    return render_to_response('others/pactlist.html', {'title': '合同管理', 'others':True})

def seat(request):
    return render_to_response('others/seatlist.html', {'title': '机架管理', 'others':True})

def business(request):
    return render_to_response('others/businesslist.html', {'title': '业务线管理', 'others':True})

def CPU(request):
    return render_to_response('parts/cpulist.html', {'title': 'CPU管理','parts':True})

def MEM(request):
    return render_to_response('parts/memlist.html', {'title': '内存管理','parts':True})

def disk(request):
    return render_to_response('parts/disklist.html', {'title': '磁盘管理','parts':True})

def net(request):
    return render_to_response('parts/netlist.html', {'title': '网络端口管理','parts':True})

def otherpart(request):
    return render_to_response('parts/otherpartlist.html', {'title': '其它部件管理','parts':True})

def database(request):
    return render_to_response('parts/databaselist.html', {'title': '数据库管理','parts':True})

def middleware(request):
    return render_to_response('parts/middlewarelist.html', {'title': '中间件管理','parts':True})

def app(request):
    return render_to_response('parts/applist.html', {'title': '应用管理','parts':True})

def OS(request):
    return render_to_response('parts/oslist.html', {'title': '操作系统管理','parts':True})

def assetfclass(request):
    return render_to_response('others/assetfclasslist.html', {'title': '资产一级分类管理', 'others':True})

def assetsclass(request):
    return render_to_response('others/assetsclasslist.html', {'title': '资产二级分类管理', 'others':True})
