var timeout_event;
var execute_cnt = 0;
// 查询绑定状态
function get_bind_status(){
    execute_cnt += 1;
	$.get(site_url + 'user_center/weixin/get_bind_status/', function(res){
		if(res.result){
			$("#bind_action").html('<a href="#unbind_weixin" role="button" class="btn-control other_operate" data-toggle="modal">' + gettext('解绑微信') + '</a>');
		}else{
		    // 小于半个小时，就间隔1.5秒查询，大于则以 （execute_cnt-120）* 1.5秒查询
            var execute_time = 1500;
		    if(execute_cnt > 120){
                execute_time = (execute_cnt - 120) * 1500;
            }
			timeout_event = setTimeout("get_bind_status()", execute_time);
		}
	});
}

$("#bind_weixin").on('click', function(){
    clearTimeout(timeout_event);
    execute_cnt = 0;
    // 后台请求登录URL
    $.ajax({
        method: "get",
        dataType: "json",
        url: site_url + 'user_center/weixin/qy/get_login_url/',
        async: false,
        success: function (res) {
            if (res.result) {
                window.open(res.url, '_blank');
                get_bind_status();
            }
        }
    });
});