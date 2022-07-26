var timeout_event;

// 查询绑定状态
function get_bind_status(){
	$.get(site_url + 'user_center/weixin/get_bind_status/', function(res){
		if(res.result){
			$("#bind_action").html('<a href="#unbind_weixin" role="button" class="btn-control other_operate" data-toggle="modal">' + gettext('解绑微信') + '</a>');
			$("#bind_weixin").modal("hide");
		}else{
			timeout_event = setTimeout("get_bind_status()", 1500);
		}
	});
}

//异步加载微信二维码
$("#bind_weixin").on('show.bs.modal', function(){
	$("#code_content").html('<img class="loading_img" src="' + static_url + 'user_center/img/loading_2_36x36.gif">')
	$.getJSON(site_url + "user_center/weixin/mp/get_qrcode/", function(res) {
		if(res.result){
			$("#code_content").html('<img class="code_img" src="' + res.url + '">');
			get_bind_status();
		}else{
			$("#code_content").html('<span class="code_img_error">' + res.message + '</span>');
		}
	});
})

$("#bind_weixin").on('hidden.bs.modal', function(){
	clearTimeout(timeout_event);
})