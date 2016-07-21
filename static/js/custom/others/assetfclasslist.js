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
    url:'/assetfclassAPI/',
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
        if (seach_name) {data['seach_name']=seach_name;};
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
        {title:'备注',
        align:'center',
        valign: 'middle',
        field:'remarks',
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
    $('#j-title').text('新增一级分类');
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
        url:'/assetfclasshandleAPI/?method=del',
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

function infohandle(handle,infoid) {
    var name=$('#j-name').val();
    var remarks=$('#j-remarks').val();
    if (!name) {$('.form_warning').text('一级分类名称不能为空！')}
    else {
            var senddata={'name':name};
            if (remarks){senddata['remarks']=remarks}
            if (infoid){senddata['id']=infoid}
            $.ajax({
            url:'/assetfclasshandleAPI/?method='+handle,
            contentType:'application/json;charset=utf-8',
            data:JSON.stringify(senddata),
            type:'post',
            success:function (res) {
                if (res['result']){
                    $('.showdisplay').removeClass('showdisplay');
                    $('#list_table').bootstrapTable('refresh');

                }else {
                    if (handle=='add'){$('.form_warning').text('添加一级分类失败！')}
                    else {$('.form_warning').text('修改一级分类失败！')}
                }
            }});
    }
}
function changeinfo(index) {
    initform();
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('修改一级分类信息');
    $('#info_handle').text('提交修改');
    $('#j-name').val(rowdata['name']);
    $('#j-oldid').val(rowdata['id']);
    $('#j-remarks').val(rowdata['remarks']);
}


function initform() {
    $('.addchangeform').find('input').val('');
    $('.addchangeform').find('select').val('-1');
    $('.form_warning').text('');
}



