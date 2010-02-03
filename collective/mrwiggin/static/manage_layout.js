var tmp;
jq(document).ready(function() {
  jq('.mrwiggin').mouseover(function(){
    tmp = jq(this).find('.portlets_actions');
    tmp.css('display', 'block');
  });
  jq('.mrwiggin').mouseleave(function(){
    tmp = jq(this).find('.portlets_actions');
    tmp.css('display', 'none');
  });
  jq('.mrwiggin .portlets_actions').mouseleave(function(){
    this.css('display', 'none');
  });

  jq('.mrwiggin .button_add>div').click(function(){
    tmp = jq(this.parentNode).find('ul');
    if (tmp.css('display') == 'block') {
      tmp.css('display', 'none');
    } else {
      tmp.css('display', 'block');
    }
  });
});
