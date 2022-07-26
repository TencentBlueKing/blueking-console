/*
 * 获取桌面app list，通过宣传链接打开app
 * 应用没有添加则跳转到应用市场应用详细页面
 */
$(function(){
	// 通过链接打开应用，如果没有添加该应用，则打开应用市场页面.
	var app_code = "",
		app_url = "",
		search_str = window.location.search,
		params = search_str.substring(1).split("&");
	for(var i=0; i<params.length; i++){
		var	param = params[i].split("=");
		// 默认打开某个app
		if(param[0]=="app"){
			app_code = params[i].replace("app=", "");
		}
		// 打开app的某个页面(如果为空，则打开app的首页). 注意，这里的url，如果是比较复杂的，则一定要进行utf-8编码(可以使用encodeURIComponent()进行编码)
		if(param[0]=="url"){
			app_url = decodeURIComponent(params[i].replace("url=", ""));
		}
	}
	if(app_code){
		// 如果是系统应用（码头应用），则直接打开系统应用
		if(BLUEKING.api.is_tool_app(app_code)){
			switch(app_code){
				case 'market':
					BLUEKING.window.create_market(app_url);
					break;
				case 'app_statistics':
					BLUEKING.window.create_app_statistics(app_url);
					break;
				case 'user_center':
					BLUEKING.window.create_user_center(app_url);
					break;
			}
		}else{
			// 打开该app（没有添加该应用则需要先给用户添加应用再打开）
			BLUEKING.api.open_app_by_desk(app_code, app_url);
		}
	}
});
