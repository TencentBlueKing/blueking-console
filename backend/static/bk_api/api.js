// 蓝鲸平台前端API
var Bk_api = {
	/*
	 * 在app内打开其他app
	 * @param app_code: 要打开的app code
	 * @param app_url：想要打开的页面链接
	 * @param refresh_tips: 是否刷新页面
	 * @example: ('ccquery', 'http://paas.bking.com/o/ccquery/query_module_if_info/') or  ('ccquery', '/query_module_if_info/')
	 */
	open_other_app: function(app_code, app_url, refresh_tips){
		try{
			// 仅同域名下才可调用成功
			// window.top.BLUEKING.api.open_app_by_other(app_code, app_url, refresh_tips);
			// 支持跨域
			var data = {action: 'open_other_app', app_code: app_code, app_url: app_url, refresh_tips: refresh_tips};
			window.top.postMessage(JSON.stringify(data), '*');
		}catch(err){
			if(err.name != 'TypeError'){
				console.log('error_msg：' + err.message);
			}
		}
	},
}
