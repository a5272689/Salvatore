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
    url:'/rackAPI/',
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
        var seach_roomid=Number($('#seach_roomid').val());
        if (seach_roomid!=-1){data['seach_roomid']=seach_roomid;}
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
        {title:'所在IDC',
        align:'center',
        valign: 'middle',
        formatter:function (value,row,index) {return roomdic[row['roomid']]['name']},
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
        responseHandler:function (data) {
            roomdic=data['roomdic']
            var roomselectlist='<option value="-1">请选择所在机房</option>';
            for (var i in data['roomdic']){
                roomselectlist=roomselectlist+'<option value="'+i+'">'+data['roomdic'][i]['name']+'</option>'
            }
            if($('#seach_roomid').val()=='-1'){$('#seach_roomid').html(roomselectlist)}
            $('#j-roomid').html(roomselectlist)
            return data
        },
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
    $('#j-title').text('新增机架');
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
        url:'/rackhandleAPI/?method=del',
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
    var roomid=$('#j-roomid').val();
    var remarks=$('#j-remarks').val();
    if (!name) {$('.form_warning').text('机架名称不能为空！')}
    else {
        if(roomid!='-1'&&roomid){
            var senddata={'name':name,'roomid':roomid};
            if (remarks){senddata['remarks']=remarks}
            if (infoid){senddata['id']=infoid}
            $.ajax({
            url:'/rackhandleAPI/?method='+handle,
            contentType:'application/json;charset=utf-8',
            data:JSON.stringify(senddata),
            type:'post',
            success:function (res) {
                if (res['result']){
                    $('.showdisplay').removeClass('showdisplay');
                    $('#list_table').bootstrapTable('refresh');
                }else {
                    if (handle=='add'){$('.form_warning').text('添加机架失败！')}
                    else {$('.form_warning').text('修改机架失败！')}
                }
            }});
        }else {$('.form_warning').text('IDC不能为空！')}

    }
}
function changeinfo(index) {
    initform();
    var rowdata=$('#list_table').bootstrapTable('getData')[index];
    $('.fullscreendiv').addClass('showdisplay');
    $('#j-title').text('修改机架信息');
    $('#info_handle').text('提交修改');
    $('#j-name').val(rowdata['name']);
    $('#j-oldid').val(rowdata['id']);
    $('#j-roomid').val(rowdata['roomid']);
    $('#j-remarks').val(rowdata['remarks']);
}

function initform() {
    $('.addchangeform').find('input').val('');
    $('.addchangeform').find('select').val('-1');
    $('.form_warning').text('');
}


