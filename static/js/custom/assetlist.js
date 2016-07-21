/**
 * Created by root on 7/5/16.
 */
function table_height() {
    var tmpheight=$(window).height()-145;
    if (tmpheight>250) {return tmpheight} else {return 250};
};
function tabledate() {
    return {
    height:table_height(),
    striped:true,
    pagination:true,
    pageNumber:1,
    pageSize:20,
    pageList:[10,15,20,30,50],
    sidePagination:'server',
    url:'/assetlistAPI/',
    method:'post',
    showColumns:true,
    toolbar:'#toolbar',
    queryParams:function(params) {
        var data =  {
            rows:params.limit,
            page:Math.ceil(params.offset/params.limit+1) || 1,
        };
        if (params.sort){
            data['sort']=params.sort;
            data['order']=params.order;
        };
        var name=$('#seach_name').val();
        if (name) {data['seach_name']=name;}
        var sn=$('#seach_sn').val();
        if (sn) {data['seach_sn']=sn;}
        var assetfclass=Number($('#seach_assetfclass').val());
        if (assetfclass!=-1) {data['seach_assetfclass']=assetfclass;}
        var assetsclass=Number($('#seach_assetsclass').val());
        if (assetsclass!=-1) {data['seach_assetsclass']=assetsclass;}
        var room=Number($('#seach_room').val());
        if (room!=-1) {data['seach_room']=room;}
        var seat=Number($('#seach_seat').val());
        if (seat!=-1) {data['seach_seat']=seat;}
        return data;
    },
    responseHandler:function(res) {
        roomdic=res['roomdic'];
        assetclassdic=res['assetclassdic'];
        assetadmindic=res['assetadmindic'];
        businessdic=res['businessdic'];
        pactdic=res['pactdic'];
        if($('#seach_room').val()=='-1'){$('#seach_room').html(makeoption(roomdic));}
        if($('#seach_assetfclass').val()=='-1'){$('#seach_assetfclass').html(makeoption(assetclassdic));}
        return res;
    },
    columns:[
        {
            checkbox:true
        },{
            title:'资产名称',
            align:'center',
            valign: 'middle',
            field:'name',
            sortable:true,
        },{
            title:'资产序列号',
            align:'center',
            valign: 'middle',
            field:'sn'
        },{
            title:'资产一级分类',
            align:'center',
            valign: 'middle',
            formatter:function (value,row,index) {
                return assetclassdic[row['assetfclass_id']]['name']
            }
        },{
            title:'资产二级分类',
            align:'center',
            valign: 'middle',
            formatter:function (value,row,index) {
                return assetclassdic[row['assetfclass_id']]['assetsclasss'][row['assetsclass_id']]
            }
        },{
            title:'生产厂家',
            align:'center',
            valign: 'middle',
            field:'manufactor'
        },{
            title:'业务线',
            align:'center',
            valign: 'middle',
            field:'business_id',
            formatter:function (value,row,index) {
                if (row['business_id']){return businessdic[row['business_id']]['name']}
                else {return '-'}
            }
        },{
            title:'管理员',
            align:'center',
            valign: 'middle',
            formatter:function (value,row,index) {
                if (row['assets_admin_id']){return assetadmindic[row['assets_admin_id']]['name']}
                else {return '-'}
            }
        },{
            title:'IDC',
            align:'center',
            valign: 'middle',
            formatter:function (value,row,index) {
                if (row['room_id']){return roomdic[row['room_id']]['name']}
                else {return '-'}
            }
        },{
            title:'机架',
            align:'center',
            valign: 'middle',
            formatter:function (value,row,index) {
                if(row['seat_id']){return roomdic[row['room_id']]['seats'][row['seat_id']]}
                else {return '-'}
            }
        },{
            title:'合同',
            align:'center',
            valign: 'middle',
            field:'pact_id',
            formatter:function (value,row,index) {
                if(row['pact_id']){return pactdic[row['pact_id']]['name']}
                else {return '-'}
            }
        },{
            title:'价格',
            align:'center',
            valign: 'middle',
            field:'price'
        },{
            title:'购买日期',
            align:'center',
            valign: 'middle',
            field:'purchasing_date'
        },{
            title:'出保日期',
            align:'center',
            valign: 'middle',
            field:'warranty_date'
        },{
            title:'备注',
            align:'center',
            valign: 'middle',
            field:'remarks'
        },{
            title:'创建日期',
            align:'center',
            valign: 'middle',
            field:'create_date'
        },{
            title:'最近修改日期',
            align:'center',
            valign: 'middle',
            field:'update_date'
        },{title:'操作',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {
            var detail='<button type="button" class="btn btn-primary btn-xs" onclick="lookinfo('+index+')">详情</button>';
            var change='<button type="button" class="btn btn-default btn-xs" onclick="changeinfo('+index+')">修改</button>';
            return detail+change
        }
        }
    ],
    }
};


