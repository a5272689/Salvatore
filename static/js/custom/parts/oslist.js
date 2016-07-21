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
    url:'/osAPI/',
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
        var seach_version=$('#seach_version').val();
        if (seach_version) {data['seach_version']=seach_version;}
        var seach_os_class=$('#seach_os_class').val();
        if (seach_os_class!='-1'){data['seach_os_class']=seach_os_class;}
        return data;
    },
    responseHandler:function (res) {
        assetdic=res.assetdic;
        os_class_dic=res.os_class_dic;
        bit_dic=res.bit_dic;
        if($('#seach_os_class').val()=='-1'){$('#seach_os_class').html(makeselectoptionforseach(os_class_dic));}
        $('#j-os_class').html(makeselectoptionforseach(os_class_dic));
        $('#j-bit').html(makeselectoptionforseach(bit_dic))
        return res
    },
    columns:[
        {checkbox:true},
        {title:'操作系统版本',
        align:'center',
        valign: 'middle',
        field:'version',
        sortable:true,
        },{title:'所在资产',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {
            var assetnamelist=[]
            for (var i in row['asset_ids']){
                assetnamelist.push(assetdic[row['asset_ids'][i]])
            }
            return assetnamelist.join(',')
        }
        },{title:'操作系统大类',
        align:'center',
        valign: 'middle',
        field:'os_class'
        },{title:'位数',
        align:'center',
        valign: 'middle',
        field:'bit'
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
    $('#j-title').text('新增操作系统');
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
        url:'/oshandleAPI/?method=del',
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
    var version=$('#j-version').val();
    var os_class=$('#j-os_class').val();
    var bit=$('#j-bit').val();
    var language=$('#j-language').val();
    var remarks=$('#j-remarks').val();
    var asset_ids=$('#j-asset_ids').val();
    if(os_class=='-1'){$('.form_warning').text('操作系统分类不能为空！');return}
    if (!version) {$('.form_warning').text('操作系统版本不能为空！');return}
    if (bit=='-1') {$('.form_warning').text('操作系统位数不能为空！');return}
    var senddata={'bit':bit,'os_class':os_class,'version':version};
    if (remarks){senddata['remarks']=remarks}
    var newasset_ids=[];
    for (var i in asset_ids){
        if ((asset_ids[i]!='-1')&&(Number(asset_ids[i]))){newasset_ids.push(Number(asset_ids[i]))}
    }
    senddata['asset_ids']=newasset_ids;
    if (infoid){senddata['id']=infoid}
    $.ajax({
    url:'/oshandleAPI/?method='+handle,
    contentType:'application/json;charset=utf-8',
    data:JSON.stringify(senddata),
    type:'post',
    success:function (res) {
        if (res['result']){
            $('.showdisplay').removeClass('showdisplay');
            $('#list_table').bootstrapTable('refresh');

        }else {
            if (handle=='add'){$('.form_warning').text('添加操作系统失败！')}
            else {$('.form_warning').text('修改操作系统失败！')}
        }
    }});

}


function changeinfo(index) {
    initform();
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('修改操作系统信息');
    $('#info_handle').text('提交修改');
    $('#j-oldid').val(rowdata['id']);
    $('#j-version').val(rowdata['version']);
    $('#j-bit').val(rowdata['bit']);
    $('#j-os_class').val(rowdata['os_class']);
    $('#j-remarks').val(rowdata['remarks']);
    if(rowdata['asset_ids']){$('#j-asset_ids').val(rowdata['asset_ids']);}
    else {$('#j-asset_ids').val('-1')}
}

function initform() {
    $('.addchangeform').find('input').val('');
    $('.addchangeform').find('select').val('-1');
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
        $('#j-asset_ids').html(str)
    }})
}
initassetselect();



