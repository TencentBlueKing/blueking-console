/*
**  应用码头
*/
BLUEKING.dock = (function(){
	return {
		/*
		**	初始化
		*/
		init : function(){
			BLUEKING.dock.getPos(function(){
				BLUEKING.dock.setPos();
			});
			//绑定应用码头拖动事件
			BLUEKING.dock.move();
			var dockShowtopFunc;
			$('#dock-container').on('mouseenter', function(){
				dockShowtopFunc = setTimeout(function(){
					$('#dock-container').addClass('showtop');
				}, 300);
			}).on('mouseleave', function(){
				clearInterval(dockShowtopFunc);
				$(this).removeClass('showtop');
			});
			// 应用码头 鼠标右键
			$('body').on('contextmenu', '#dock-container', function(e){
				BLUEKING.popupMenu.hide();
				BLUEKING.folderView.hide();
				BLUEKING.searchbar.hide();
				BLUEKING.docktool.hide();
				var popupmenu = BLUEKING.popupMenu.dock();
				var l = ($(window).width() - e.clientX) < popupmenu.width() ? (e.clientX - popupmenu.width()) : e.clientX;
				var t = ($(window).height() - e.clientY) < popupmenu.height() ? (e.clientY - popupmenu.height()) : e.clientY;
				popupmenu.css({
					left : l,
					top : t
				}).show();
				return false;
			});
			// 绑定dock上应用的点击事件
			// 打开应用市场
			$("#dock-container #market").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				BLUEKING.window.create_market();
			});
			// 打开个人中心
			$("#dock-container #user_center").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				BLUEKING.window.create_user_center();
			});
			// 打开统计
			$("#dock-container #app_statistics").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				BLUEKING.window.create_app_statistics();
			});
      // 打开权限中心
			$("#dock-container #bk_iam").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				BLUEKING.window.create_bk_iam();
			});
      // 打开用户管理
			$("#dock-container #bk_user_manage").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				BLUEKING.window.create_bk_user_manage();
			});
			// 打开开发者中心
			$("#dock-container #developer").on('mousedown', function(){
				return false;
			}).on('click', function(e){
				var dev_url = BLUEKING.corefunc.get_dev_url()
				window.open(dev_url, '_blank');
			});

			//全局视图
			$('#dock-bar .dock-tool-appmanage').on('mousedown', function(){
				return false;
			}).on('click',function(){
				BLUEKING.appmanage.set();
			});
			// 反馈
			$('#dock-bar .dock-tool-userce').on('mousedown', function(){
				return false;
			}).on('click',function(){
				window.open(BLUEKING.corefunc.get_external_links('community_forums'), '_blank');
			});
			//选择桌面
			$('#dock-bar .pagination').on('mousedown', function(){
				return false;
			}).on('click',function(){
				BLUEKING.dock.switchDesk($(this).attr('index'));
			});
			//头像菜单
			$('#dock-bar .dock-tool-start').on('mousedown', function(){
				return false;
			}).on('click', function(){
				BLUEKING.docktool.show_startmenu();
				return false;
			}).on('mouseover', function(){
				BLUEKING.DOCKTOOL_VAR.tool_start = true;
				BLUEKING.docktool.show_startmenu();
				return false;
			}).on('mouseout', function(){
				BLUEKING.DOCKTOOL_VAR.tool_start = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.startmenu_state && !BLUEKING.DOCKTOOL_VAR.tool_start){
						BLUEKING.docktool.hide_startmenu();
					}
				}, 200);
				return false;
			});
			//外观设置（主题设置，布局设置）
			$('#dock-bar .dock-tool-appearance').on('mousedown', function(){
				return false;
			}).on('click', function(){
				BLUEKING.docktool.show_appearancemenu();
				return false;
			}).on('mouseover', function(){
				BLUEKING.DOCKTOOL_VAR.tool_appearance = true;
				BLUEKING.docktool.show_appearancemenu();
				return false;
			}).on('mouseout', function(){
				BLUEKING.DOCKTOOL_VAR.tool_appearance = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.appearancemenu_state && !BLUEKING.DOCKTOOL_VAR.tool_appearance){
						BLUEKING.docktool.hide_appearancemenu();
					}
				}, 200);
				return false;
			});
			//帮助设置
			$('#dock-bar .dock-tool-helps').on('mousedown', function(){
				return false;
			}).on('click', function(){
				BLUEKING.docktool.show_helpsmenu();
				return false;
			}).on('mouseover', function(){
				BLUEKING.DOCKTOOL_VAR.tool_helps = true;
				BLUEKING.docktool.show_helpsmenu();
				return false;
			}).on('mouseout', function(){
				BLUEKING.DOCKTOOL_VAR.tool_helps = false;
				setTimeout(function(){
					if(!BLUEKING.DOCKTOOL_VAR.helpsmenu_state && !BLUEKING.DOCKTOOL_VAR.tool_helps){
						BLUEKING.docktool.hide_helpsmenu();
					}
				}, 200);
				return false;
			});
		},
		getPos : function(callback){
			$.ajax({
				type : 'POST',
				async:false,
				url : urlPrefix + 'get_dock_pos/',
				success : function(i){
					BLUEKING.CONFIG.dockPos = i;
					callback && callback();
				}
			});
		},
		setPos : function(){
			BLUEKING.dock.switchDesk(BLUEKING.CONFIG.desk);
			var desktop = $('#desk-' + BLUEKING.CONFIG.desk), desktops = $('#desk .desktop-container');
			var desk_w = desktop.css('width', '100%').width(), desk_h = desktop.css('height', '100%').height();
			//清除dock位置样式
			$('#dock-container').removeClass('dock-top dock-left dock-right');
			$('#dock-bar').removeClass('top-bar left-bar right-bar').hide();
			if(BLUEKING.CONFIG.dockPos == 'top'){
				$('#dock-bar').addClass('top-bar').children('#dock-container').addClass('dock-top');
				desktops.css({
					'width' : desk_w,
					'height' : desk_h - $('#task-bar').height() - $('#dock-bar').height(),
					'left' : desk_w,
					'top' : $('#dock-bar').height()
				});
				desktop.css({
					'left' : 0
				});
				$('#dock-bar').show();
			}else if(BLUEKING.CONFIG.dockPos == 'left'){
				$('#dock-bar').addClass('left-bar').children('#dock-container').addClass('dock-left');
				desktops.css({
					'width' : desk_w - $('#dock-bar').width(),
					'height' : desk_h - $('#task-bar').height(),
					'left' : desk_w + $('#dock-bar').width(),
					'top' : 0
				});
				desktop.css({
					'left' : $('#dock-bar').width()
				});
				$('#dock-bar').show();
			}else if(BLUEKING.CONFIG.dockPos == 'right'){
				$('#dock-bar').addClass('right-bar').children('#dock-container').addClass('dock-right');
				desktops.css({
					'width' : desk_w - $('#dock-bar').width(),
					'height' : desk_h - $('#task-bar').height(),
					'left' : desk_w,
					'top' : 0
				});
				desktop.css({
					'left' : 0
				});
				$('#dock-bar').show();
			}else if(BLUEKING.CONFIG.dockPos == 'none'){
				desktops.css({
					'width' : desk_w,
					'height' : desk_h - $('#task-bar').height(),
					'left' : desk_w,
					'top' : 0
				});
				desktop.css({
					'left' : 0
				});
			}
			BLUEKING.taskbar.resize();
			BLUEKING.folderView.setPos();
		},
		updatePos : function(pos){
			if(pos != BLUEKING.CONFIG.dockPos && typeof(pos) != 'undefined'){
				BLUEKING.CONFIG.dockPos = pos;
				//更新码头位置
				BLUEKING.dock.setPos();
				//更新桌面应用
				BLUEKING.app.set();
				$.ajax({
					type : 'POST',
					url : urlPrefix + 'set_dock_pos/' + pos + '/',
					success : function(){
					}
				});
			}
		},
		move : function(){
			$('#dock-container').on('mousedown',function(e){
				if(e.button == 0 || e.button == 1){
					var lay = BLUEKING.maskBox.dock(), location;
					$(document).on('mousemove', function(e){
						lay.show();
						if(e.clientY < lay.height() * 0.2){
							location = 'top';
						}else if(e.clientX < lay.width() * 0.5){
							location = 'left';
						}else{
							location = 'right';
						}
						$('.dock_drap_effect').removeClass('hover');
						$('.dock_drap_effect_' + location).addClass('hover');
					}).on('mouseup', function(){
						$(document).off('mousemove').off('mouseup');
						lay.hide();
						BLUEKING.dock.updatePos(location);
					});
				}
			});
		},
		/*
		**  切换桌面
		*/
		switchDesk : function(deskNumber){
			//验证传入的桌面号是否为1-5的正整数
			var r = /^\+?[1-5]*$/;
			deskNumber = r.test(deskNumber) ? deskNumber : 1;
			var pagination = $('#dock-bar .dock-pagination'), currindex = BLUEKING.CONFIG.desk, switchindex = deskNumber,
			currleft = $('#desk-' + currindex).offset().left, switchleft = $('#desk-' + switchindex).offset().left;
			if(currindex != switchindex){
				if(!$('#desk-' + switchindex).hasClass('animated') && !$('#desk-' + currindex).hasClass('animated')){
					$('#desk-' + currindex).addClass('animated').animate({
						left : switchleft
					}, 500, 'easeInOutCirc', function(){
						$(this).removeClass('animated');
					});
					$('#desk-'+switchindex).addClass('animated').animate({
						left : currleft
					}, 500, 'easeInOutCirc', function(){
						$(this).removeClass('animated');
						pagination.removeClass('current-pagination-' + currindex).addClass('current-pagination-' + switchindex);
						BLUEKING.CONFIG.desk = switchindex;
					});
				}
			}else{
				pagination.removeClass('current-pagination-' + currindex).addClass('current-pagination-' + switchindex);
			}
		}
	}
})();
