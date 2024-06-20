/*
**  基本配置信息，在其他js前引用
*/
var TEMP      = {};
var BLUEKING      = {};
var tool_apps = ["market", "app_statistics", "user_center", "bk_iam", "bk_user_manage"];
BLUEKING.CONFIG = {
    desk            : 1,        //当前显示桌面
    dockPos         : 'left',   //应用码头位置，参数有：top,left,right
    appXY           : 'x',      //图标排列方式，参数有：x,y
    appSize         : 'm',       //图标显示尺寸，参数有：s,m
    appButtonTop    : 80,       //快捷方式top初始位置
    appButtonLeft   : 20,       //快捷方式left初始位置
    windowIndexid   : 10000,    //窗口z-index初始值
    windowMinWidth  : 315,      //窗口最小宽度
    windowMinHeight : 200,       //窗口最小高度
    wallpaperState  : 1,        //1系统壁纸,2自定义壁纸,3网络壁纸
    wallpaper       : '',       //壁纸
    wallpaperType   : '',       //壁纸显示类型，参数有：tianchong,shiying,pingpu,lashen,juzhong
    wallpaperWidth  : 0,        //壁纸宽度
    wallpaperHeight : 0,         //壁纸高度
};

BLUEKING.VAR = {
    zoomLevel       : 1,
    isAppMoving     : false,    //桌面应用是否正在移动中，也就是ajax操作是否正在执行中
    dock            : [],
    desk1           : [],
    desk2           : [],
    desk3           : [],
    desk4           : [],
    desk5           : [],
    folder          : []
};

BLUEKING.DOCKTOOL_VAR = {
    startmenu_state         : false, // 鼠标是否已经在头像开始菜单上
    tool_start              : false,    //鼠标是否在头像上
    appearancement_state    : false,    //鼠标是否已经在外观设置菜单上
    tool_appearance         : false,    //鼠标是否在外观设置上
    helpsment_state         : false,    //鼠标是否已经在帮助菜单上
    tool_helps              : false,    //鼠标是否在帮助上
}

//ajax全局设置
$.ajaxSetup({
    // timeout: 8000,
    cache: false,
    statusCode: {
        // 401未授权
        401: function(xhr) {
            // 重新加载页面后跳转到登录页面，重新获取登录态
			window.top.location.reload();
        },
        // 402 权限验证不通过
        402:function(xhr){
            var _src = xhr.responseText;
            ajax_content = '<iframe name="access_control_iframe" frameborder="0" src="'+_src+'"></iframe>';
            art.dialog({id: 'bktips'}).close();
            art.dialog({
                id: 'bktips',
                title: gettext("提示"),
                lock: true,
                content: ajax_content
            });
            return;
        },
        500: function(xhr, textStatus) {
            art.dialog({id: 'bktips'}).close();
              // 异常
            art.dialog({
                id: 'bktips',
                title: gettext("提示"),
                lock: true,
                content: gettext("系统出现异常：")+textStatus+"---"+xhr.status+'===='
            });
        }
    },
});

// 核心函数
BLUEKING.corefunc = (function(){
	return {
		// 获取桌面的URL前缀
		get_urlprefix: function(){
			return '/console/';
		},
		// 获取开发者中心URL前缀
		get_dev_urlprefix: function(){
			return '/app/list/';
		},
		// 获取统计分析上报数据请求URL前缀
		get_analysis_urlprefix: function(){
			return '/console/analysis/';
		},
		// 获取蓝鲸集成平台的域名
		get_bk_host: function(){
			return window.location.host;
		},
		// 获取桌面的完整链接（区分http和https）
		get_bk_url: function(){
			var current_host = window.location.host;
			var current_protocol = window.location.protocol;
			var bk_url = current_protocol + "//" + current_host + BLUEKING.corefunc.get_urlprefix();
			return bk_url;
		},
		// 获取开发者中心完整链接
		get_dev_url: function(){
			if(bk_paas3_url){
				return bk_paas3_url;
			}

			var current_host = window.location.host;
			var current_protocol = window.location.protocol;
			var bk_url = current_protocol + "//" + current_host + BLUEKING.corefunc.get_dev_urlprefix();
			return bk_url;
		},
		// 获取应用的链接
		get_app_url: function(app_code){
			var current_host = window.location.host;
			var current_protocol = window.location.protocol;
			var app_url = current_protocol + "//" + current_host + '/o/' + app_code;
			return app_url;
		},
		// 登出URL 前缀
		get_logout_urlprefix: function(){
			return BLUEKING.corefunc.get_urlprefix() + 'accounts/logout/';
		},
		// 用户信息 前缀
		get_account_profile_urlprefix: function(){
			return '/accounts/profile/';
		},
		// 外部链接 URL
		get_external_links: function(external_name){
			var external_links = BLUEKING.corefunc.get_dev_urlprefix();
			switch(external_name){
				//社区论坛
				case 'community_forums':
					external_links = 'https://bk.tencent.com/s-mart/community/';
					break;
				//视频教程
				case 'video_course':
					external_links = 'https://ke.qq.com/course/154064#tuin=218e4713';
					break;
				// 蓝鲸 Magicbox
				case 'magicbox':
					external_links = 'https://magicbox.bk.tencent.com/';
					break;
				// 蓝鲸官网
				case 'bk_os':
					external_links = 'https://bk.tencent.com/';
					break;
				// 蓝鲸服务协议
				case 'bk_service_agreement':
					external_links = 'https://bk.tencent.com/info/#laws';
					break;
			}
			return external_links;
		}
	}
})();

