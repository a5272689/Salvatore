/**
 * Created by root on 7/22/16.
 */
function initheight() {
    $('.rightcharts').css('width',$('.body_headfoot').width()-550);
    $(window).resize(function(){
        var oldwidth=$('.rightcharts').css('width');
        var newwidth=$('.body_headfoot').width()-550+'px';
        if (oldwidth!=newwidth){
            $('.rightcharts').css('width',newwidth);
            allobchart();
        }
    });
}
initheight();
fclasschart();
allobchart();
idcchart();
function fclasschart() {
    var indexchart = echarts.init($('#index_chart')[0]);
    var indexchartoption = {
        title:{
            show:true,
            text:'分类资产情况',
            textAlign: 'center',
            left:'50%'
        },
        color:['#f45b5b','#c4ccd3','#91e8e1','#2b908f','#e4d354','#f7a35c','#434348','#7cb5ec',  '#90ed7d',  '#8085e9','#f15c80',     ],
        tooltip: {
            trigger: 'item',
            formatter: "{a}:{b}<br/>含{c}个资产 占{d}%"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:[]
        },
        series: [
            {
                name:'一级分类',
                type:'pie',
                radius: ['55%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[]
            }
        ]
            };
    $.ajax({
        url:'/fclasschartAPI/',
        async:false,
        success:function (res) {
            indexchartoption.legend.data=res.name;
            indexchartoption.series[0].data=res.value;
        }
    });
    indexchart.setOption(indexchartoption);
}

function idcchart() {
    var indexchart = echarts.init($('#idc_chart')[0]);
    var indexchartoption = {
        title:{
            show:true,
            text:'IDC资产情况',
            textAlign: 'center',
            left:'50%'
        },
        color:['#2b908f','#e4d354','#f7a35c','#434348','#7cb5ec',  '#90ed7d',  '#8085e9','#f15c80',   '#f45b5b', '#91e8e1', '#c4ccd3'],
        tooltip: {
            trigger: 'item',
            formatter: "{a}:{b}<br/>含{c}个资产 占{d}%"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:[]
        },
        series: [
            {
                name:'IDC',
                type:'pie',
                radius: ['55%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[]
            }
        ]
            };
    $.ajax({
        url:'/idcchartAPI/',
        async:false,
        success:function (res) {
            indexchartoption.legend.data=res.name;
            indexchartoption.series[0].data=res.value;
        }
    });
    indexchart.setOption(indexchartoption);
}

function allobchart() {
    var indexchart = echarts.init($('#allob_chart')[0]);
    var indexchartoption = {
    title:{
        show:true,
        text:'资产及资产部件数量情况',
        textAlign: 'center',
        left:'50%'
    },
    tooltip: {},
    legend: {
        data:['数量'],
        right:'15%',
        top:'10%'
    },
    color:['#f7a35c','#434348','#7cb5ec',  '#90ed7d',  '#8085e9','#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1', '#c4ccd3'],
    xAxis: {
        data: ['资产','CPU','内存','硬盘','网络端口','其他部件','操作系统','应用程序','数据库','中间件']
    },
    yAxis: {},
    series: [{
        name: '数量',
        type: 'bar',
        data: []
    }]
    };
    $.ajax({
        url:'/allobchartAPI/',
        async:false,
        success:function (res) {
            indexchartoption.series[0].data=res.num;
        }
    });
    indexchart.setOption(indexchartoption);
}