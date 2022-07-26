/*
**  应用
*/
BLUEKING.app = (function(){
	return {
		/*
		**  初始化桌面应用
		*/
		init : function(){
			//绑定'添加'点击事件
			$('#desk').on('click', 'li.add', function(e){
				BLUEKING.window.create_add_menu(e);
			});
			//绑定应用拖动事件
			BLUEKING.app.move();
			//绑定滚动条拖动事件
			BLUEKING.app.moveScrollbar();
			//绑定应用右击事件
			$('body').on('contextmenu', '.appbtn:not(.add)', function(e){
				BLUEKING.popupMenu.hide();
				BLUEKING.folderView.hide();
				BLUEKING.window.hide_add_menu();
				var popupmenu;
				switch($(this).attr('type')){
					case 'app':
						popupmenu = BLUEKING.popupMenu.app($(this));
						break;
					case 'folder':
						popupmenu = BLUEKING.popupMenu.folder($(this));
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
			$('body').on('contextmenu', '.appbtn_dock', function(e){
				BLUEKING.popupMenu.hide();
				BLUEKING.folderView.hide();
				BLUEKING.docktool.hide();
				var popupmenu = BLUEKING.popupMenu.desk();
				var l = ($(window).width() - e.clientX) < popupmenu.width() ? (e.clientX - popupmenu.width()) : e.clientX;
				var t = ($(window).height() - e.clientY) < popupmenu.height() ? (e.clientY - popupmenu.height()) : e.clientY;
				popupmenu.css({
					left : l,
					top : t
				}).show();
				return false;
			});
			//获取桌面应用数据
			BLUEKING.app.getXY(function(){
				BLUEKING.app.get();
			});
		},
		/*
		* 获得图标排列方式，x横向排列，y纵向排列
		*/
		getXY : function(callback){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_appxy/',
			}).done(function(i){
				BLUEKING.CONFIG.appXY = i;
				callback && callback();
			});
		},
		/*
		**  更新应用排列方式
		*/
		updateXY : function(i){
			if(BLUEKING.CONFIG.appXY != i){
				$.ajax({
					type : 'POST',
					url : urlPrefix + 'set_appxy/' + i + '/',
				}).done(function(){
					BLUEKING.CONFIG.appXY = i;
					BLUEKING.deskTop.resize();
				});
			}
		},
		/*
		**  获取桌面应用数据
		*/
		get : function(){
			//获取json数组并循环输出每个应用
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_my_app/',
				dataType : 'json',
				beforeSend : function(){
					BLUEKING.VAR.isAppMoving = true;
				}
			}).done(function(sc){
				BLUEKING.VAR.isAppMoving = false;
				if(typeof sc == 'object'){
					if(typeof sc['dock'] == 'object'){
						BLUEKING.VAR.dock = sc['dock'];
					}
					if(typeof sc['desk1'] == 'object'){
						BLUEKING.VAR.desk1 = sc['desk1'];
					}
					if(typeof sc['desk2'] == 'object'){
						BLUEKING.VAR.desk2 = sc['desk2'];
					}
					if(typeof sc['desk3'] == 'object'){
						BLUEKING.VAR.desk3 = sc['desk3'];
					}
					if(typeof sc['desk4'] == 'object'){
						BLUEKING.VAR.desk4 = sc['desk4'];
					}
					if(typeof sc['desk5'] == 'object'){
						BLUEKING.VAR.desk5 = sc['desk5'];
					}
					if(typeof sc['folder'] == 'object'){
						BLUEKING.VAR.folder = sc['folder'];
					}
				}
				//输出桌面应用
				BLUEKING.app.set(false);
			});
			//dock栏APP
			BLUEKING.app.setDockApp();
		},
		/*
		**  渲染桌面，输出应用
		*/
		set : function(isSetDock){
			//默认为true
			isSetDock = isSetDock == null ? true : isSetDock;
			//加载桌面应用
			for(var j = 1; j <= 5; j++){
				var desk_append = '';
				var desk = eval('BLUEKING.VAR.desk' + j);
				if(desk != ''){
					$(desk).each(function(){
						desk_append += appbtnTemp({
							'title' : this.name,
							'name' : this.name,
							'type' : this.type,
							'id' : 'd_' + this.appid,
							'appid' : this.appid,
							'code': this.app_code,
							'imgsrc' : this.icon,
							'isoutline': this.isoutline,
							'islapp': this.islapp
						});
					});
				}
				desk_append += addbtnTemp();
				$('#desk-' + j + ' li').remove();
				$('#desk-' + j + ' .desktop-apps-container').append(desk_append);
			}
			BLUEKING.app.setPos(false, isSetDock);
			//如果文件夹预览面板为显示状态，则进行更新
			$('body .quick_view_container').each(function(){
				BLUEKING.folderView.get($('#d_' + $(this).attr('appid')));
			});
			//如果文件夹窗口为显示状态，则进行更新
			$('#desk .folder-window').each(function(){
				BLUEKING.window.updateFolder($(this).attr('appid'));
			});
			//加载滚动条
			BLUEKING.app.getScrollbar();
		},
		setPos : function(isAnimate, isSetDock){
			isAnimate = isAnimate == null ? true : isAnimate;
			$('#desk').removeClass('smallIcon bigIcon');
			if(BLUEKING.CONFIG.appSize == 's'){
				$('#desk').addClass('smallIcon');
			}else if(BLUEKING.CONFIG.appSize == 'b'){
				$('#desk').addClass('bigIcon');
			}
			//是否设置dock栏
			//默认为true
			isSetDock = isSetDock == null ? true : isSetDock;
			if(isSetDock){
				BLUEKING.app.setDockApp();
			}
			var grid = BLUEKING.grid.getAppGrid();
			//设置桌面图标位置
			for(var j = 1; j <= 5; j++){
				$('#desk-' + j + ' li').each(function(i){
					var offsetTop, offsetLeft;
					switch(BLUEKING.CONFIG.appSize){
						case 's':
							offsetTop = 11;
							offsetLeft = 21;
							break;
						case 'b':
							offsetTop = 21;
							offsetLeft = 17;
							break;
						default:
							offsetTop = 7;
							offsetLeft = 16;
					}
					var top = grid[i]['startY'] + offsetTop;
					var left = grid[i]['startX'] + offsetLeft;
					$(this).stop(true, false).animate({
						'top' : top,
						'left' : left
					}, isAnimate ? 500 : 0);
					switch(BLUEKING.CONFIG.dockPos){
						case 'top':
							$(this).attr('left', left).attr('top', top + $('#dock-bar').height());
							break;
						case 'left':
							$(this).attr('left', left + $('#dock-bar').width()).attr('top', top);
							break;
						default:
							$(this).attr('left', left).attr('top', top);
					}
				});
			}
			//更新滚动条
			BLUEKING.app.getScrollbar();
		},
		/*
		 * 设置dock app
		 */
		setDockApp: function(){
			var times = 500;
			try{
				//IE下不加动画
				if($.browser.msie){
					var times = 0;
				}
			}catch(err){}
			var dockGrid = BLUEKING.grid.getDockAppGrid();
			//设置应用码头图标位置
			$('#dock-bar .dock-applist li').each(function(i){
				$(this).animate({
					'top' : BLUEKING.CONFIG.dockPos == 'top' ? dockGrid[i]['startY'] : dockGrid[i]['startY'] + 5,
					'left' : BLUEKING.CONFIG.dockPos == 'top' ? dockGrid[i]['startX'] + 5 : dockGrid[i]['startX']
				}, times).attr('top', $(this).offset().top).attr('left', $(this).offset().left);
			});
		},
		/*
		**  添加应用
		*/
		add : function(id, callback){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'add_my_app/' + id + '/',
				data : 'desk=' + BLUEKING.CONFIG.desk,
				success : function(msg){
					var msg = parseInt(msg);
					// 0:app添加失败，1：app添加成功，2：用户已经添加了该应用
					callback && callback.call(this, msg);
				}
			});
		},
		/*
		**  删除应用
		*/
		remove : function(id, callback){
			this.remove_new(id, function(data){
				if(data==1){
					callback && callback();
				}else if(data==2){
					ZENG.msgbox.show(gettext("文件夹中有存在的应用，不能删除！"), 1, 2000);
				}else if(data==3){
					ZENG.msgbox.show(gettext("您早就删除了该应用(或文件夹)，建议刷新桌面！"), 1, 3000);
					callback && callback();
				}else if(data==0){
					ZENG.msgbox.show(gettext('删除失败！'), 5, 2000);
				}
			});
		},
		remove_new : function(id, callback){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'del_my_app/' + id + '/',
				success : function(msg){
					var msg = parseInt(msg);
					callback && callback.call(this, msg);
				}
			});
		},
		/*
		**  应用拖动、打开
		**  这块代码略多，主要处理了9种情况下的拖动，分别是：
		**  桌面拖动到应用码头、桌面拖动到文件夹内、当前桌面上拖动(排序)
		**  应用码头拖动到桌面、应用码头拖动到文件夹内、应用码头上拖动(排序)
		**  文件夹内拖动到桌面、文件夹内拖动到应用码头、不同文件夹之间拖动
		*/
		move : function(){
			//应用码头应用拖动
			$('#dock-bar .dock-applist').on('mousedown', 'li', function(e){
				e.preventDefault();
				e.stopPropagation();
				if(e.button == 0 || e.button == 1){
					var oldobj = $(this);
					var obj = $('<li id="shortcut_shadow">' + oldobj.html() + '</li>');
					var dx = e.clientX;
					var dy = e.clientY;
					var cx = e.clientX;
					var cy = e.clientY;
					var x = dx - oldobj.offset().left;
					var y = dy - oldobj.offset().top;
					var lay = BLUEKING.maskBox.desk();
					//绑定鼠标移动事件
					$(document).on('mousemove', function(e){
						$('#desk').append(obj);
						lay.show();
						cx = e.clientX <= 0 ? 0 : e.clientX >= $(window).width() ? $(window).width() : e.clientX;
						cy = e.clientY <= 0 ? 0 : e.clientY >= $(window).height() ? $(window).height() : e.clientY;
						if(dx != cx || dy != cy){
							obj.css({
								left : cx - x,
								top : cy - y
							}).show();
						}
					}).on('mouseup', function(){
						$(document).off('mousemove').off('mouseup');
						obj.remove();
						lay.hide();
						//判断是否移动应用，如果没有则判断为click事件
						if(dx == cx && dy == cy){
							switch(oldobj.attr('type')){
								case 'app':
									BLUEKING.window.create(oldobj.attr('appid'));
									break;
								case 'folder':
									BLUEKING.folderView.get(oldobj);
									break;
							}
							return false;
						}
					});
				}
			});
			//桌面应用拖动
			$('#desktop .desktop-apps-container').on('mousedown', 'li:not(.add)', function(e){
				e.preventDefault();
				e.stopPropagation();
				if(e.button == 0 || e.button == 1){
					var oldobj = $(this);
					var obj = $('<li id="shortcut_shadow">' + oldobj.html() + '</li>');
					var dx = e.clientX;
					var dy = e.clientY;
					var cx = e.clientX;
					var cy = e.clientY;
					var x = dx - oldobj.offset().left;
					var y = dy - oldobj.offset().top;
					var lay = BLUEKING.maskBox.desk();
					//绑定鼠标移动事件
					$(document).on('mousemove', function(e){
						$('#desk').append(obj);
						lay.show();
						cx = e.clientX <= 0 ? 0 : e.clientX >= $(window).width() ? $(window).width() : e.clientX;
						cy = e.clientY <= 0 ? 0 : e.clientY >= $(window).height() ? $(window).height() : e.clientY;
						if(dx != cx || dy != cy){
							obj.css({
								left : cx - x,
								top : cy - y
							}).show();
						}
					}).on('mouseup', function(){
						$(document).off('mousemove').off('mouseup');
						obj.remove();
						lay.hide();
						//判断是否移动应用，如果没有则判断为click事件
						if(dx == cx && dy == cy){
							switch(oldobj.attr('type')){
								case 'app':
									BLUEKING.window.create(oldobj.attr('appid'));
									break;
								case 'folder':
									BLUEKING.folderView.get(oldobj);
									break;
							}
							return false;
						}
						var movegrid = BLUEKING.grid.searchFolderGrid(cx, cy);
						if(movegrid != null){
							if(oldobj.attr('type') != 'folder'){
								var id = oldobj.attr('appid');
								var from = oldobj.index();
								var to = movegrid;
								var desk = BLUEKING.CONFIG.desk;
								if(!BLUEKING.app.checkIsMoving()){
									if(BLUEKING.app.dataDeskToFolder(id, from, to, desk)){
										$.ajax({
											type : 'POST',
											url : urlPrefix + 'update_my_app/' + id + '/',
											data : 'movetype=desk-folder&from=' + from + '&to=' + to + '&desk=' + desk,
											success : function(){
												BLUEKING.VAR.isAppMoving = false;
											}
										});
									}
								}
							}
						}else{
							var dock_w = BLUEKING.CONFIG.dockPos == 'left' ? 0 : BLUEKING.CONFIG.dockPos == 'top' ? ($(window).width() - $('#dock-container').width() + 20) / 2 : $(window).width() - $('#dock-container').width();
							var dock_h = BLUEKING.CONFIG.dockPos == 'top' ? 0 : ($(window).height() - $('#dock-container').height() + 20) / 2;
							var movegrid = BLUEKING.grid.searchDockAppGrid(cx - dock_w, cy - dock_h);
							if(movegrid == null){
								var dock_w = BLUEKING.CONFIG.dockPos == 'left' ? $('#dock-bar').width() : 0;
								var dock_h = BLUEKING.CONFIG.dockPos == 'top' ? $('#dock-bar').height() : 0;
								var deskScrollLeft = $('#desk-' + BLUEKING.CONFIG.desk + ' .desktop-apps-container').scrollLeft();
								var deskScrollTop = $('#desk-' + BLUEKING.CONFIG.desk + ' .desktop-apps-container').scrollTop();
								var movegrid = BLUEKING.grid.searchAppGrid(cx - dock_w + deskScrollLeft, cy - dock_h + deskScrollTop);
								if(movegrid != null && movegrid != oldobj.index()){
									var movegrid2 = BLUEKING.grid.searchAppGrid2(cx - dock_w + deskScrollLeft, cy - dock_h + deskScrollTop);
									var id = oldobj.attr('appid');
									var from = oldobj.index();
									var to = movegrid;
									var boa = movegrid2 % 2 == 0 ? 'b' : 'a';
									var desk = BLUEKING.CONFIG.desk;
									if(!BLUEKING.app.checkIsMoving()){
										if(BLUEKING.app.dataDeskToDesk(id, from, to, boa, desk)){
											var a = from < to ? 0 : 1;
											var b = from < to ? -1 : 0;
											to = boa == 'a' ? (to + a): (to + b);
											$.ajax({
												type : 'POST',
												url : urlPrefix + 'update_my_app/' + id + '/',
												data : 'movetype=desk-desk&from=' + from + '&to=' + to + '&desk=' + desk,
												success : function(){
													BLUEKING.VAR.isAppMoving = false;
												}
											});
										}
									}
								}
							}
						}
					});
				}
			});
			//文件夹内应用拖动
			$('body').on('mousedown', '.folder_body li, .quick_view_container li', function(e){
				e.preventDefault();
				e.stopPropagation();
				if(e.button == 0 || e.button == 1){
					var oldobj = $(this);
					var obj = $('<li id="shortcut_shadow">' + oldobj.html() + '</li>');
					var dx = e.clientX;
					var dy = e.clientY;
					var cx = e.clientX;
					var cy = e.clientY;
					var x = dx - oldobj.offset().left;
					var y = dy - oldobj.offset().top;
					var lay = BLUEKING.maskBox.desk();
					//绑定鼠标移动事件
					$(document).on('mousemove', function(e){
						$('#desk').append(obj);
						lay.show();
						cx = e.clientX <= 0 ? 0 : e.clientX >= $(window).width() ? $(window).width() : e.clientX;
						cy = e.clientY <= 0 ? 0 : e.clientY >= $(window).height() ? $(window).height() : e.clientY;
						if(dx != cx || dy != cy){
							obj.css({
								left : cx - x,
								top : cy - y
							}).show();
						}
					}).on('mouseup', function(){
						$(document).off('mousemove').off('mouseup');
						obj.remove();
						lay.hide();
						//判断是否移动应用，如果没有则判断为click事件
						if(dx == cx && dy == cy){
							switch(oldobj.attr('type')){
								case 'app':
									BLUEKING.window.create(oldobj.attr('appid'));
									break;
							}
							return false;
						}
						var movegrid = BLUEKING.grid.searchFolderGrid(cx, cy);
						if(movegrid != null){
							if((oldobj.parents('.folder-window').attr('appid') || oldobj.parents('.quick_view_container').attr('appid')) != movegrid){
								var id = oldobj.attr('appid');
								var from = oldobj.index();
								var to = movegrid;
								var fromFolderId = oldobj.parents('.folder-window').attr('appid') || oldobj.parents('.quick_view_container').attr('appid');
								if(!BLUEKING.app.checkIsMoving()){
									if(BLUEKING.app.dataFolderToFolder(id, from, to, fromFolderId)){
										$.ajax({
											type : 'POST',
											url : urlPrefix + 'update_my_app/' + id + '/',
											data : 'movetype=folder-otherfolder&to=' + to,
											success : function(){
												BLUEKING.VAR.isAppMoving = false;
											}
										});
									}
								}
							}
						}else{
							var dock_w = BLUEKING.CONFIG.dockPos == 'left' ? 0 : BLUEKING.CONFIG.dockPos == 'top' ? ($(window).width() - $('#dock-container').width() + 20) / 2 : $(window).width() - $('#dock-container').width();
							var dock_h = BLUEKING.CONFIG.dockPos == 'top' ? 0 : ($(window).height() - $('#dock-container').height() + 20) / 2;
							var movegrid = BLUEKING.grid.searchDockAppGrid(cx - dock_w, cy - dock_h);
							if(movegrid == null){
								var dock_w = BLUEKING.CONFIG.dockPos == 'left' ? $('#dock-bar').width() : 0;
								var dock_h = BLUEKING.CONFIG.dockPos == 'top' ? $('#dock-bar').height() : 0;
								var deskScrollLeft = $('#desk-' + BLUEKING.CONFIG.desk + ' .desktop-apps-container').scrollLeft();
								var deskScrollTop = $('#desk-' + BLUEKING.CONFIG.desk + ' .desktop-apps-container').scrollTop();
								var movegrid = BLUEKING.grid.searchAppGrid(cx - dock_w + deskScrollLeft, cy - dock_h + deskScrollTop);
								if(movegrid != null){
									var movegrid2 = BLUEKING.grid.searchAppGrid2(cx - dock_w + deskScrollLeft, cy - dock_h + deskScrollTop);
									var id = oldobj.attr('appid');
									var from = oldobj.index();
									var to = movegrid;
									var fromFolderId = oldobj.parents('.folder-window').attr('appid') || oldobj.parents('.quick_view_container').attr('appid');
									var boa = movegrid2 % 2 == 0 ? 'b' : 'a';
									var desk = BLUEKING.CONFIG.desk;
									if(!BLUEKING.app.checkIsMoving()){
										if(BLUEKING.app.dataFolderToDesk(id, from, to, fromFolderId, boa, desk)){
											to = boa == 'a' ? (to + 1) : to;
											$.ajax({
												type : 'POST',
												url : urlPrefix + 'update_my_app/' + id + '/',
												data : 'movetype=folder-desk&to=' + to + '&desk=' + desk,
												success : function(){
													BLUEKING.VAR.isAppMoving = false;
												}
											});
										}
									}
								}
							}
						}
					});
				}
			});
		},
		/*
		**  加载滚动条
		*/
		getScrollbar : function(){
			setTimeout(function(){
				$('#desk .desktop-container').each(function(){
					var desk = $(this).children('.desktop-apps-container'), scrollbar = $(this).children('.scrollbar');
					var scrollbarLeft = desk.nextAll('.scrollbar-x').position().left, scrollbarTop = desk.nextAll('.scrollbar-y').position().top;
					//先清空所有附加样式
					scrollbar.hide();
					desk.scrollLeft(0).scrollTop(0);
					/*
					**  判断应用排列方式
					**  横向排列超出屏幕则出现纵向滚动条，纵向排列超出屏幕则出现横向滚动条
					*/
					if(BLUEKING.CONFIG.appXY == 'x'){
						/*
						**  获得桌面应用定位好后的实际高度
						**  因为显示的高度是固定的，而实际的高度是根据应用个数会变化
						*/
						var deskH = parseInt(desk.children('.add').css('top')) + 108;
						/*
						**  计算滚动条高度
						**  高度公式（应用纵向排列计算滚动条宽度以此类推）：
						**  滚动条实际高度 = 桌面显示高度 / 桌面实际高度 * 滚动条总高度(桌面显示高度)
						**  如果“桌面显示高度 / 桌面实际高度 >= 1”说明应用个数未能超出桌面，则不需要出现滚动条
						*/
						if(desk.height() / deskH < 1){
							desk.nextAll('.scrollbar-y').height(desk.height() / deskH * desk.height());
							scrollbarTop = scrollbarTop + desk.nextAll('.scrollbar-y').height() > desk.height() ? desk.height() - desk.nextAll('.scrollbar-y').height() : scrollbarTop;
							desk.nextAll('.scrollbar-y').css('top', scrollbarTop).show();
							desk.scrollTop(scrollbarTop / desk.height() * deskH);
						}
					}else{
						var deskW = parseInt(desk.children('.add').css('left')) + 106;
						if(desk.width() / deskW < 1){
							desk.nextAll('.scrollbar-x').width(desk.width() / deskW * desk.width());
							scrollbarLeft = scrollbarLeft + desk.nextAll('.scrollbar-x').width() > desk.width() ? desk.width() - desk.nextAll('.scrollbar-w').width() : scrollbarLeft;
							desk.nextAll('.scrollbar-x').css('left', scrollbarLeft).show();
							desk.scrollLeft(scrollbarLeft / desk.width() * deskW);
						}
					}
				});
			}, 500);
		},
		/*
		**  移动滚动条
		*/
		moveScrollbar : function(){
			/*
			**  手动拖动
			*/
			$('#desk .scrollbar').on('mousedown', function(e){
				var x, y, cx, cy, deskrealw, deskrealh, movew, moveh;
				var scrollbar = $(this), desk = scrollbar.prevAll('.desktop-apps-container');
				deskrealw = parseInt(desk.children('.add').css('left')) + 106;
				deskrealh = parseInt(desk.children('.add').css('top')) + 108;
				movew = desk.width() - scrollbar.width();
				moveh = desk.height() - scrollbar.height();
				if(scrollbar.hasClass('scrollbar-x')){
					x = e.clientX - scrollbar.position().left;
				}else{
					y = e.clientY - scrollbar.position().top;
				}
				$(document).on('mousemove', function(e){
					if(scrollbar.hasClass('scrollbar-x')){
						cx = e.clientX - x < 0 ? 0 : e.clientX - x > movew ? movew : e.clientX - x;
						scrollbar.css('left', cx);
						desk.scrollLeft(cx / desk.width() * deskrealw);
					}else{
						cy = e.clientY - y < 0 ? 0 : e.clientY - y > moveh ? moveh : e.clientY - y;
						scrollbar.css('top', cy);
						desk.scrollTop(cy / desk.height() * deskrealh);
					}
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
				});
			});
			/*
			**  鼠标滚动
			*/
			for(var i = 1; i <= 5; i++){
				$('#desk-' + i).on('mousewheel', function(event, delta){
					var desk = $(this).find('.desktop-apps-container');
					if(BLUEKING.CONFIG.appXY == 'x'){
						var deskrealh = parseInt(desk.find('.add').css('top')) + 108, scrollupdown;
						/*
						**  delta == -1   往下
						**  delta == 1    往上
						**  200px 是鼠标滚轮每滚一次的距离
						*/
						if(delta < 0){
							scrollupdown = desk.scrollTop() + 200 > deskrealh - desk.height() ? deskrealh - desk.height() : desk.scrollTop() + 200;
						}else{
							scrollupdown = desk.scrollTop() - 200 < 0 ? 0 : desk.scrollTop() - 200;
						}
						desk.stop(false, true).animate({scrollTop : scrollupdown}, 300);
						desk.nextAll('.scrollbar-y').stop(false, true).animate({
							top : scrollupdown / deskrealh * desk.height()
						}, 300);
					}else{
						var deskrealw = parseInt(desk.find('.add').css('left')) + 106, scrollleftright;
						if(delta < 0){
							scrollleftright = desk.scrollLeft() + 200 > deskrealw - desk.width() ? deskrealw - desk.width() : desk.scrollLeft() + 200;
						}else{
							scrollleftright = desk.scrollLeft() - 200 < 0 ? 0 : desk.scrollLeft() - 200;
						}
						desk.stop(false, true).animate({scrollLeft : scrollleftright}, 300);
						desk.nextAll('.scrollbar-x').stop(false, true).animate({
							left : scrollleftright / deskrealw * desk.width()
						}, 300);
					}
				});
			}
		},
		checkIsMoving : function(){
			var rtn = false;
			if(BLUEKING.VAR.isAppMoving){
				$.dialog({
					title : gettext('温馨提示'),
					icon : 'warning',
					content : gettext('数据正在处理中，请稍后。'),
					ok : true
				});
				rtn = true;
			}else{
				BLUEKING.VAR.isAppMoving = true;
			}
			return rtn;
		},
		dataWarning : function(){
			$.dialog({
				title : gettext('温馨提示'),
				icon : 'warning',
				content : gettext('数据错误，请刷新后重试。'),
				ok : true
			});
		},
		dataDockToFolder : function(id, from, to){
			var rtn = false;
			$(BLUEKING.VAR.dock).each(function(i){
				if(this.appid == id){
					$(BLUEKING.VAR.folder).each(function(j){
						if(this.appid == to){
							BLUEKING.VAR.folder[j].apps.push(BLUEKING.VAR.dock[i]);
							BLUEKING.VAR.folder[j].apps = BLUEKING.VAR.folder[j].apps.sortBy(function(n){
								return n.appid;
							}, true);
							BLUEKING.VAR.dock.splice(i, 1);
							rtn = true;
							return false;
						}
					});
					return false;
				}
			});
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDockToDock : function(id, from, to, boa){
			var rtn = false;
			if(BLUEKING.VAR.dock[from] != null){
				if(to == 0){
					if(boa == 'b'){
						BLUEKING.VAR.dock.splice(0, 0, BLUEKING.VAR.dock[from]);
					}else{
						BLUEKING.VAR.dock.splice(1, 0, BLUEKING.VAR.dock[from]);
					}
				}else{
					if(boa == 'b'){
						BLUEKING.VAR.dock.splice(to, 0, BLUEKING.VAR.dock[from]);
					}else{
						BLUEKING.VAR.dock.splice(to + 1, 0, BLUEKING.VAR.dock[from]);
					}
				}
				if(from > to){
					BLUEKING.VAR.dock.splice(from + 1, 1);
				}else{
					BLUEKING.VAR.dock.splice(from, 1);
				}
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDockToDesk : function(id, from, to, boa, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			if(BLUEKING.VAR.dock[from] != null){
				if(to == 0){
					if(boa == 'b'){
						desk.splice(0, 0, BLUEKING.VAR.dock[from]);
					}else{
						desk.splice(1, 0, BLUEKING.VAR.dock[from]);
					}
				}else{
					if(boa == 'b'){
						desk.splice(to, 0, BLUEKING.VAR.dock[from]);
					}else{
						desk.splice(to + 1, 0, BLUEKING.VAR.dock[from]);
					}
				}
				BLUEKING.VAR.dock.splice(from, 1);
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDockToOtherdesk : function(id, from, todesk){
			var rtn = false;
			todesk = eval('BLUEKING.VAR.desk' + todesk);
			if(BLUEKING.VAR.dock[from] != null){
				todesk.push(BLUEKING.VAR.dock[from]);
				BLUEKING.VAR.dock.splice(from, 1);
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDockToDelete : function(id, from){
			var rtn = false;
			if(BLUEKING.VAR.dock[from] != null){
				BLUEKING.VAR.dock.splice(from, 1);
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDeskToFolder : function(id, from, to, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			$(BLUEKING.VAR.folder).each(function(i){
				if(this.appid == to && desk[from] != null){
					BLUEKING.VAR.folder[i].apps.push(desk[from]);
					BLUEKING.VAR.folder[i].apps = BLUEKING.VAR.folder[i].apps.sortBy(function(n){
						return n.appid;
					}, true);
					desk.splice(from, 1);
					rtn = true;
					return false;
				}
			});
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDeskToDock : function(id, from, to, boa, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			if(desk[from] != null){
				if(to == 0){
					if(boa == 'b'){
						BLUEKING.VAR.dock.splice(0, 0, desk[from]);
					}else{
						BLUEKING.VAR.dock.splice(1, 0, desk[from]);
					}
				}else{
					if(boa == 'b'){
						BLUEKING.VAR.dock.splice(to, 0, desk[from]);
					}else{
						BLUEKING.VAR.dock.splice(to + 1, 0, desk[from]);
					}
				}
				desk.splice(from, 1);
				if(BLUEKING.VAR.dock.length > 7){
					desk.push(BLUEKING.VAR.dock[7]);
					BLUEKING.VAR.dock.splice(7, 1);
				}
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDeskToDesk : function(id, from, to, boa, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			if(desk[from] != null){
				if(to == 0){
					if(boa == 'b'){
						desk.splice(0, 0, desk[from]);
					}else{
						desk.splice(1, 0, desk[from]);
					}
				}else{
					if(boa == 'b'){
						desk.splice(to, 0, desk[from]);
					}else{
						desk.splice(to + 1, 0, desk[from]);
					}
				}
				if(from > to){
					desk.splice(from + 1, 1);
				}else{
					desk.splice(from, 1);
				}
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataDeskToOtherdesk : function(id, from, to, boa, todesk, fromdesk){
			var rtn = false;
			fromdesk = eval('BLUEKING.VAR.desk' + fromdesk);
			todesk = eval('BLUEKING.VAR.desk' + todesk);
			if(fromdesk[from] != null){
				if(to == 0){
					if(boa == 'b'){
						todesk.splice(0, 0, fromdesk[from]);
					}else{
						todesk.splice(1, 0, fromdesk[from]);
					}
				}else{
					if(boa == 'b'){
						todesk.splice(to, 0, fromdesk[from]);
					}else{
						todesk.splice(to + 1, 0, fromdesk[from]);
					}
				}
				fromdesk.splice(from, 1);
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataFolderToFolder : function(id, from, to, fromFolderId){
			var rtn = false, flags = 0, fromKey, toKey;
			$(BLUEKING.VAR.folder).each(function(i){
				if(this.appid == fromFolderId && BLUEKING.VAR.folder[i].apps[from] != null){
					fromKey = i;
					flags += 1;
				}
				if(this.appid == to){
					toKey = i;
					flags += 1;
				}
			});
			if(flags== 2){
				BLUEKING.VAR.folder[toKey].apps.push(BLUEKING.VAR.folder[fromKey].apps[from]);
				BLUEKING.VAR.folder[toKey].apps = BLUEKING.VAR.folder[toKey].apps.sortBy(function(n){
					return n.appid;
				}, true);
				BLUEKING.VAR.folder[fromKey].apps.splice(from, 1);
				rtn = true;
			}
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataFolderToDock : function(id, from, to, fromFolderId, boa, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			$(BLUEKING.VAR.folder).each(function(i){
				if(this.appid == fromFolderId && BLUEKING.VAR.folder[i].apps[from] != null){
					if(to == 0){
						if(boa == 'b'){
							BLUEKING.VAR.dock.splice(0, 0, BLUEKING.VAR.folder[i].apps[from]);
						}else{
							BLUEKING.VAR.dock.splice(1, 0, BLUEKING.VAR.folder[i].apps[from]);
						}
					}else{
						if(boa == 'b'){
							BLUEKING.VAR.dock.splice(to, 0, BLUEKING.VAR.folder[i].apps[from]);
						}else{
							BLUEKING.VAR.dock.splice(to + 1, 0, BLUEKING.VAR.folder[i].apps[from]);
						}
					}
					BLUEKING.VAR.folder[i].apps.splice(from, 1);
					if(BLUEKING.VAR.dock.length > 7){
						desk.push(BLUEKING.VAR.dock[7]);
						BLUEKING.VAR.dock.splice(7, 1);
					}
					rtn = true;
					return false;
				}
			});
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataFolderToDesk : function(id, from, to, fromFolderId, boa, desk){
			var rtn = false;
			desk = eval('BLUEKING.VAR.desk' + desk);
			$(BLUEKING.VAR.folder).each(function(i){
				if(this.appid == fromFolderId && BLUEKING.VAR.folder[i].apps[from] != null){
					if(to == 0){
						if(boa == 'b'){
							desk.splice(0, 0, BLUEKING.VAR.folder[i].apps[from]);
						}else{
							desk.splice(1, 0, BLUEKING.VAR.folder[i].apps[from]);
						}
					}else{
						if(boa == 'b'){
							desk.splice(to, 0, BLUEKING.VAR.folder[i].apps[from]);
						}else{
							desk.splice(to + 1, 0, BLUEKING.VAR.folder[i].apps[from]);
						}
					}
					BLUEKING.VAR.folder[i].apps.splice(from, 1);
					rtn = true;
					return false;
				}
			});
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataFolderToOtherdesk : function(id, from, todesk, fromFolderId){
			var rtn = false;
			todesk = eval('BLUEKING.VAR.desk' + todesk);
			$(BLUEKING.VAR.folder).each(function(i){
				if(this.appid == fromFolderId && BLUEKING.VAR.folder[i].apps[from] != null){
					todesk.push(BLUEKING.VAR.folder[i].apps[from]);
					BLUEKING.VAR.folder[i].apps.splice(from, 1);
					rtn = true;
					return false;
				}
			});
			if(rtn){
				if($('#desktop').is(':visible')){
					BLUEKING.app.set();
				}else{
					BLUEKING.appmanage.set();
				}
			}else{
				BLUEKING.app.dataWarning();
			}
			return rtn;
		},
		dataAllDockToDesk : function(desk){
			desk = eval('BLUEKING.VAR.desk' + desk);
			$(BLUEKING.VAR.dock).each(function(i){
				desk.push(BLUEKING.VAR.dock[i]);
			});
			BLUEKING.VAR.dock.splice(0, BLUEKING.VAR.dock.length);
		},
		dataDeleteByAppid : function(appid){
			$(BLUEKING.VAR.dock).each(function(i){
				if(this.appid == appid){
					BLUEKING.VAR.dock.splice(i, 1);
					return false;
				}
			});
			for(var i = 1; i <= 5; i++){
				var desk = eval('BLUEKING.VAR.desk' + i);
				$(desk).each(function(j){
					if(this.appid == appid){
						desk.splice(j, 1);
						if(this.type == 'folder'){
							$(BLUEKING.VAR.folder).each(function(k){
								if(this.appid == appid){
									BLUEKING.VAR.folder.splice(k, 1);
									return false;
								}
							});
						}
						return false;
					}
				});
			}
			$(BLUEKING.VAR.folder).each(function(i){
				$(this.apps).each(function(j){
					if(this.appid == appid){
						BLUEKING.VAR.folder[i].apps.splice(j, 1);
						return false;
					}
				});
			});
		}
	}
})();
