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
    sidePagination:'server',
    clickToSelect:true,
    url:'/pactAPI/',
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
        var seach_name=$('#seach_name').val();
        if (seach_name) {data['seach_name']=seach_name;}
        var seach_sn=$('#seach_sn').val();
        if (seach_sn) {data['seach_sn']=seach_sn;}
        return data;
    },
    columns:[
        {checkbox:true},
        {title:'名称',
        align:'center',
        valign: 'middle',
        field:'name',
        sortable:true,
        },
        {title:'合同号',
        align:'center',
        valign: 'middle',
        field:'sn',
        },
        {title:'合同总价(万)',
        align:'center',
        valign: 'middle',
        field:'price',
        },
        {title:'合同文件',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {
            if (row['file_path']){var a='<a href="'+row['file_path']+'">合同下载</a>'}
            else {var a='-'}
            return a
        }
        },
        {title:'备注',
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
        },
        {title:'操作',
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
    $('#j-title').text('新增合同');
    $('#info_handle').text('新增');
});


$('.close').click(function () {
        $('.showdisplay').removeClass('showdisplay');
});

$('#info_del').click(function () {
    var rows=$('#list_table').bootstrapTable('getSelections');
    var data=[];
    for (var i in rows) {data.push(rows[i]['id']);}
    $.ajax({
        url:'/pacthandleAPI/?method=del',
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
    var name=$('#j-name').val();
    var pactsn=$('#j-pactsn').val();
    var price=$('#j-price').val();
    var remarks=$('#j-remarks').val();
    if (!name) {$('.form_warning').text('合同名称不能为空！')}
    else {
        if (pactsn){
            var senddata={'name':name,'sn':pactsn};
            var tmpfile=$('#uploadfilepath')[0].files;
            if (tmpfile.length){var uploadresult=uploadFile(tmpfile[0]);
            senddata['file_path']=uploadresult}
            if (!senddata['file_path']){
                var oldfilepath=$('#filepath').html();
                if (oldfilepath){senddata['file_path']=oldfilepath}
            }
            if (price){senddata['price']=price}
            if (remarks){senddata['remarks']=remarks}
            if (infoid){senddata['id']=infoid}
            $.ajax({
            url:'/pacthandleAPI/?method='+handle,
            contentType:'application/json;charset=utf-8',
            data:JSON.stringify(senddata),
            type:'post',
            success:function (res) {
                if (res['result']){
                    $('.showdisplay').removeClass('showdisplay');
                    $('#list_table').bootstrapTable('refresh');

                }else {
                    if (handle=='add'){$('.form_warning').text('添加合同失败！')}
                    else {$('.form_warning').text('修改合同失败！')}
                }
            }});
            }else {$('.form_warning').text('合同号不能为空！')}
    }
}


function changeinfo(index) {
    initform();
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('修改合同信息');
    $('#info_handle').text('提交修改');
    $('#j-name').val(rowdata['name']);
    $('#j-oldid').val(rowdata['id']);
    $('#j-pactsn').val(rowdata['sn']);
    $('#j-price').val(rowdata['price']);
    if (rowdata['file_path']){$('#filepath').html(rowdata['file_path'])}
    $('#j-remarks').val(rowdata['remarks']);
}

function initform() {
    $('.addchangeform').find('input').val('');
    $('.addchangeform').find('select').val('-1');
    $('.form_warning').text('');
    $('#filepath').html('');
}