$('#list_table').bootstrapTable(tabledate());

$(window).resize(function () {
    $('#list_table').bootstrapTable('resetView', {height:table_height()});
});
$('#assetlist_check').click(function () {
    $('#list_table').bootstrapTable('refresh');
});

$('.close').click(function () {
        $('.fullscreendiv').removeClass('showdisplay');
});

$('#info_del').click(function () {
    var rows=$('#list_table').bootstrapTable('getSelections');
    var data=[];
    for (var i in rows) {data.push(rows[i]['id']);}
    $.ajax({
        url:'/assethandleAPI/?method=del',
        contentType:'application/json;charset=utf-8',
        data:JSON.stringify({'rows':data}),
        type:'post',
        success:function (res) {
            $('#list_table').bootstrapTable('refresh');
        }
    });
});


$('.tabs_leftpadding').on('click', 'a', function(){

    var $this = $(this),
        cat = $this.data('cat'),
        index=Number($('#detailinfo_index').val());
    $('li.activetabs').removeAttr('class');
    $('#'+cat).addClass('active activetabs');
    if(cat=='baseinfo'){lookinfo(index)}
    if(cat=='softinfo'){looksoft(index)}
    if(cat=='hardwareinfo'){lookhardware(index)}
});


function makeoption(dic) {
        var newstr='<option value="-1">请选择</option>\n';
        for (var key in dic) {newstr=newstr+'<option value="'+key+'">'+dic[key]['name']+'</option>\n';}
        return newstr
}

$('#seach_room').change(function () {
    var seach_room=Number($('#seach_room').val());
    var newoption='<option value="-1">请选择</option>\n';
    if (seach_room!='-1'){
        for(var key in roomdic[seach_room].seats){
            newoption=newoption+'<option value="'+key+'">'+roomdic[seach_room].seats[key]+'</option>\n'
        }
    }
    $('#seach_seat').html(newoption)
});



$('#seach_assetfclass').change(function () {
    var seach_assetfclass=Number($('#seach_assetfclass').val());
    var newoption='<option value="-1">请选择</option>\n';
    if (seach_assetfclass!='-1'){
        for(var key in assetclassdic[seach_assetfclass].assetsclasss){
            newoption=newoption+'<option value="'+key+'">'+assetclassdic[seach_assetfclass].assetsclasss[key]+'</option>\n'
        }
    }
    $('#seach_assetsclass').html(newoption)
});

function changeinfo(index) {
    $('#j-title').text('修改资产信息');
    $('#info_handle').text('提交修改');
    $('#detaildiv').attr('style','display: none');
    $('#handlediv').attr('style','display: block');
    $('.modal-footer').attr('style','display: block');
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');

}

$('#info_add').click(function () {
    $('#j-title').text('新增资产信息');
    $('#info_handle').text('新增');
    $('#detaildiv').attr('style','display: none');
    $('#handlediv').attr('style','display: block');
    $('.modal-footer').attr('style','display: block');
    $('.fullscreendiv').addClass('showdisplay');
});

