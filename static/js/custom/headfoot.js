/**
 * Created by goldd on 7/4/16.
 */


// $(document).ready(initheight());
function initheight() {
  $('.body_headfoot').css('height',$(window).height()-81);
  $('.fullscreendiv').css('height',$(window).height());
  // $('#totaldiv').css('min-height',$(window).height());
  $(window).resize(function(){
    $('.body_headfoot').css('height',$(window).height()-81);
    $('.fullscreendiv').css('height',$(window).height());
  });

  $('#dropdown_parts').dropdown();
  $('#dropdown_others').dropdown();
}
initheight();

function makeselectoption(dataob) {
  var str = '<option value="-1">请选择</option>';
  for (var i in dataob){
    str+='<option value="'+i+'">'+i+' '+dataob[i]['name']+'</option>';
  }
  return str
}
function makeselectoptionforseach(dataob) {
  var str = '<option value="-1">请选择</option>';
  for (var i in dataob){
    str+='<option value="'+i+'">'+dataob[i]+'</option>';
  }
  return str
}


