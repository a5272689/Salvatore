/**
 * Created by root on 7/5/16.
 */
function table_height() {
    var tmpheight=$(window).height()-160;
    if (tmpheight>250) {return tmpheight} else {return 250};
};
function tabledate() {
    return {
    height:table_height(),
    striped:true,
    pagination:true,
    pageNumber:1,
    pageSize:20,
    pageList:[20,30,50],
    sidePagination:'server',
    url:'/diskAPI/',
    method:'post',
    queryParams:function(params) {
        var data =  {
            rows:params.limit,
            page:Math.ceil(params.offset/params.limit+1) || 1,
        };
        if (params.sort){
            data['sort']=params.sort;
            data['order']=params.order;
        };
        var seach_model=$('#seach_model').val();
        if (seach_model) {data['seach_model']=seach_model;}
        return data;
    },
    responseHandler:function (res) {
        assetdic=res.assetdic;
        return res
    },
    columns:[
        {checkbox:true},
        {title:'硬盘型号',
        align:'center',
        valign: 'middle',
        field:'model',
        sortable:true,
        },{title:'所在资产',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {
            return assetdic[row.asset_id]
        }
        },{title:'序列号',
        align:'center',
        valign: 'middle',
        field:'sn'
        },{title:'容量 GB',
        align:'center',
        valign: 'middle',
        field:'capacity'
        },{title:'硬盘类型',
        align:'center',
        valign: 'middle',
        field:'type'
        },{title:'转速',
        align:'center',
        valign: 'middle',
        field:'nowspeed'
        },{title:'槽位',
        align:'center',
        valign: 'middle',
        field:'slot'
        },{title:'厂家',
        align:'center',
        valign: 'middle',
        field:'manufactor'
        },{title:'接口',
        align:'center',
        valign: 'middle',
        field:'interface'
        },{title:'备注',
        align:'center',
        valign: 'middle',
        field:'remarks',
        },{title:'创建时间',
        align:'center',
        valign: 'middle',
        field:'create_date',
        },{title:'最后修改时间',
        align:'center',
        valign: 'middle',
        field:'update_date',
        },{title:'操作',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {
            var change='<button type="button" class="btn btn-default btn-xs" onclick="changeinfo('+index+')">修改</button>';
            return change
        }
        },
    ],
    }
};


$('#list_table').bootstrapTable(tabledate());

$(window).resize(function () {
    $('#list_table').bootstrapTable('resetView', {height:table_height()});
});
$('#list_check').click(function () {
    $('#list_table').bootstrapTable('refresh');
});
$('#info_add').click(function () {
    initform();
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('新增硬盘');
    $('#info_handle').text('新增');
    // console.log(businessdic)
    // $('#j-SBusiness').
});


$('.close').click(function () {
        $('.showdisplay').removeClass('showdisplay');
});

$('#info_del').click(function () {
    var rows=$('#list_table').bootstrapTable('getSelections');
    var data=[];
    for (var i in rows) {data.push(rows[i]['id']);}
    $.ajax({
        url:'/diskhandleAPI/?method=del',
        contentType:'application/json;charset=utf-8',
        data:JSON.stringify({'rows':data}),
        type:'post',
        success:function (res) {
            $('#list_table').bootstrapTable('refresh');
        }
    });
});

$('#info_handle').click(function () {
    if ($('#info_handle').text()=='新增'){infohandle('add')}
    else {infohandle('change',$('#j-oldid').val())}
});

function uploadFile(file) {
        var formData = new FormData();
        formData.append("UploadFile",file);
        var uploadresult;
        $.ajax({
            url: '/upload/',
            type: 'post',
            async: false,
            data: formData,
            processData: false,
            contentType: false,
            mimeType: 'multipart/form-data',
            success: function (data) {
                uploadresult=data;
            }
        });
        return JSON.parse(uploadresult)['filepath']
    }

function infohandle(handle,infoid) {
    var model=$('#j-model').val();
    var sn=$('#j-sn').val();
    var capacity=Number($('#j-capacity').val());
    var remarks=$('#j-remarks').val();
    var nowspeed=Number($('#j-nowspeed').val());
    var slot=$('#j-slot').val();
    var manufactor=$('#j-manufactor').val();
    var asset_id=Number($('#j-asset_id').val());
    var diskinterface=$('#j-interface').val();
    var disktype=$('#j-type').val();
    if (!model) {$('.form_warning').text('硬盘型号不能为空！');return}
    if(!capacity){$('.form_warning').text('硬盘容量不能为空,且必须为数字！');return}
    var senddata={'model':model,'capacity':capacity};
    if(nowspeed){senddata['nowspeed']=nowspeed}
    if(sn){senddata['sn']=sn}
    if(slot){senddata['slot']=slot}
    if (diskinterface){senddata['interface']=diskinterface}
    if (disktype){senddata['type']=disktype}
    if (remarks){senddata['remarks']=remarks}
    if(asset_id!='-1'){senddata['asset_id']=asset_id}
    if(manufactor){senddata['manufactor']=manufactor}
    if (infoid){senddata['id']=infoid}
    $.ajax({
    url:'/diskhandleAPI/?method='+handle,
    contentType:'application/json;charset=utf-8',
    data:JSON.stringify(senddata),
    type:'post',
    success:function (res) {
        if (res['result']){
            $('.showdisplay').removeClass('showdisplay');
            $('#list_table').bootstrapTable('refresh');

        }else {
            if (handle=='add'){$('.form_warning').text('添加硬盘失败！')}
            else {$('.form_warning').text('修改硬盘失败！')}
        }
    }});

}


function changeinfo(index) {
    initform();
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('修改硬盘信息');
    $('#info_handle').text('提交修改');
    $('#j-oldid').val(rowdata['id']);
    $('#j-model').val(rowdata['model']);
    $('#j-sn').val(rowdata['sn']);
    $('#j-capacity').val(rowdata['capacity']);
    $('#j-interface').val(rowdata['interface']);
    $('#j-nowspeed').val(rowdata['nowspeed']);
    $('#j-slot').val(rowdata['slot']);
    $('#j-manufactor').val(rowdata['manufactor']);
    $('#j-remarks').val(rowdata['remarks']);
    if(rowdata['type']){$('#j-type').val(rowdata['type']);}
    if(rowdata['asset_id']){$('#j-asset_id').val(rowdata['asset_id']);}
    else {$('#j-asset_id').val('-1')}
}

function initform() {
    $('.addchangeform').find('input').val('');
    $('.addchangeform').find('select').val('-1');
    $('#j-type').val('机械硬盘');
    $('.form_warning').text('');
}
function initassetselect() {
    $.ajax({
    url:'/assetlistAPI/?method=alllist',
    contentType:'application/json;charset=utf-8',
    type:'post',
    success:function (res) {
        var str = '<option value="-1">请选择</option>';
        for (var i in res['rows']){
        str+='<option value="'+res['rows'][i]['id']+'">'+res['rows'][i]['id']+' 资产:'+res['rows'][i]['name']+'</option>';
        }
        $('#j-asset_id').html(str)
    }})
}
initassetselect();



