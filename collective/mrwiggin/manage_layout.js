var timeout    = 500;
var closetimer = 0;
var ddmenuitem = 0;

function portlet_menu_open() {
   portlet_menu_canceltimer();
   portlet_menu_close();
   ddmenuitem = jq(this.parentNode).find('ul').css('visibility', 'visible');
}
function portlet_menu_close() {
  if(ddmenuitem) ddmenuitem.css('visibility', 'hidden');
}
function portlet_menu_timer() {
  closetimer = window.setTimeout(portlet_menu_close, timeout);
}
function portlet_menu_canceltimer() {
  if(closetimer) {
    window.clearTimeout(closetimer);
    closetimer = null;
  }
}

jq(document).ready(function() {
  jq('.mrwiggin .portlet_add').bind('mouseover', portlet_menu_open);
  jq('.mrwiggin .portlet_add').bind('mouseout',  portlet_menu_timer);
});
document.onclick = portlet_menu_close;
