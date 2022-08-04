/*
**  一个不属于其他模块的模块
*/
BLUEKING.base = (function(){
	return {
		/*
		**	系统初始化
		*/
		init : function(){
			//阻止弹出浏览器默认右键菜单
			$('body').on('contextmenu', function(){
				return false;
			});
			//桌面(容器)初始化
			BLUEKING.deskTop.init();
			//初始化壁纸
			BLUEKING.wallpaper.init();
			//初始化搜索栏
			BLUEKING.searchbar.init();
			//初始化DOCK栏的头像菜单、外观菜单和帮助菜单
			BLUEKING.docktool.init();
			//初始化任务栏
			BLUEKING.taskbar.init();
			/*
			**      当dockPos为top时          当dockPos为left时         当dockPos为right时
			**  -----------------------   -----------------------   -----------------------
			**  | o o o        [dock] |   | o | o               |   | o               | o |
			**  -----------------------   | o | o               |   | o               | o |
			**  | o o                 |   | o | o               |   | o               | o |
			**  | o +                 |   |   | o               |   | o               |   |
			**  | o            [desk] |   |   | o        [desk] |   | o        [desk] |   |
			**  | o                   |   |   | +               |   | +               |   |
			**  -----------------------   -----------------------   -----------------------
			**  因为desk区域的尺寸和定位受dock位置的影响，所以加载应用前必须先定位好dock的位置
			*/

			//初始化应用码头
			BLUEKING.dock.init();
			//初始化桌面应用
			BLUEKING.app.init();
			//初始化窗口模块
			BLUEKING.window.init();
			//初始化文件夹预览
			BLUEKING.folderView.init();
			//初始化全局视图
			BLUEKING.appmanage.init();
			//初始化右键菜单
			BLUEKING.popupMenu.init();
			//初始化快捷键
			BLUEKING.hotkey.init();
			//初始化版本信息
			BLUEKING.version.init();
			// 初始化license提示信息
			BLUEKING.license.init();
			//页面加载后运行
			// BLUEKING.base.help_first();
			BLUEKING.base.getSkin(function(skin){BLUEKING.base.setSkin(skin)});
		},
		logout_handler: function() {
			//退出登录
			var logout_url = BLUEKING.corefunc.get_logout_urlprefix();
			window.location.href = logout_url;
		},
		logout : function(){
			var dialog = art.dialog({
			    title: gettext('注销确认'),
				content: gettext('注销蓝鲸后需要重新登录，您确认注销?'),
			    fixed: true,
			    id: 'logout',
			    icon: 'question',
			    okVal: gettext('确定'),
                cancelVal: gettext('取消'),
			    ok: function () {
					BLUEKING.base.logout_handler();
			    },
				cancel: function () { }
			});
		},
		setLanguage: function(language, callback){
			$.ajax({
				type: 'POST',
				data: {language: language},
				async: false,
				url: urlPrefix + 'i18n/set_language/',
				success: function(){
					callback && callback();
				}
			});
		},
		getSkin:  function(callback){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_skin/',
				success : function(skin){
					callback && callback(skin);
				}
			});
		},
		setSkin : function(skin, callback){
			function styleOnload(node, callback) {
				// for IE6-9 and Opera
				if(node.attachEvent){
					node.attachEvent('onload', callback);
					// NOTICE:
					// 1. "onload" will be fired in IE6-9 when the file is 404, but in
					// this situation, Opera does nothing, so fallback to timeout.
					// 2. "onerror" doesn't fire in any browsers!
				}
				// polling for Firefox, Chrome, Safari
				else{
					setTimeout(function(){
						poll(node, callback);
					}, 0); // for cache
				}
			}
			function poll(node, callback) {
				if(callback.isCalled){
					return;
				}
				var isLoaded = false;
				//webkit
				if(/webkit/i.test(navigator.userAgent)){
					if (node['sheet']) {
						isLoaded = true;
					}
				}
				// for Firefox
				else if(node['sheet']){
					try{
						if (node['sheet'].cssRules) {
							isLoaded = true;
						}
					}catch(ex){
						// NS_ERROR_DOM_SECURITY_ERR
						if(ex.code === 1000){
							isLoaded = true;
						}
					}
				}
				if(isLoaded){
					// give time to render.
					setTimeout(function() {
						callback();
					}, 1);
				}else{
					setTimeout(function() {
						poll(node, callback);
					}, 1);
				}
			}
			//将原样式修改id，并载入新样式
			$('#window-skin').attr('id', 'window-skin-ready2remove');
			var css = document.createElement('link');
			css.rel = 'stylesheet';
			css.href = staticUrl + 'css/skins/' + skin + '.min.css?' + staticVersion;
			css.id = 'window-skin';
			document.getElementsByTagName('head')[0].appendChild(css);
			//新样式载入完毕后清空原样式
			//方法为参考seajs源码并改编，文章地址：http://www.blogjava.net/Hafeyang/archive/2011/10/08/360183.html
			styleOnload(css, function(){
				$('#window-skin-ready2remove').remove();
				BLUEKING.CONFIG.skin = skin;
				callback && callback();
			});
		},
		// help_first: function(){
		// 	//IE6,7,8基本就告别新手帮助了
		// 	if(!$.browser.msie || ($.browser.msie && $.browser.version > 8)){
		// 		$.getJSON(urlPrefix+'is_login_first/',{}, function(data){
		// 			if(data.result){
		// 				BLUEKING.base.help();
		// 			}
		// 		});
		// 	}
		// },
		help : function(){
			//IE6,7,8基本就告别新手帮助了
			if(!$.browser.msie || ($.browser.msie && $.browser.version > 8)){
				$('body').append(helpTemp);
				var w = $(window).width();
				var h = $(window).height();
				if(BLUEKING.CONFIG.dockPos == 'left'){
					var top = (h-600)/2 + 100;
					$('#step3').css({'top':top, 'left':105});
					$('#step4').css({'top':top+370, 'left':105});
					$('#step3 b').remove();
					$('#step3').prepend('<b class="jt jt_left" style="left:-40px;top:45px"></b>');
					$('#step4 b').remove();
					$('#step4').prepend('<b class="jt jt_left" style="left:-40px;top:45px"></b>');
				}else if(BLUEKING.CONFIG.dockPos == 'top'){
					var left = (w-600)/2 + 50;
					$('#step3').css({'top':105, 'left':left});
					$('#step4').css({'top':105, 'left':left+370});
					$('#step3 b').remove();
					$('#step3').prepend('<b class="jt jt_top" style="left:122px;top:-40px"></b>');
					$('#step4 b').remove();
					$('#step4').prepend('<b class="jt jt_top" style="left:122px;top:-40px"></b>');
				}else if(BLUEKING.CONFIG.dockPos == 'right'){
					var top =  (h-600)/2 + 100;
					var left = (w-400);
					$('#step3').css({'top':top, 'left':left});
					$('#step4').css({'top':top+370, 'left':left});
					$('#step3 b').remove();
					$('#step3').prepend('<b class="jt jt_right" style="left:290px;top:45px"></b>');
					$('#step4 b').remove();
					$('#step4').prepend('<b class="jt jt_right" style="left:290px;top:45px"></b>');
				}
				$('#step1').show();
				$('.close').on('click', function(){
					$('#help').remove();
				});
				$('.next').on('click', function(){
					var obj = $(this).parents('.step');
					var step = obj.attr('step');
					obj.hide();
					$('#step' + (parseInt(step) + 1)).show();
				});
				$('.over').on('click', function(){
					$('#help').remove();
					// $.post(urlPrefix + "set_login_first/", {}, function(data){}, 'json');
				});
				$('.donot_tip').on('click', function(){
					$('#help').remove();
					// $.post(urlPrefix + "set_login_first/", {}, function(data){}, 'json');
				});
			}
		},
	}
})();
