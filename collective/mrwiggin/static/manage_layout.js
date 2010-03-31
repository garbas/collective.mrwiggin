var expose_options = {
  lazy: true,
  closeOnClick: false,
  closeOnEsc: false,
  color: '#78c',
  opacity: 0.5,
  api: true }

var overlay_options = {
  top: 100, 
  expose: {
    loadSpeed: 100
  }, 
  oneInstance: false,  
  closeOnClick: false, 
  api: true }


jq(document).ready(function() {
  jq('.portlets-manager-rendered').each(function() {
    jq(this).expose(expose_options).load();
    jq(this).click(function() {
      jq(jq(this).attr('rel')).overlay(overlay_options).load();
      return false;
    });
  });
});