// ajax 等请求的URL前缀
var urlPrefix = BLUEKING.corefunc.get_urlprefix();
// 静态文件请求URL前缀
var staticUrl = BLUEKING.corefunc.get_urlprefix() + 'static/';
// 静态文件版本号，主要用于防止缓存
var staticVersion = '0.0.1';


// 工具函数
BLUEKING.toolfunc = (function(){
	return {
		// 处理 app_logo 图片不存在的情况
		app_logo_error_handle: function(){
			var img = event.srcElement;
			img.src = staticUrl + 'img/app_logo/default.png';
			img.onerror = null; // 防止 默认图片也不存在时出现死循环情况
		},
		/**
		 * xssCheck 检查是否有xss攻击
		 * @param url 访问的url
		*/
		xssCheck: function(url){
			if(!url){
				return url;
			}
			var _url = url.toLowerCase();
			if( _url.indexOf('javascript:') != -1 ||
				_url.indexOf('vbscript:') != -1 ||
				_url.indexOf('data:') != -1 ||
				_url.indexOf('scrip:') != -1
			){
				return '';
			}else{
				url.replace(/[&<">'](?:(amp|lt|quot|gt|#39|nbsp|#\d+);)?/g, function (a, b) {
			        if(b){
			            return a;
			        }else{
			            return {
			                '<':'&lt;',
			                '&':'&amp;',
			                '"':'&quot;',
			                '>':'&gt;',
			                "'":'&#39;',
			            }[a]
			        }
			    })
				return url;
			}
		},
	}
})();