function lookhardware(index) {
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $.ajax({
        url:'/assetHAPI/',
        data:{'asset_id':rowdata['id']},
        type:'get',
        success:function (res) {
            var newstr='';
            if (res.cpu.num){
                newstr=newstr+'<h4>CPU信息 总CPU个数:'+res.cpu['num']+' 总核数:'+res.cpu['corenum']+' </h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>CPU型号</th><th>序列号</th><th>核心数</th><th>主频 GHz</th><th>槽位</th><th>厂家</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.cpu.rows){
                    var sn=res.cpu.rows[i].sn||'-',
                        slot=res.cpu.rows[i].slot||'-',
                        manufactor=res.cpu.rows[i].manufactor||'-',
                        remarks=res.cpu.rows[i].remarks||'-';
                    newstr+='<tr>'+
                        '<td>'+res.cpu.rows[i].model+'</td>'+
                        '<td>'+sn+'</td>'+
                        '<td>'+res.cpu.rows[i].corenum+'</td>'+
                        '<td>'+res.cpu.rows[i].nowspeed+'</td>'+
                        '<td>'+slot+'</td>'+
                        '<td>'+manufactor+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.mem.num){
                newstr=newstr+'<h4>内存信息 总内存片数:'+res.mem['num']+' 总内存空间:'+res.mem['capacity']+'GB </h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>内存型号</th><th>序列号</th><th>容量 GB</th><th>主频 MHz</th><th>槽位</th><th>接口</th><th>厂家</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.mem.rows){
                    var sn=res.mem.rows[i].sn||'-',
                        slot=res.mem.rows[i].slot||'-',
                        manufactor=res.mem.rows[i].manufactor||'-',
                        remarks=res.mem.rows[i].remarks||'-',
                        interface=res.mem.rows[i].interface||'-',
                        nowspeed=res.mem.rows[i].nowspeed||'-';
                    newstr+='<tr>'+
                        '<td>'+res.mem.rows[i].model+'</td>'+
                        '<td>'+sn+'</td>'+
                        '<td>'+res.mem.rows[i].capacity+'</td>'+
                        '<td>'+nowspeed+'</td>'+
                        '<td>'+slot+'</td>'+
                        '<td>'+interface+'</td>'+
                        '<td>'+manufactor+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.disk.num){
                newstr=newstr+'<h4>硬盘信息 总硬盘个数:'+res.disk['num']+' 总硬盘空间:'+res.disk['capacity']+'GB </h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>硬盘型号</th><th>序列号</th><th>容量 GB</th><th>硬盘类型</th><th>转速</th><th>槽位</th><th>接口</th><th>厂家</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.disk.rows){
                    var sn=res.disk.rows[i].sn||'-',
                        slot=res.disk.rows[i].slot||'-',
                        manufactor=res.disk.rows[i].manufactor||'-',
                        remarks=res.disk.rows[i].remarks||'-',
                        interface=res.disk.rows[i].interface||'-',
                        nowspeed=res.disk.rows[i].nowspeed||'-';
                    newstr+='<tr>'+
                        '<td>'+res.disk.rows[i].model+'</td>'+
                        '<td>'+sn+'</td>'+
                        '<td>'+res.disk.rows[i].capacity+'</td>'+
                        '<td>'+res.disk.rows[i].type+'</td>'+
                        '<td>'+nowspeed+'</td>'+
                        '<td>'+slot+'</td>'+
                        '<td>'+interface+'</td>'+
                        '<td>'+manufactor+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.net.num){
                newstr=newstr+'<h4>网络端口信息 总网络端口个数:'+res.net['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>网络端口型号</th><th>序列号</th><th>名称</th><th>MAC地址</th><th>IP地址</th><th>传输速率 Mbp</th><th>厂家</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.net.rows){
                    var sn=res.net.rows[i].sn||'-',
                        name=res.net.rows[i].name||'-',
                        mac=res.net.rows[i].mac||'-',
                        ip=res.net.rows[i].ip||'-',
                        manufactor=res.net.rows[i].manufactor||'-',
                        remarks=res.net.rows[i].remarks||'-',
                        nowspeed=res.net.rows[i].nowspeed||'-';
                    newstr+='<tr>'+
                        '<td>'+res.net.rows[i].model+'</td>'+
                        '<td>'+sn+'</td>'+
                        '<td>'+name+'</td>'+
                        '<td>'+mac+'</td>'+
                        '<td>'+ip+'</td>'+
                        '<td>'+nowspeed+'</td>'+
                        '<td>'+manufactor+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.otherpart.num){
                newstr=newstr+'<h4>其他部件信息 总其他部件个数:'+res.otherpart['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>其他部件型号</th><th>序列号</th><th>名称</th><th>厂家</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.net.rows){
                    var sn=res.otherpart.rows[i].sn||'-',
                        name=res.otherpart.rows[i].name||'-',
                        manufactor=res.otherpart.rows[i].manufactor||'-',
                        remarks=res.otherpart.rows[i].remarks||'-',
                        nowspeed=res.otherpart.rows[i].nowspeed||'-';
                    newstr+='<tr>'+
                        '<td>'+res.otherpart.rows[i].model+'</td>'+
                        '<td>'+sn+'</td>'+
                        '<td>'+name+'</td>'+
                        '<td>'+manufactor+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            $('.detailinfo').html(newstr)
        }
    });
}

function looksoft(index) {
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $.ajax({
        url:'/assetSAPI/',
        data:{'asset_id':rowdata['id']},
        type:'get',
        success:function (res) {
            var newstr='';
            if(res.os.num){
                newstr=newstr+'<h4>操作系统信息 操作系统个数:'+res.os['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>操作系统版本</th><th>操作系统大类</th><th>位数</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.os.rows){
                    var remarks=res.os.rows[i].remarks||'-';
                    newstr+='<tr>'+
                        '<td>'+res.os.rows[i].version+'</td>'+
                        '<td>'+res.os.os_class_dic[res.os.rows[i].os_class]+'</td>'+
                        '<td>'+res.os.bit_dic[res.os.rows[i].bit]+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.app.num){
                newstr=newstr+'<h4>应用程序信息 应用程序个数:'+res.app['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>应用程序名称</th><th>应用程序版本</th><th>端口</th><th>开发语言</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.app.rows){
                    var remarks=res.app.rows[i].remarks||'-',
                        version=res.app.rows[i].version||'-',
                        port=res.app.rows[i].port||'-',
                        language=res.app.rows[i].language||'-';
                    newstr+='<tr>'+
                        '<td>'+res.app.rows[i].name+'</td>'+
                        '<td>'+version+'</td>'+
                        '<td>'+port+'</td>'+
                        '<td>'+language+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.database.num){
                newstr=newstr+'<h4>数据库信息 数据库个数:'+res.database['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>数据库名称</th><th>数据库版本</th><th>端口</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.database.rows){
                    var remarks=res.database.rows[i].remarks||'-',
                        version=res.database.rows[i].version||'-',
                        port=res.database.rows[i].port||'-';
                    newstr+='<tr>'+
                        '<td>'+res.database.rows[i].name+'</td>'+
                        '<td>'+version+'</td>'+
                        '<td>'+port+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            if(res.middleware.num){
                newstr=newstr+'<h4>中间件信息 中间件个数:'+res.middleware['num']+'</h4>';
                newstr=newstr+'<table id="customtable" class="table table-bordered table-condensed"><thead><tr><th>中间件名称</th><th>中间件版本</th><th>端口</th><th>备注</th></tr></thead><tbody>';
                for (var i in res.middleware.rows){
                    var remarks=res.middleware.rows[i].remarks||'-',
                        version=res.middleware.rows[i].version||'-',
                        port=res.middleware.rows[i].port||'-';
                    newstr+='<tr>'+
                        '<td>'+res.middleware.rows[i].name+'</td>'+
                        '<td>'+version+'</td>'+
                        '<td>'+port+'</td>'+
                        '<td>'+remarks+'</td>'+
                        '</tr>'
                }
                newstr+='</tbody></table>'
            }
            $('.detailinfo').html(newstr)
        }
    });
    // $('.detailinfo').html('soft')
}

function lookinfo(index) {
    $('#j-title').text('资产详情');
    $('#detaildiv').attr('style','display: block');
    $('#handlediv').attr('style','display: none');
    $('.modal-footer').attr('style','display: none');
    // initform();
    $('li.activetabs').removeAttr('class');
    $('#baseinfo').addClass('active activetabs');
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    var nowstr='<table id="table_popup" class="table table-bordered table-col-4">';
    var endstr='</table>';
    nowstr=nowstr+'<tr><th>资源编号</th><td>'+rowdata['id']+'</td><th>资源名称</th><td>'+rowdata['name']+'</td></tr>';
    nowstr=nowstr+'<tr><th>资源序列号</th><td>'+rowdata['sn']+'</td><th>生产厂家</th><td>'+rowdata['manufactor']+'</td></tr>';
    nowstr=nowstr+'<tr><th>一级分类</th><td>'+assetclassdic[rowdata['assetfclass_id']]['name']+
        '</td><th>二级分类</th><td>'+assetclassdic[rowdata['assetfclass_id']]['assetsclasss'][rowdata['assetsclass_id']]+'</td></tr>';
    if(rowdata['business_id']){
        nowstr=nowstr+'<tr><th>业务</th><td>'+businessdic[rowdata['business_id']]['name'];
        if(businessdic[rowdata['business_id']]['superior_business_id']){
            nowstr=nowstr+'</td><th>上层业务</th><td>'+businessdic[businessdic[rowdata['business_id']]['superior_business_id']]['name']+'</td></tr>';
        }
        else {nowstr=nowstr+'</td><th>上层业务</th><td>-</td></tr>';}
    }
    if(rowdata['pact_id']){
        nowstr=nowstr+'<tr><th>合同</th><td>'+pactdic[rowdata['pact_id']]['name']+
        '</td><th>合同号</th><td>'+pactdic[rowdata['pact_id']]['sn']+'</td></tr>';
        var price=pactdic[rowdata['pact_id']]['price']||'-';
        var file_path=pactdic[rowdata['pact_id']]['file_path']||'-';
        if (file_path!='-'){file_path='<a href="'+file_path+'">合同下载</a>'}
        nowstr=nowstr+'<tr><th>合同金额</th><td>'+price+'</td><th>合同文件</th><td>'+file_path+'</td></tr>';
    }
    if(rowdata['assets_admin_id']){
        nowstr=nowstr+'<tr><th>资产管理员</th><td>'+assetadmindic[rowdata['assets_admin_id']]['name']+
        '</td><th>资产管理员电话</th><td>'+assetadmindic[rowdata['assets_admin_id']]['tel']+'</td></tr>';
        var qq=assetadmindic[rowdata['assets_admin_id']]['qq']||'-';
        var email=assetadmindic[rowdata['assets_admin_id']]['email']||'-';
        nowstr=nowstr+'<tr><th>资产管理员QQ</th><td>'+qq+'</td><th>资产管理员邮箱</th><td>'+email+'</td></tr>';
    }
    if(rowdata['seat_id']){
        nowstr=nowstr+'<tr><th>IDC</th><td>'+roomdic[rowdata['room_id']]['name']+
        '</td><th>机架</th><td>'+roomdic[rowdata['room_id']]['seats'][rowdata['seat_id']]+'</td></tr>';
        var idcadmin=roomdic[rowdata['room_id']]['idcadmin'] || '-';
        var tel=roomdic[rowdata['room_id']]['tel'] || '-';
        nowstr=nowstr+'<tr><th>机房管理员</th><td>'+idcadmin+'</td><th>机房管理员电话</th><td>'+tel+'</td></tr>';
        var qq=roomdic[rowdata['room_id']]['qq'] || '-';
        var email=roomdic[rowdata['room_id']]['email']||'-';
        nowstr=nowstr+'<tr><th>机房管理员QQ</th><td>'+qq+'</td><th>机房管理员邮箱</th><td>'+email+'</td></tr>';
    }
    nowstr=nowstr+'<tr><th>价格</th><td>'+rowdata['price']+'</td><th>备注</th><td>'+rowdata['remarks']+'</td></tr>';
    nowstr=nowstr+'<tr><th>购买日期</th><td>'+rowdata['purchasing_date']+'</td><th>出保日期</th><td>'+rowdata['warranty_date']+'</td></tr>';
    nowstr=nowstr+'<tr><th>创建日期</th><td>'+rowdata['create_date']+'</td><th>最后修改日期</th><td>'+rowdata['update_date']+'</td></tr>';
    $('.detailinfo').html(nowstr+endstr);
    $('#detailinfo_index').val(index)
}