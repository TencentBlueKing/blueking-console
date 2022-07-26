/*
**  DOCK 工具栏（头像、外观、反馈、全局视图、相关疑问）
*/
BLUEKING.docktool = (function(){
	return {
		/*
		**	初始化
		*/
		init : function(){
			// 头像菜单初始化
			$('#startmenu-container').on('mousedown', function(e){
				e.preventDefault();
			}).on('mouseover', function(e){
				BLUEKING.DOCKTOOL_VAR.startmenu_state = true;
				BLUEKING.docktool.show_startmenu();
			}).on('mouseout', function(e){
				BLUEKING.DOCKTOOL_VAR.startmenu_state = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.startmenu_state && !BLUEKING.DOCKTOOL_VAR.tool_start){
						BLUEKING.docktool.hide_startmenu();
					}
				}, 300);
			});
			// 绑定头像菜单点击（名字）事件
			$('#startmenu-container .startmenu a').on('click', function(){
				switch($(this).attr('class')){
					case 'user_center':
						window.open(BLUEKING.corefunc.get_account_profile_urlprefix(), '_blank');
						break;
					case 'about':
						window.open(BLUEKING.corefunc.get_external_links('bk_os'), '_blank');
						break;
					case 'bk_service_agreement':
						window.open(BLUEKING.corefunc.get_external_links('bk_service_agreement'), '_blank');
						break;
				}
			});
			// 绑定头像菜单点击（注销）事件
			$('#startmenu-container .startmenu-exit a').on('click', function(){
				BLUEKING.base.logout();
			});

			// 外观菜单初始化
			$('#appearancemenu-container').on('mousedown', function(e){
				e.preventDefault();
			}).on('mouseover', function(e){
				BLUEKING.DOCKTOOL_VAR.appearancemenu_state = true;
				BLUEKING.docktool.show_appearancemenu();
			}).on('mouseout', function(e){
				BLUEKING.DOCKTOOL_VAR.appearancemenu_state = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.appearancemenu_state && !BLUEKING.DOCKTOOL_VAR.tool_appearance){
						BLUEKING.docktool.hide_appearancemenu();
					}
				}, 300);
			});
			// 绑定外观菜单点击（主题设置、布局设置）事件
			$('#appearancemenu-container .appearancemenu a').on('click', function(){
				switch($(this).attr('class')){
					case 'theme_setting':
						BLUEKING.window.create_theme_window();
						break;
					case 'layout_setting':
						BLUEKING.window.create_setting_window();
						break;
				}
			});

			// 帮助菜单初始化
			$('#helpsmenu-container').on('mousedown', function(e){
				e.preventDefault();
			}).on('mouseover', function(e){
				BLUEKING.DOCKTOOL_VAR.helpsmenu_state = true;
				BLUEKING.docktool.show_helpsmenu();
			}).on('mouseout', function(e){
				BLUEKING.DOCKTOOL_VAR.helpsmenu_state = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.helpsmenu_state && !BLUEKING.DOCKTOOL_VAR.tool_helps){
						BLUEKING.docktool.hide_helpsmenu();
					}
				}, 300);
			});
			// 绑定帮助菜单点击（快捷键、桌面指引）事件
			$('#helpsmenu-container .helpsmenu a').on('click', function(){
				switch($(this).attr('class')){
					case 'about_version':
						BLUEKING.version.show();
						break;
					case 'about_hotkey':
						BLUEKING.hotkey.show();
						break;
					case 'help':
						BLUEKING.base.help();
						break;
					case 'video_course':
						window.open(BLUEKING.corefunc.get_external_links('video_course'), '_blank');
						break;
				}
			});
		},
		show: function(obj, offset_height){
			BLUEKING.popupMenu.hide();
			BLUEKING.folderView.hide();
			BLUEKING.searchbar.hide();
			obj.css({top : 'auto',left : 'auto',right : 'auto',bottom : 'auto'}).show();
			switch(BLUEKING.CONFIG.dockPos){
				case 'top':
					obj.css({
						top : $('#dock-container').height() - 1,
						right : $('#dock-container').offset().left
					});
					break;
				case 'left':
					obj.css({
						bottom : $('#dock-container').offset().top + offset_height,
						left : $('#dock-container').width() - 1
					});
					break;
				case 'right':
					obj.css({
						bottom : $('#dock-container').offset().top + offset_height,
						right : $('#dock-container').width() - 1
					});
					break;
			}
		},
		show_startmenu: function(){
			BLUEKING.docktool.show($('#startmenu-container'), 0);
		},
		hide_startmenu : function(){
			$('#startmenu-container').hide();
		},
		show_appearancemenu: function(){
			BLUEKING.docktool.show($('#appearancemenu-container'), 53);
		},
		hide_appearancemenu: function(){
			$('#appearancemenu-container').hide();
		},
		show_helpsmenu: function(){
			BLUEKING.docktool.show($('#helpsmenu-container'), 0);
		},
		hide_helpsmenu: function(){
			$('#helpsmenu-container').hide();
		},
		hide: function(){
			BLUEKING.docktool.hide_startmenu();
			BLUEKING.docktool.hide_appearancemenu();
			BLUEKING.docktool.hide_helpsmenu();
		}
	}
})();