BLUEKING.api = (function(){
	return {
		/*
		 * 判断该应用是否是 工具app
		 */
		is_tool_app: function(app_code){
			if($.inArray(app_code, tool_apps) != -1){
				return true;
			}else{
				return false;
			}
		},
		/*
		 * 通过宣传链接打开应用
		 */
		open_app_by_desk: function(app_code, app_url){
			// //判断是否添加了该应用
			// var return_msg = BLUEKING.api.is_user_added_app(app_code);
			// var is_added = return_msg[0]; 			//应用是否添加（true添加、false未添加）
			// var realappid = return_msg[1];			//应用真正id
			// //打开app
			// if(is_added == false && realappid != ""){
			// 	//用户没有添加该应用则打开应用市场详细页
			// 	BLUEKING.window.create_market(realappid);
			// }else if(is_added == true){
			// 	//用户添加了该应用则打开应用
			// 	//获取app的所有信息（realappid、appid、type等）
			// 	var msg = BLUEKING.api.get_app_msg(app_code);
			// 	//判断获取应用信息是否发生异常
			// 	if(msg["error"] == "E100"){
			// 		ZENG.msgbox.show('应用不存在！', 5, 3000);
			// 	}else if(msg["error"] == "E501" || msg["error"] == "E502" || msg["error"] == "E503"){
			// 		ZENG.msgbox.show('应用加载失败，请重试', 5, 3000);
			// 	}else if(msg["error"] == "E400"){
			// 		ZENG.msgbox.show('您没有操作该应用的权限！', 5, 3000);
			// 	}else if(msg["error"] == "E200"){
			// 		ZENG.msgbox.show('应用已下架！', 5, 3000);
			// 	}else if(msg["error"] == "E300"){
			// 		ZENG.msgbox.show('应用正在开发中！', 5, 3000);
			// 	}else{
			// 		var appid = msg["appid"];
			// 		// 通过appid和app_url打开应用（判断应用类型）
			// 		BLUEKING.window.create(appid, app_url);
			// 	}
			// }else{
			// 	//应用不存在、已下架、未提测三种情况下提示信息
			// 	ZENG.msgbox.show(return_msg[2], 5, 3000);
			// }

			// 兼容 bk_cc => bk_cmdb， TODO: 后续版本将去除
			if (app_code == "bk_cc") {
				app_code = "bk_cmdb";
			}
			//获取app的所有信息（realappid、appid、type等）
			var msg = BLUEKING.api.get_app_msg(app_code);
			//判断获取应用信息是否发生异常
			if(msg["error"] == "E100"){
				ZENG.msgbox.show(gettext('应用不存在！'), 5, 3000);
			}else if(msg["error"] == "E501" || msg["error"] == "E502" || msg["error"] == "E503"){
				ZENG.msgbox.show(gettext('应用加载失败，请重试'), 5, 3000);
			}else if(msg["error"] == "E400"){
				ZENG.msgbox.show(gettext('您没有操作该应用的权限！'), 5, 3000);
			}else if(msg["error"] == "E200"){
				ZENG.msgbox.show(gettext('应用已下架！'), 5, 3000);
			}else if(msg["error"] == "E300"){
				ZENG.msgbox.show(gettext('应用正在开发中！'), 5, 3000);
			}else{
				var appid = msg["appid"];
				//通过appid和app_url打开应用
				if(!appid){   //用户添加app时，appid为用户id
					appid = app_code;//用户未添加app时，appid为app_code
					isnotadd = 1;
				}else{
					isnotadd = 0;
				}
				// 通过appid和app_url打开应用（判断应用类型）
				BLUEKING.window.create(appid, app_url, '', isnotadd);
			}
		},
		/*
		 * 其他位置通过app_code及链接打开应用
		 * 应用没有添加则桌面直接打开
		 * app_code 应用编码
		 * app_url 指定url   可选
		 * refresh_tips true：弹出框刷新提醒   可选
		 */
		open_app_by_other: function(app_code, app_url, refresh_tips){
			//判断是否是指定的系统应用
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
					case 'bk_iam':
						BLUEKING.window.create_bk_iam(app_url);
						break;
					case 'bk_user_manage':
						BLUEKING.window.create_bk_user_manage(app_url);
						break;
				}
			}else{
				// 兼容 bk_cc => bk_cmdb， TODO: 后续版本将去除
				if (app_code == "bk_cc") {
					app_code = "bk_cmdb";
				}
				//打开其他应用，获取app的信息（realappid和appid）
				var msg = BLUEKING.api.get_app_msg(app_code);
				//判断获取应用信息是否发生异常
				if(msg["error"] == "E100"){
					ZENG.msgbox.show(gettext('应用不存在！'), 5, 3000);
				}else if(msg["error"] == "E501" || msg["error"] == "E502" || msg["error"] == "E503"){
					ZENG.msgbox.show(gettext('应用加载失败，请重试'), 5, 3000);
				}else if(msg["error"] == "E400"){
					ZENG.msgbox.show(gettext('您没有操作该应用的权限！'), 5, 3000);
				}else if(msg["error"] == "E200"){
					ZENG.msgbox.show(gettext('应用已下架！'), 5, 3000);
				}else if(msg["error"] == "E300"){
					ZENG.msgbox.show(gettext('应用正在开发中！'), 5, 3000);
				}else{
					var appid = msg["appid"];
					//通过appid和app_url打开应用
					if(!appid){   //用户添加app时，appid为用户id
						appid = app_code;//用户未添加app时，appid为app_code
						isnotadd = 1;
					}else{
						isnotadd = 0;
					}
					if(refresh_tips == true){ //提醒框弹出
						BLUEKING.window.create(appid, app_url, app_code, isnotadd);
					}else{					 //提醒框不弹出
						BLUEKING.window.create(appid, app_url, '', isnotadd);
					}
				}
			}
		},
		/*
		 * 判断用户是否添加了该应用
		 */
		is_user_added_app: function(app_code){
			//判断用户是否添加了该应用
			var is_added = false;  			//初始值，默认没有添加
			var realappid = "";			 	//realappid默认为空
			var tips_msg = "应用不存在！";              //提示信息
			//请求是否添加应用返回值，和app realid
			$.ajax({
				url: urlPrefix + "is_user_added_app/" + app_code + "/",
				success: function(app){
						if(app != null){
							if(app["error"]){
								//错误信息
								is_added = false;
								realappid = "";
								if(app["error"] == "E100"){
									tips_msg = gettext("应用不存在！");
								}else if(app["error"] == "E501" || app["error"] == "E502" || app["error"] == "E503"){
									tips_msg = gettext('应用加载失败，请重试')
								}else if(app["error"] == "E400"){
									tips_msg = gettext("您没有操作该应用的权限！");
								}else if(app["error"] == "E200"){
									tips_msg = gettext("应用已下架！");
								}else if(app["error"] == "E300"){
									tips_msg = gettext("应用正在开发中！");
								}
							}else{
								//app realid信息
								is_added = app["result"]; 			//应用是否添加，true为添加，false为未添加
								realappid = app["realappid"];  		//应用真实id
							}
						}else{
							is_added = false;
							realappid = "";
							tips_msg = gettext("应用不存在！");
						}
					},
				type : "POST",
				async: false
			})
			return [is_added, realappid, tips_msg]   //返回值
		},
		/*
		 * 使用app_code查询app信息（用户未添加该应用则自动添加）
		 * return: 应用基本信息或错误信息
		*/
		get_app_msg: function(app_code){
			var msg = '';
			$.ajax({
				url: urlPrefix + 'get_my_app_by_code/' + app_code + '/',
				data: {'desk': BLUEKING.CONFIG.desk},
				success: function(app){
						if(app != null){
							if(app['error']){
								msg = {'error': app['error']}; //返回错误提示信息
							}else{
								msg = {
									appid: app['appid'],
									realappid: app['realappid'],
									url: app['url'],
									width: app['width'],
									height: app['height'],
									is_add: app['return_code'] //1：用户未添加，重新添加成功，2：用户已经添加了该应用
								};
							}
						}else{
							msg = {'error': 'E100'};
						}
					},
				type : 'GET',
				async: false
			})
			return msg;
		},
		/*
		 * 应用打开记录，用于应用的热度等指标统计
		 * return: 应用基本信息或错误信息
		*/
		app_record_by_user: function(realappid){
			$.ajax({
				type : 'POST',
				url : BLUEKING.corefunc.get_analysis_urlprefix() + 'app_record_by_user/' + realappid + '/',
				success : function(msg){}
			});
		},
	}
})();

