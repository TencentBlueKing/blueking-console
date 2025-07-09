/*
**  应用窗口
*/
BLUEKING.window = (function(){
	return {
		init : function(){
			//窗口上各个按钮
			BLUEKING.window.handle();
			//窗口移动
			BLUEKING.window.move();
			//窗口拉伸
			BLUEKING.window.resize();
			//绑定窗口遮罩层点击事件
			$('#desk').on('click', '.window-container .window-mask, .window-container .folder_body', function(){
				BLUEKING.window.show2top($(this).parents('.window-container').attr('appid'), true);
			});
			//屏蔽窗口右键
			$('#desk').on('contextmenu', '.window-container', function(){
				return false;
			});
			//绑定文件夹内应用点击事件
			$('#desk').on('click', '.folder_body li', function(){
				return false;
			}).on('contextmenu', '.folder_body .appbtn', function(e){
				$('.popup-menu').hide();
				$('.quick_view_container').remove();
				switch($(this).attr('type')){
					case 'app':
						var popupmenu = BLUEKING.popupMenu.app($(this));
						break;
				}
				var l = ($(window).width() - e.clientX) < popupmenu.width() ? (e.clientX - popupmenu.width()) : e.clientX;
				var t = ($(window).height() - e.clientY) < popupmenu.height() ? (e.clientY - popupmenu.height()) : e.clientY;
				popupmenu.css({
					left : l,
					top : t
				}).show();
				return false;
			});
		},
		/*
		**  创建窗口
		**  自定义窗口：BLUEKING.window.createTemp({title,url,width,height,resize});
		**      后面参数依次为：标题、地址、宽、高、是否可拉伸、是否打开默认最大化
		**      示例：BLUEKING.window.createTemp({title:"百度",url:"http://www.baidu.com",width:800,height:400,isresize:false,isopenmax:false});
		*/
		createTemp : function(obj, app_url){
			// 处理app_url
			app_url = BLUEKING.toolfunc.xssCheck(app_url);
			var type = 'app', appid = obj.appid == null ? Date.parse(new Date()) : obj.appid;
			//判断窗口是否已打开
			var iswindowopen = false;
			$('#task-content-inner a.task-item').each(function(){
				if($(this).attr('appid') == appid){
					iswindowopen = true;
					BLUEKING.window.show2top($(this).attr('appid'));
					return false;
				}
			});
			//如果没有打开，则进行创建
			if(!iswindowopen){
				function nextDo(options){
					var windowId = '#w_' + options.appid;
					//新增任务栏
					$('#task-content-inner').prepend(taskTemp({
						'type' : options.type,
						'id' : 't_' + options.appid,
						'appid' : options.appid,
						'title' : options.title,
						'imgsrc' : options.imgsrc,
						'islapp': options.islapp
					}));
					BLUEKING.taskbar.resize();
					// 如果需要打开某个具体的页面，则url改变
					var _url = options.url;
					if(app_url){
						_url = app_url;
					}
					//判断是否用当前浏览器窗口最大值打开app
					var win_width = options.width;			//app设置的宽度
					var win_height = options.height;		//app设置的高度
					var win_width_short = $(window).width() - options.width;	//window宽度 与 app设置的宽度差
					var win_height_short = $(window).height() - options.height;	//window高度 与 app设置的高度差
					//app不是最大化打开且是可以缩放的情况下
					if(options.isresize == true && options.isopenmax == false){
						if(win_width_short < 0){
							win_width = $(window).width();
						}
						if(win_height_short < 0){
							win_height = $(window).height();
						}
					}
					//新增窗口
					TEMP.windowTemp = {
						'top' : win_height_short / 2 <= 0 ? 0 : win_height_short / 2,
						'left' : win_width_short / 2 <= 0 ? 0 : win_width_short / 2,
						'emptyW' : win_width_short,
						'emptyH' : win_height_short,
						'width' : win_width,
						'height' : win_height,
						'zIndex' : BLUEKING.CONFIG.windowIndexid,
						'type' : options.type,
						'id' : 'w_' + options.appid,
						'appid' : options.appid,
						'realappid' : options.appid,
						'title' : options.title,
						'url' : _url,
						'org_url': options.url,
						'imgsrc' : options.imgsrc,
						'isresize' : options.isresize,
						'isopenmax' : options.isopenmax,
						'istitlebar' : options.isresize,
						'istitlebarFullscreen' : options.isresize ? window.fullScreenApi.supportsFullScreen == true ? true : false : false,
						'issetbar' : options.issetbar,
					};
					$('#desk').append(windowTemp(TEMP.windowTemp));
					$(windowId).data('info', TEMP.windowTemp);
					BLUEKING.CONFIG.windowIndexid += 1;
					BLUEKING.window.setPos(false);
					//iframe加载完毕后，隐藏loading遮罩层
					$(windowId + ' iframe').load(function(){
						$(windowId + ' .window-frame').children('div').eq(1).fadeOut();
					});
					BLUEKING.window.show2top(options.appid);
					var clip = new ClipboardJS('#w_' + options.appid + '_copy_url', {
						text: function(trigger) {
							var cp_text = '###';
							try{
								var location = document.getElementById('w_' + options.appid + '_iframe').contentWindow.location;
								var app_code = location.pathname.split('/')[2];
								var app_url = BLUEKING.corefunc.get_app_url(app_code);
								var url = location.href.replace(app_url, "");
								cp_text = BLUEKING.corefunc.get_bk_url() + '?app=' + app_code + '&url=' + encodeURIComponent(url);
							}catch(err){
								console.log(err);
								cp_text = $('#w_' + options.appid + '_iframe').attr('src');
							}
							return cp_text;
						}
					});
					clip.on('success',function(){
					  art.dialog({
							title:gettext( "温馨提示"),
							width: 340,
							icon: 'succeed',
							lock: false,
							fixed:true,
							content: gettext('复制成功！您可以使用ctrl+v进行粘贴！'),
							okVal: gettext("关闭"),
							time: 3
					  }).time(2)
						$('.popup-menu').hide();
					});

				}
				nextDo({
					type : type,
					appid : appid,
					imgsrc : obj.imgsrc ? obj.imgsrc : staticUrl + 'img/base_ui/default_icon.png',
					title : obj.title,
					url : obj.url,
					width : obj.width,
					height : obj.height,
					isresize : typeof(obj.isresize) == 'undefined' ? false : obj.isresize,
					isopenmax : typeof(obj.isopenmax) == 'undefined' ? false : obj.isopenmax,
					issetbar : false,
					islapp: typeof(obj.islapp) == 'undefined' ? false : obj.islapp,
					isthird: typeof(obj.isthird) == 'undefined' ? false : obj.isthird,
					is_in_paas3: typeof (obj.is_in_paas3) == 'undefined' ? false : obj.is_in_paas3,
				});
			}else{
				//如果是跳转url
				if(app_url){
					var windowId = '#w_' + appid;
					$(windowId).find('iframe').attr('src', app_url);
				}else{
					//如果设置强制刷新
					if(obj.refresh){
						var windowId = '#w_' + appid;
						$(windowId).find('iframe').attr('src', obj.url);
					}else{
						//应用市场跳转链接
						if(obj.appid == 'bk-yysc' && (obj.url.indexOf('?id=') >= 0 || obj.url.indexOf('?searchkey=') >= 0)){
							var windowId = '#w_' + appid;
							$(windowId).find('iframe').attr('src', obj.url);
						}
					}
				}
			}
		},
		/*
		**  创建窗口
		**  系统窗口：BLUEKING.window.create(appid, [type]);
		**      示例：BLUEKING.window.create(12);
		*/
		create : function(appid, app_url, appcode, isnotadd){
			// 处理app_url
			app_url = BLUEKING.toolfunc.xssCheck(app_url);
			//判断窗口是否已打开
			var iswindowopen = false;
			$('#task-content-inner a.task-item').each(function(){
				if($(this).attr('appid') == appid){
					iswindowopen = true;
					BLUEKING.window.show2top(appid);
					return false;
				}
			});
			//如果没有打开，则进行创建
			if(!iswindowopen && $('#d_' + appid).attr('opening') != 1){
				$('#d_' + appid).attr('opening', 1);
				function nextDo(options){
					var windowId = '#w_' + options.appid;
					//判断是否用当前浏览器窗口最大值打开app
					var win_width = options.width;	 //app设置的宽度
					var win_height = options.height; //app设置的高度
					var win_width_short = $(window).width() - options.width;	//window宽度 与 app设置的宽度差
					var win_height_short = $(window).height() - options.height;	//window高度 与 app设置的高度差
					//app不是最大化打开且是可以缩放的情况下
					if(options.isopenmax == false){
						if(win_width_short < 0){
							win_width = $(window).width();
						}
						if(win_height_short < 0){
							win_height = $(window).height();
						}
					}
					// window top & left
					var top = win_height_short / 2 <= 0 ? 0 : win_height_short / 2;
					var left = win_width_short / 2 <= 0 ? 0 : win_width_short / 2;
					switch(options.type){
						case 'app':
							// 如果需要打开某个具体的页面，则url改变
							var _url = options.url;

							if(app_url){
								var re_url = new RegExp('^(http:|https:)', 'gi');

								if(parseInt(options.isthird) == 1){
									// 第三方应用
									if(re_url.test(app_url)){
										var p = new Poly9.URLParser(app_url);
										var _host = p.getHost();
										var url_p = new Poly9.URLParser(_url);
										var _url_host = url_p.getHost();
										//判断跳转链接是否与第三方应用同域
										if(_host == _url_host){
											_url = app_url;
										}
									}
								}else if(re_url.test(app_url)){
									// 内建应用类型判断是否是蓝鲸应用域名
									var p = new Poly9.URLParser(app_url);
									var _host = p.getHost();
									if(_host == BLUEKING.corefunc.get_bk_host()){
										_url = app_url;
									}
								}else{
									//app_url为path
									if (parseInt(options.is_in_paas3) == 1) {
										// PaaS3.0 应用的链接直接由后台返回, 不是由平台域名拼接而来
										app_domain = options.url;
									}else{
										app_domain = BLUEKING.corefunc.get_app_url(options.app_code)
									}

									// 判断拼接域名 和 path 的时候是不是需要手动添加 /
									if (app_domain.endsWith("/") || app_url.startsWith("/")) {
										_url = app_domain + app_url;
									}else{
										_url = app_domain + '/' + app_url;
									}

									// 当链接末尾没有 '/' 且链接末尾未带有 get 参数时, 在结尾加上'/'
									if (!_url.endsWith("/") && _url.indexOf("?") === -1) {
										_url = _url + '/';
									}
								}
							}
							// 记录app使用信息
							BLUEKING.api.app_record_by_user(options.realappid);
							if(options.open_mode == "new_tab") {
								// 新标签打开
								window.open(_url, "_blank");
								return
							}
							//新增任务栏
							$('#task-content-inner').prepend(taskTemp({
								'type' : options.type,
								'id' : 't_' + options.appid,
								'appid' : options.appid,
								'title' : options.title,
								'imgsrc' : options.imgsrc,
								'app_code': options.app_code,
								'islapp': options.islapp
							}));
							BLUEKING.taskbar.resize();
							//新增窗口
							TEMP.windowTemp = {
								'top' : top,
								'left' : left,
								'emptyW' : win_width_short,
								'emptyH' : win_height_short,
								'width' : win_width,
								'height' : win_height,
								'zIndex' : BLUEKING.CONFIG.windowIndexid,
								'type' : options.type,
								'id' : 'w_' + options.appid,
								'appid' : options.appid,
								'realappid' : options.realappid,
								'title' : options.title,
								'url' : _url,
								'org_url': options.url,
								'imgsrc' : options.imgsrc,
								'isthird': options.isthird,

								'isresize' : options.isresize == 1 ? true : false,
								'isopenmax' : options.isresize == 1 ? options.isopenmax == 1 ? true : false : false,
								'istitlebar' : options.isresize == 1 ? true : false,
								'istitlebarFullscreen' : options.isresize == 1 ? window.fullScreenApi.supportsFullScreen == true ? true : false : false,
								'issetbar' : options.issetbar == 1 ? true : false,
							};
							$('#desk').append(windowTemp(TEMP.windowTemp));
							$(windowId).data('info', TEMP.windowTemp);
							BLUEKING.CONFIG.windowIndexid += 1;
							BLUEKING.window.setPos(false);
							//iframe加载完毕后，隐藏loading遮罩层
							$(windowId + ' iframe').load(function(){
								$(windowId + ' .window-frame').children('div').fadeOut();
							});
							BLUEKING.window.show2top(options.appid);
							var clip = new ClipboardJS('#w_' + options.appid + '_copy_url', {
								text: function(trigger) {
									var cp_text = '###';
									try{
										var location = document.getElementById('w_' + options.appid + '_iframe').contentWindow.location;
										var app_code = location.pathname.split('/')[2];
										var app_url = BLUEKING.corefunc.get_app_url(app_code);
										var url = location.href.replace(app_url, "");
										cp_text = BLUEKING.corefunc.get_bk_url() + '?app=' + app_code + '&url=' + encodeURIComponent(url);
									}catch(err){
										console.log(err);
										cp_text = $('#w_' + options.appid + '_iframe').attr('src');
									}
									return cp_text;
								}
							});
							clip.on('success',function(){
							  art.dialog({
									title:gettext( "温馨提示"),
									width: 340,
									icon: 'succeed',
									lock: false,
									fixed:true,
									content: gettext('复制成功！您可以使用ctrl+v进行粘贴！'),
									okVal: gettext("关闭"),
									time: 3
							  }).time(2)
								$('.popup-menu').hide();
							});
							break;
						case 'folder':
							//新增任务栏
							$('#task-content-inner').prepend(taskTemp({
								'type' : options.type,
								'id' : 't_' + options.appid,
								'appid' : options.appid,
								'app_code': '',
								'title' : options.title,
								'imgsrc' : options.imgsrc,
								'islapp': options.islapp
							}));
							BLUEKING.taskbar.resize();
							//新增窗口
							TEMP.folderWindowTemp = {
								'top' : top,
								'left' : left,
								'emptyW' : $(window).width() - options.width,
								'emptyH' : $(window).height() - options.height,
								'width' : options.width,
								'height' : options.height,
								'zIndex' : BLUEKING.CONFIG.windowIndexid,
								'type' : options.type,
								'id' : 'w_' + options.appid,
								'appid' : options.appid,
								'title' : options.title,
								'imgsrc' : options.imgsrc
							};
							$('#desk').append(folderWindowTemp(TEMP.folderWindowTemp));
							$(windowId).data('info', TEMP.folderWindowTemp);
							BLUEKING.CONFIG.windowIndexid += 1;
							BLUEKING.window.setPos(false);
							//载入文件夹内容
							var sc = '';
							$(BLUEKING.VAR.folder).each(function(){
								if(this.appid == options.appid){
									sc = this.apps;
									return false;
								}
							});
							if(sc != ''){
								var folder_append = '';
								$(sc).each(function(){
									folder_append += appbtnTemp({
										'title' : this.title,
										'name' : this.name,
										'type' : this.type,
										'id' : 'd_' + this.appid,
										'appid' : this.appid,
										'code' : this.app_code,
										'imgsrc' : this.icon,
										'isoutline': this.isoutline,
										'islapp': this.islapp
									});
								});
								$(windowId).find('.folder_body').append(folder_append);
							}
							BLUEKING.window.show2top(options.appid);
							break;
					}
				}
				ZENG.msgbox.show(gettext('应用正在加载中，请耐心等待...'), 6, 100000);
				//判断app打开方式，没有添加则使用appcode查找app信息，打开了则使用appid（用户ID）查找
				if((typeof(appid)=='number' || appid.match('^[0-9]+$')) && !isnotadd){
					var get_app_url = urlPrefix + 'get_my_app_by_id/' + appid + '/';
				}else{
					var get_app_url = urlPrefix + 'get_my_app_by_code/' + appid + '/';
				}
				$.getJSON(get_app_url, function(app){
					if(app != null){
						if(app['error'] == 'E100'){
							if(app['type'] == 'folder'){
								ZENG.msgbox.show(gettext('文件夹不存在，建议删除'), 5, 2000);
							}else{
								ZENG.msgbox.show(gettext('应用不存在，建议卸载'), 5, 2000);
							}
						}else if(app['error']=='E501' || app['error']=='E502' || app['error']=='E503'){
							ZENG.msgbox.show(gettext('应用加载失败，请重试'), 5, 2000);
						}else if(app['error']=='E400'){
							//appid（用户appid）存在则使用，不存在则用code
							if(app['appid']){
								var _appid = app['appid'];
							}else{
								var _appid = app['app_code'];
							}
							ZENG.msgbox.show(gettext('您没有操作该应用的权限，正在为您卸载该应用...'), 5, 2000);
							BLUEKING.app.remove(_appid, function(){
//								ZENG.msgbox.show('卸载成功', 1, 1000);
								BLUEKING.app.get();
							});
						}else{
							//appid（用户appid）存在则使用，不存在则用code
							if(app['appid']){
								var _appid = app['appid'];
							}else{
								var _appid = app['app_code'];
							}
							if(app['is_outline']==1){
								ZENG.msgbox.show(gettext('应用已经下架，正在为您卸载该应用...'), 5, 2000);
								BLUEKING.app.remove(_appid, function(){
//									ZENG.msgbox.show('卸载成功', 1, 1000);
									BLUEKING.app.get();
								});
							}else{
								ZENG.msgbox._hide();
								nextDo({
									type : app['type'],
									id : _appid,
									appid : _appid,
									realappid : app['realappid'],
									title : app['name'],
									imgsrc : app['icon'],
									isthird: app['isthird'],
									url : app['url'],
									width : app['width'],
									height : app['height'],
									isresize : app['isresize'],
									isopenmax : app['isopenmax'],
									issetbar : app['issetbar'],
									app_code : app['app_code'],
									islapp: app['islapp'],
									open_mode: app['open_mode'],
									is_in_paas3: app['is_in_paas3']
								});
							}
						}
					}else{
						ZENG.msgbox.show(gettext('数据拉取失败'), 5, 2000);
					}
					$('#d_' + appid).attr('opening', 0);
				});
			}else{
				//app已经打开，带url，强制刷新
				var window_app = '#w_' + appid;
				if(app_url){
					// todo 第三方应用判断是否与第三方链接同域名，内置应用判断是否与蓝鲸平台同域
				}else{ //没有带url，传参选择是否弹出刷新提示
					if(appcode){
						//判断应用是否在首页
						var app_iframe_src = $(window_app).find('iframe').attr('src');
						// todo 第三方应用后台获取对应链接
						var re = BLUEKING.corefunc.get_app_url(appcode);
						if(re != app_iframe_src){
							//app不在首页，则提示是否刷新到首页
							art.dialog({
								title: gettext("温馨提示"),
								width: 340,
								icon: 'warning',
								lock: true,
								content: gettext('该应用已经打开，是否刷新到应用首页？'),
								okVal: gettext('刷新'),
								ok: function(){
									$(window_app).find('iframe').attr('src', re);
								},
								cancelVal:gettext('不刷新'),
								cancel: function(){}
							});
						}
					}
				}
			}
		},
		setPos : function(isAnimate){
			isAnimate = isAnimate == null ? true : isAnimate;
			$('#desk .window-container').each(function(){
				var windowdata = $(this).data('info');
				var currentW = $(window).width() - $(this).width();
				var currentH = $(window).height() - $(this).height();
				var left = 0;
				var top = 0;
				if(windowdata['emptyW'] != 0){
					left = windowdata['left'] / windowdata['emptyW'] * currentW >= currentW ? currentW : windowdata['left'] / windowdata['emptyW'] * currentW;
				}
				left = left <= 0 ? 0 : left;
				if(windowdata['emptyH'] != 0){
					top = windowdata['top'] / windowdata['emptyH'] * currentH >= currentH ? currentH : windowdata['top'] / windowdata['emptyH'] * currentH;
				}
				top = top <= 0 ? 0 : top;
				if($(this).attr('state') != 'hide'){
					$(this).stop(true, false).animate({
						'left' : left,
						'top' : top
					}, isAnimate ? 500 : 0, function(){
						windowdata['left'] = left;
						windowdata['top'] = top;
						windowdata['emptyW'] = $(window).width() - $(this).width();
						windowdata['emptyH'] = $(window).height() - $(this).height();
					});
				}else{
					windowdata['left'] = left;
					windowdata['top'] = top;
					windowdata['emptyW'] = $(window).width() - $(this).width();
					windowdata['emptyH'] = $(window).height() - $(this).height();
				}
			});
		},
		close : function(appid){
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId).removeData('info').html('').remove();
			$('#task-content-inner ' + taskId).html('').remove();
			$('#task-content-inner').css('width', $('#task-content-inner .task-item').length * 114);
			$('#task-bar, #nav-bar').removeClass('min-zIndex');
			BLUEKING.taskbar.resize();
		},
		closeAll : function(){
			$('#desk .window-container').each(function(){
				BLUEKING.window.close($(this).attr('appid'));
			});
		},
		hide : function(appid){
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId).css('left', -10000).attr('state', 'hide');
			$('#task-content-inner ' + taskId).removeClass('task-item-current');
			if($(windowId).attr('ismax') == 1){
				$('#task-bar, #nav-bar').removeClass('min-zIndex');
			}
		},
		hideAll : function(){
			$('#task-content-inner a.task-item').removeClass('task-item-current');
			$('#desk-' + BLUEKING.CONFIG.desk).nextAll('div.window-container').css('left', -10000).attr('state', 'hide');
			$('#task-bar, #nav-bar').removeClass('min-zIndex');
		},
		max : function(appid){
			BLUEKING.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId + ' .title-handle .ha-max').hide().next(".ha-revert").show();
			$(windowId).addClass('window-maximize').attr('ismax',1).animate({
				width : '100%',
				height : '100%',
				top : 0,
				left : 0
			}, 200);
			$('#task-bar, #nav-bar').addClass('min-zIndex');
		},
		revert : function(appid){
			BLUEKING.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId + ' .title-handle .ha-revert').hide().prev('.ha-max').show();
			var obj = $(windowId), windowdata = obj.data('info');
			obj.removeClass('window-maximize').attr('ismax',0).animate({
				width : windowdata['width'],
				height : windowdata['height'],
				left : windowdata['left'],
				top : windowdata['top']
			}, 500);
			$('#task-bar, #nav-bar').removeClass('min-zIndex');
		},
		refresh : function(appid){
			BLUEKING.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			//判断是应用窗口，还是文件夹窗口
			if($(windowId + '_iframe').length != 0){
				$(windowId + '_iframe').attr('src', $(windowId + '_iframe').attr('org_url'));
			}else{
				BLUEKING.window.updateFolder(appid);
			}
		},
		refresh_current : function(appid){
			BLUEKING.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			//判断是应用窗口，还是文件夹窗口
			if($(windowId + '_iframe').length != 0){
				document.getElementById('w_' + appid + '_iframe').contentWindow.location.reload();
			}else{
				BLUEKING.window.updateFolder(appid);
			}
		},
		go_back : function(appid){
			BLUEKING.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			//判断是应用窗口，还是文件夹窗口
			if($(windowId + '_iframe').length != 0){
				// var referrer = document.getElementById('w_' + appid + '_iframe').contentDocument.referrer;
				// var current_href = window.location.href;
				// if(referrer != current_href){
				// 	document.getElementById('w_' + appid + '_iframe').contentWindow.history.back()
				// }else{
				// 	$(windowId + '_iframe').attr('src', document.getElementById('w_' + appid + '_iframe').contentWindow.location.href);
				// }
				document.getElementById('w_' + appid + '_iframe').contentWindow.history.back()
			}else{
				BLUEKING.window.updateFolder(appid);
			}
		},
		show2top : function(appid, isAnimate){
			isAnimate = isAnimate == null ? false : isAnimate;
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			var windowdata = $(windowId).data('info');
			var arr = [];
			function show(){
				BLUEKING.window.show2under();
				//改变当前任务栏样式
				$('#task-content-inner ' + taskId).addClass('task-item-current');
				if($(windowId).attr('ismax') == 1){
					$('#task-bar, #nav-bar').addClass('min-zIndex');
				}
				//改变当前窗口样式
				$(windowId).addClass('window-current').css({
					'z-index' : BLUEKING.CONFIG.windowIndexid,
					'left' : windowdata['left'],
					'top' : windowdata['top']
				}).attr('state', 'show');
				//如果窗口最小化前是最大化状态的，则坐标位置设为0
				if($(windowId).attr('ismax') == 1){
					$(windowId).css({
						'left' : 0,
						'top' : 0
					});
				}
				//改变当前窗口遮罩层样式
				$(windowId + ' .window-mask').hide();
				//改变当前iframe显示
				$(windowId + ' iframe').show();
				BLUEKING.CONFIG.windowIndexid += 1;
			}
			if(isAnimate){
				var baseStartX = $(windowId).offset().left, baseEndX = baseStartX + $(windowId).width();
				var baseStartY = $(windowId).offset().top, baseEndY = baseStartY + $(windowId).height();
				var baseCenterX = baseStartX + ($(windowId).width() / 2), baseCenterY = baseStartY + ($(windowId).height() / 2);
				var baseZIndex = parseInt($(windowId).css('zIndex'));
				$('#desk .window-container:not(' + windowId + ')').each(function(){
					var thisStartX = $(this).offset().left, thisEndX = thisStartX + $(this).width();
					var thisStartY = $(this).offset().top, thisEndY = thisStartY + $(this).height();
					var thisCenterX = thisStartX + ($(this).width() / 2), thisCenterY = thisStartY + ($(this).height() / 2);
					var thisZIndex = parseInt($(this).css('zIndex'));
					var flag = '';
					if(thisZIndex > baseZIndex){
						//  常规情况，只要有一个角处于区域内，则可以判断窗口有覆盖
						//   _______            _______        _______    _______
						//  |    ___|___    ___|       |   ___|___    |  |       |___
						//  |   |       |  |   |       |  |       |   |  |       |   |
						//  |___|       |  |   |_______|  |       |___|  |_______|   |
						//      |_______|  |_______|      |_______|          |_______|
						if(
							(thisStartX >= baseStartX && thisStartX <= baseEndX && thisStartY >= baseStartY && thisStartY <= baseEndY)
							||
							(thisStartX >= baseStartX && thisStartX <= baseEndX && thisEndY >= baseStartY && thisEndY <= baseEndY)
							||
							(thisEndX >= baseStartX && thisEndX <= baseEndX && thisStartY >= baseStartY && thisStartY <= baseEndY)
							||
							(thisEndX >= baseStartX && thisEndX <= baseEndX && thisEndY >= baseStartY && thisEndY <= baseEndY)
						){
							flag = 'x';
						}
						//  非常规情况
						//       _______    _______          _____
						//   ___|       |  |       |___    _|     |___
						//  |   |       |  |       |   |  | |     |   |
						//  |___|       |  |       |___|  |_|     |___|
						//      |_______|  |_______|        |_____|
						if(
							(thisStartX >= baseStartX && thisStartX <= baseEndX && thisStartY < baseStartY && thisEndY > baseEndY)
							||
							(thisEndX >= baseStartX && thisEndX <= baseEndX && thisStartY < baseStartY && thisEndY > baseEndY)
						){
							flag = 'x';
						}
						//      _____       ___________      _____
						//   __|_____|__   |           |   _|_____|___
						//  |           |  |           |  |           |
						//  |           |  |___________|  |___________|
						//  |___________|     |_____|       |_____|
						if(
							(thisStartY >= baseStartY && thisStartY <= baseEndY && thisStartX < baseStartX && thisEndX > baseEndX)
							||
							(thisEndY >= baseStartY && thisEndY <= baseEndY && thisStartX < baseStartX && thisEndX > baseEndX)
						){
							flag = 'y';
						}
						//  两个角处于区域内，另外两种情况不用处理，因为这两种情况下，被移动的窗口是需要进行上下滑动，而非左右
						//      _____       ___________
						//   __|     |__   |   _____   |
						//  |  |     |  |  |  |     |  |
						//  |  |_____|  |  |__|     |__|
						//  |___________|     |_____|
						if(
							(thisStartX >= baseStartX && thisStartX <= baseEndX && thisEndY >= baseStartY && thisEndY <= baseEndY)
							&&
							(thisEndX >= baseStartX && thisEndX <= baseEndX && thisEndY >= baseStartY && thisEndY <= baseEndY)
							||
							(thisStartX >= baseStartX && thisStartX <= baseEndX && thisStartY >= baseStartY && thisStartY <= baseEndY)
							&&
							(thisEndX >= baseStartX && thisEndX <= baseEndX && thisStartY >= baseStartY && thisStartY <= baseEndY)
						){
							flag = 'y';
						}
					}
					if(flag != ''){
						var direction, distance;
						if(flag == 'x'){
							if(thisCenterX > baseCenterX){
								direction = 'right';
								distance = baseEndX - thisStartX + 30;
							}else{
								direction = 'left';
								distance = thisEndX - baseStartX + 30;
							}
						}else{
							if(thisCenterY > baseCenterY){
								direction = 'bottom';
								distance = baseEndY - thisStartY + 30;
							}else{
								direction = 'top';
								distance = thisEndY - baseStartY + 30;
							}
						}
						arr.push({
							id : $(this).attr('id'),
							direction : direction, //移动方向
							distance : distance //移动距离
						});
					}
				});
				//开始移动
				var delayTime = 0;
				for(var i = 0; i < arr.length; i++){
					var baseLeft = $('#' + arr[i].id).offset().left, baseTop = $('#' + arr[i].id).offset().top;
					if(arr[i].direction == 'left'){
						$('#' + arr[i].id).delay(delayTime).animate({
							left : baseLeft - arr[i].distance
						}, 300).animate({
							left : baseLeft
						}, 300);
					}else if(arr[i].direction == 'right'){
						$('#' + arr[i].id).delay(delayTime).animate({
							left : baseLeft + arr[i].distance
						}, 300).animate({
							left : baseLeft
						}, 300);
					}else if(arr[i].direction == 'top'){
						$('#' + arr[i].id).delay(delayTime).animate({
							top : baseTop - arr[i].distance
						}, 300).animate({
							top : baseTop
						}, 300);
					}else if(arr[i].direction == 'bottom'){
						$('#' + arr[i].id).delay(delayTime).animate({
							top : baseTop + arr[i].distance
						}, 300).animate({
							top : baseTop
						}, 300);
					}
					delayTime += 100;
				}
				setTimeout(show, delayTime + 100);
			}else{
				show();
			}
		},
		show2under : function(){
			//改变任务栏样式
			$('#task-content-inner a.task-item').removeClass('task-item-current');
			//改变窗口样式
			$('#desk .window-container').removeClass('window-current');
			//改变窗口遮罩层样式
			$('#desk .window-container .window-mask').show();
		},
		updateFolder : function(appid){
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			var sc = '';
			$(BLUEKING.VAR.folder).each(function(){
				if(this.appid == appid){
					sc = this.apps;
					return false;
				}
			});
			if(sc != null){
				var folder_append = '';
				for(var i = 0; i < sc.length; i++){
					if(sc[i]['title'] != ''){
						var _audit_title = sc[i]['title'] + '（' + this.title +'）';
					}else{
						var _audit_title = sc[i]['title'];
					}
					folder_append += appbtnTemp({
						'top' : 0,
						'left' : 0,
						'title' : _audit_title,
						'name' : sc[i]['name'],
						'type' : sc[i]['type'],
						'id' : 'd_' + sc[i]['appid'],
						'appid' : sc[i]['appid'],
						'code': sc[i]['app_code'],
						'imgsrc' : sc[i]['icon'],
						'isoutline': sc[i]['isoutline'],
						'islapp': sc[i]['islapp']
					});
				}
				$(windowId).find('.folder_body').html('').append(folder_append).on('contextmenu', '.appbtn', function(e){
					$('.popup-menu').hide();
					$('.quick_view_container').remove();
					TEMP.AppRight = BLUEKING.popupMenu.app($(this));
					var l = ($(window).width() - e.clientX) < TEMP.AppRight.width() ? (e.clientX - TEMP.AppRight.width()) : e.clientX;
					var t = ($(window).height() - e.clientY) < TEMP.AppRight.height() ? (e.clientY - TEMP.AppRight.height()) : e.clientY;
					TEMP.AppRight.css({
						left : l,
						top : t
					}).show();
					return false;
				});
			}
		},
		handle : function(){
			$('#desk').on('mousedown', '.window-container .title-bar .title-handle a', function(e){
				e.preventDefault();
				e.stopPropagation();
			});
			$('#desk').on('mouseenter', '.window-container .copy_current_url', function(e){
				$(this).addClass('focus');
			}).on('mouseleave', '.window-container .copy_current_url', function(){
				$(this).removeClass('focus');
			});
			$('#desk').on('dblclick', '.window-container .title-bar', function(e){
				var obj = $(this).parents('.window-container');
				//判断当前窗口是否已经是最大化
				if(obj.find('.ha-max').is(':hidden')){
					obj.find('.ha-revert').click();
				}else{
					obj.find('.ha-max').click();
				}
			}).on('click', '.window-container .ha-hide', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.hide(obj.attr('appid'));
			}).on('click', '.window-container .ha-max', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.max(obj.attr('appid'));
			}).on('click', '.window-container .ha-revert', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.revert(obj.attr('appid'));
			}).on('click', '.window-container .ha-fullscreen', function(){
				var obj = $(this).parents('.window-container');
				window.fullScreenApi.requestFullScreen(document.getElementById(obj.find('iframe').attr('id')));
			}).on('click', '.window-container .ha-close', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.close(obj.attr('appid'));
			}).on('click', '.window-container .refresh', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.refresh(obj.attr('appid'));
			}).on('click', '.window-container .refresh_current', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.refresh_current(obj.attr('appid'));
			}).on('click', '.window-container .go_back', function(){
				var obj = $(this).parents('.window-container');
				BLUEKING.window.go_back(obj.attr('appid'));
			}).on('click', '.window-container .detail', function(){
				var obj = $(this).parents('.window-container');
				if(obj.attr('realappid') !== 0){
					BLUEKING.window.create_market(obj.attr('realappid'));
				}else{
					ZENG.msgbox.show(gettext('对不起，该应用没有任何详细介绍'), 1, 2000);
				}
			}).on('contextmenu', '.window-container', function(){
				$('.popup-menu').hide();
				$('.quick_view_container').remove();
				return false;
			});
		},
		move : function(){
			$('#desk').on('mousedown', '.window-container .title-bar', function(e){
				var obj = $(this).parents('.window-container');
				if(obj.attr('ismax') == 1){
					return false;
				}
				BLUEKING.window.show2top(obj.attr('appid'), true);
				var windowdata = obj.data('info');
				var x = e.clientX - obj.offset().left;
				var y = e.clientY - obj.offset().top;
				var lay;
				//绑定鼠标移动事件
				$(document).on('mousemove', function(e){
					lay = BLUEKING.maskBox.desk();
					lay.show();
					//强制把右上角还原按钮隐藏，最大化按钮显示
					obj.find('.ha-revert').hide().prev('.ha-max').show();
					obj.css({
						width : windowdata['width'],
						height : windowdata['height'],
						left : e.clientX - x,
						top : e.clientY - y <= 10 ? 0 : e.clientY - y >= lay.height()-30 ? lay.height()-30 : e.clientY - y
					});
					obj.data('info').left = obj.offset().left;
					obj.data('info').top = obj.offset().top;
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
					if(typeof(lay) !== 'undefined'){
						lay.hide();
					}
				});
			});
		},
		resize : function(obj){
			$('#desk').on('mousedown', '.window-container .window-resize', function(e){
				var obj = $(this).parents('.window-container');
				var resizeobj = $(this);
				var lay;
				var x = e.clientX;
				var y = e.clientY;
				var w = obj.width();
				var h = obj.height();
				$(document).on('mousemove', function(e){
					lay = BLUEKING.maskBox.desk();
					lay.show();
					//当拖动到屏幕边缘时，自动贴屏
					var _x = e.clientX <= 10 ? 0 : e.clientX >= (lay.width() - 12) ? (lay.width() - 2) : e.clientX;
					var _y = e.clientY <= 10 ? 0 : e.clientY >= (lay.height() - 12) ? lay.height() : e.clientY;
					switch(resizeobj.attr('resize')){
						case 't':
							h + y - _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							break;
						case 'r':
							w - x + _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							break;
						case 'b':
							h - y + _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							break;
						case 'l':
							w + x - _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							break;
						case 'rt':
							h + y - _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							w - x + _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							break;
						case 'rb':
							w - x + _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							h - y + _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							break;
						case 'lt':
							w + x - _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							h + y - _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							break;
						case 'lb':
							w + x - _x > BLUEKING.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : BLUEKING.CONFIG.windowMinWidth
							});
							h - y + _y > BLUEKING.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : BLUEKING.CONFIG.windowMinHeight
							});
							break;
					}
				}).on('mouseup',function(){
					if(typeof(lay) !== 'undefined'){
						lay.hide();
					}
					obj.data('info').width = obj.width();
					obj.data('info').height = obj.height();
					obj.data('info').left = obj.offset().left;
					obj.data('info').top = obj.offset().top;
					obj.data('info').emptyW = $(window).width() - obj.width();
					obj.data('info').emptyH = $(window).height() - obj.height();
					$(this).off('mousemove').off('mouseup');
				});
			});
		},
		switchWindow: function(windowNumber){
			var r = /^\+?[1-9]*$/;
			windowNumber = r.test(windowNumber) ? windowNumber : 1;
			var window_list = $('#task-content-inner .task-item');
			if(window_list.length >= windowNumber){
				BLUEKING.window.show2top(window_list.eq(window_list.length-windowNumber).attr('appid'));
			}
			return true;
		},
		switchWindowLeft: function(){
			var current_obj = $('#task-content-inner .task-item-current');
			if(current_obj.length == 0){
				if($('#task-content-inner .task-item').length > 0){
					current_obj = $('#task-content-inner .task-item:first');
					BLUEKING.window.show2top(current_obj.attr('appid'));
				}
				return true;
			}
			var left_obj = $(current_obj).next();
			if(left_obj.length == 0){
				left_obj = $('#task-content-inner .task-item:first');
			}
			BLUEKING.window.show2top(left_obj.attr('appid'));
			return true;
		},
		switchWindowRight: function(){
			var current_obj = $('#task-content-inner .task-item-current');
			if(current_obj.length == 0){
				if($('#task-content-inner .task-item').length > 0){
					current_obj = $('#task-content-inner .task-item:last');
					BLUEKING.window.show2top(current_obj.attr('appid'));
				}
				return false;
			}
			var right_obj = $(current_obj).prev();
			if(right_obj.length == 0){
				right_obj = $('#task-content-inner .task-item:last');
			}
			BLUEKING.window.show2top(right_obj.attr('appid'));
			return false;
		},
		// 基于上面的函数封装的其他方法
		// 应用市场窗口
		create_market : function(app_id){
			var url = urlPrefix + 'market/';
			if(app_id){
				url += '?id=' + app_id;
			}
			BLUEKING.window.createTemp({
				appid : 'bk-yysc',
				app_code : 'app_market',
				title : gettext('应用市场'),
				url : url,
				width : 1010,
				height : 623,
				imgsrc : staticUrl + 'img/shortcut/tool_app/market.png',
				refresh : false //需要强制刷新
			});
		},
		// 带搜索参数，应用市场窗口
		create_market_search : function(searchkey){
			var url = urlPrefix + 'market/';
			if(searchkey){
				url += '?searchkey=' + searchkey;
			}
			BLUEKING.window.createTemp({
				appid : 'bk-yysc',
				app_code : 'app_market',
				title : gettext('应用市场'),
				url : url,
				width : 1010,
				height : 623,
				imgsrc : staticUrl + 'img/shortcut/tool_app/market.png',
				refresh : false //需要强制刷新
			});
		},
		// 创建主题设置窗口
		create_theme_window: function(){
			BLUEKING.window.createTemp({
				appid : 'bk-ztsz',
				title : gettext('主题设置'),
				url : urlPrefix + 'wallpaper/',
				width : 580,
				height : 520,
			});
		},
		// 创建布局设置窗口
		create_setting_window: function(){
			BLUEKING.window.createTemp({
				appid : 'bk-zmsz',
				title : gettext('布局设置'),
				url : urlPrefix + 'desk_setting/',
				width : 750,
				height : 520,
			});
		},
		// 创建权限中心应用窗口
		create_bk_iam: function(app_url){
			BLUEKING.api.open_app_by_desk('bk_iam', app_url)
		},
		// 创建用户管理应用窗口
		create_bk_user_manage: function(app_url){
			BLUEKING.api.open_app_by_desk(bk_user_app_code, app_url)
		},
		// 创建个人中心应用窗口
		create_user_center : function(app_url){
			BLUEKING.api.open_app_by_desk('bk_usermgr', app_url)
		},
		// 桌面添加菜单
		create_add_menu : function(e){
			// 弹出菜单
			$("#desk_add_menu").css({
				left: e.pageX,
				top: e.pageY
			}).show();
			// 点击任何地方，可以收起菜单
			$(document).click(function(event){
				if( !$(event.target).is("#desk li.appbtn.add") && !$(event.target).parents().is("#desk li.appbtn.add")){
					$("#desk_add_menu").hide();
				}
			});
		},
		// 隐藏桌面添加菜单
		hide_add_menu: function(){
			$("#desk_add_menu").hide();
		}
	}
})();