/*
 * * 域名解析
 */
if (typeof Poly9 == 'undefined')
{
    var Poly9 = {};
}
Poly9.URLParser = function(url) {

    this._fields = {
        'Username' : 4,
        'Password' : 5,
        'Port' : 7,
        'Protocol' : 2,
        'Host' : 6,
        'Pathname' : 8,
        'URL' : 0,
        'Querystring' : 9,
        'Fragment' : 10
    };

    this._values = {};
    this._regex = null;
    this.version = 0.1;
    this._regex = /^((\w+):\/\/)?((\w+):?(\w+)?@)?([^\/\?:]+):?(\d+)?(\/?[^\?#]+)?\??([^#]+)?#?(\w*)/;
    for(var f in this._fields)
    {
        this['get' + f] = this._makeGetter(f);
    }

    if (typeof url != 'undefined')
    {
        this._parse(url);
    }
}
Poly9.URLParser.prototype.setURL = function(url) {
    this._parse(url);
}

Poly9.URLParser.prototype._initValues = function() {
    for(var f in this._fields)
    {
        this._values[f] = '';
    }
}
Poly9.URLParser.prototype._parse = function(url) {
    this._initValues();
    var r = this._regex.exec(url);
    if (!r) throw "DPURLParser::_parse -> Invalid URL";

    for(var f in this._fields) if (typeof r[this._fields[f]] != 'undefined')
    {
        this._values[f] = r[this._fields[f]];
    }
}
Poly9.URLParser.prototype._makeGetter = function(field) {
    return function() {
        return this._values[field];
    }
}


//app跨域请求console的方法使用postMessage [与static/bk_api/api.js中的方法作用一样]
window.addEventListener('message', function(event) {
    if(event.data){
        try {
            var data = JSON.parse(event.data);
            switch(data.action){
                case 'open_other_app':
                    BLUEKING.api.open_app_by_other(data.app_code, data.app_url, data.refresh_tips);
                default: //什么也不做，便于我们扩展接口
                    break;
            }
        } catch (e) {
            console.log(e);
        }

    }
})
