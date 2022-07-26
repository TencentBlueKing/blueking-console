/*
**  全局视图
*/
BLUEKING.appmanage = (function(){
	return {
		/*
		**  初始化
		*/
		init : function(){
			$('#appmanage .amg_close').off('click').on('click', function(){
				BLUEKING.appmanage.close();
			});
			$('#amg_folder_container').on('contextmenu', '.appbtn', function(){
				return false;
			});
			BLUEKING.appmanage.move();
			BLUEKING.appmanage.moveScrollbar();
		},
		set : function(){
			$('#desktop').hide();
			$('#appmanage').show();
			$('#amg_folder_container .folderItem').show().addClass('folderItem_turn');
			$('#amg_folder_container .folderInner').height($(window).height() - 80);
			//加载应用码头应用
			$('#amg_dock_container').html('').append($('#dock-container .dock-applist li').clone());
			//加载桌面应用
			for(var j = 0; j < 5; j++){
				var desk_append = '', desk = eval('BLUEKING.VAR.desk' + (j + 1));
				if(desk != ''){
					$(desk).each(function(i){
						desk_append += appbtnTemp({
							'title' : this.name,
							'name': this.name,
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
				$('#amg_folder_container .folderItem:eq(' + j + ') .folderInner').html(desk_append);
			}
			BLUEKING.appmanage.setPos();
			BLUEKING.appmanage.getScrollbar();
		},
		setPos : function(){
			var manageDockGrid = BLUEKING.grid.getManageDockAppGrid(), manageAppGrid = BLUEKING.grid.getManageAppGrid();
			$('#amg_dock_container li').each(function(i){
				$(this).css({
					'top' : 10,
					'left' : manageDockGrid[i]['startX'] + 6
				});
			});
			for(var j = 0; j < 5; j++){
				$('#amg_folder_container .folderItem:eq(' + j + ') .folderInner li').each(function(i){
					$(this).css({
						'top' : manageAppGrid[i]['startY'] + 5,
						'left' : 0
					});
				});
			}
		},
		move : function(){
			$('#amg_dock_container').on('mousedown', 'li', function(e){
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
						$('body').append(obj);
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
							BLUEKING.appmanage.close();
							// todo 打开系统工具应用
							$("#dock-container .dock-applist > li[id='"+ oldobj.attr('id') +"']").click();
						}
					});
				}
				return false;
			});
			$('#amg_folder_container').on('mousedown', 'li.appbtn:not(.add)', function(e){
				e.preventDefault();
				e.stopPropagation();
				if(e.button == 0 || e.button == 1){
					var oldobj = $(this);
					var obj = $('<li id="shortcut_shadow2">' + oldobj.html() + '</li>');
					var dx = e.clientX;
					var dy = e.clientY;
					var cx = e.clientX;
					var cy = e.clientY;
					var x = dx - oldobj.offset().left;
					var y = dy - oldobj.offset().top;
					var lay = BLUEKING.maskBox.desk();
					//绑定鼠标移动事件
					$(document).on('mousemove', function(e){
						$('body').append(obj);
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
							BLUEKING.appmanage.close();
							switch(oldobj.attr('type')){
								case 'app':
								case 'folder':
									BLUEKING.window.create(oldobj.attr('appid'));
									break;
							}
							return false;
						}
						if(cy > 80){
							var movedesk = parseInt(cx / ($(window).width() / 5));
							var movegrid = BLUEKING.grid.searchManageAppGrid(cy - 80 + $('#amg_folder_container .folderItem:eq(' + movedesk + ') .folderInner').scrollTop());
							//判断是在同一桌面移动，还是跨桌面移动
							if(movedesk + 1 == oldobj.parent().attr('desk')){
								if(movegrid != null && movegrid != oldobj.index()){
									var movegrid2 = BLUEKING.grid.searchManageAppGrid2(cy - 80 + $('#amg_folder_container .folderItem:eq(' + movedesk + ') .folderInner').scrollTop());
									var id = oldobj.attr('appid');
									var from = oldobj.index();
									var to = movegrid;
									var boa = movegrid2 % 2 == 0 ? 'b' : 'a';
									var desk = movedesk + 1;
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
							}else{
								if(movegrid != null){
									var movegrid2 = BLUEKING.grid.searchManageAppGrid2(cy - 80 + $('#amg_folder_container .folderItem:eq(' + movedesk + ') .folderInner').scrollTop());
									var id = oldobj.attr('appid');
									var from = oldobj.index();
									var to = movegrid;
									var boa = movegrid2 % 2 == 0 ? 'b' : 'a';
									var todesk = movedesk + 1;
									var fromdesk = oldobj.parent().attr('desk');
									if(!BLUEKING.app.checkIsMoving()){
										if(BLUEKING.app.dataDeskToOtherdesk(id, from, to, boa, todesk, fromdesk)){
											to = boa == 'a' ? (to + 1) : to;
											$.ajax({
												type : 'POST',
												url : urlPrefix + 'update_my_app/' + id + '/',
												data : 'movetype=desk-otherdesk&from=' + from + '&to=' + to + '&desk=' + fromdesk + '&otherdesk=' + todesk,
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
				return false;
			});
		},
		getScrollbar : function(){
			$('#amg_folder_container .folderInner').height($(window).height() - 80);
			$('#amg_folder_container .folderItem').each(function(){
				var desk = $(this).find('.folderInner'), deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41, scrollbar = desk.next('.scrollBar');
				//记录下滚动条更新前的位置，用于更新后的复原
				var scrollbarTop = scrollbar.position().top;
				//先清空所有附加样式
				scrollbar.hide();
				desk.scrollTop(0);
				if(desk.height() / deskrealh < 1){
					scrollbar.height(desk.height() / deskrealh * desk.height());
					scrollbarTop = scrollbarTop + scrollbar.height() > desk.height() ? desk.height() - scrollbar.height() : scrollbarTop;
					scrollbar.css('top', scrollbarTop).show();
					desk.scrollTop(scrollbarTop / desk.height() * deskrealh);
				}
			});
		},
		moveScrollbar : function(){
			/*
			**  手动拖动
			*/
			$('.scrollBar').on('mousedown', function(e){
				var y, cy, deskrealh, moveh;
				var scrollbar = $(this), desk = scrollbar.prev('.folderInner');
				deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41;
				moveh = desk.height() - scrollbar.height();
				y = e.clientY - scrollbar.offset().top;
				$(document).on('mousemove', function(e){
					//减80px是因为顶部dock区域的高度为80px，所以计算移动距离需要先减去80px
					cy = e.clientY - y - 80 < 0 ? 0 : e.clientY - y - 80 > moveh ? moveh : e.clientY - y - 80;
					scrollbar.css('top', cy);
					desk.scrollTop(cy / desk.height() * deskrealh);
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
				});
			});
			/*
			**  鼠标滚轮
			*/
			$('#amg_folder_container .folderInner').on('mousewheel', function(event, delta){
				var desk = $(this), deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41, scrollupdown;
				/*
				**  delta == -1   往下
				**  delta == 1    往上
				*/
				if(delta < 0){
					scrollupdown = desk.scrollTop() + 120 > deskrealh - desk.height() ? deskrealh - desk.height() : desk.scrollTop() + 120;
				}else{
					scrollupdown = desk.scrollTop() - 120 < 0 ? 0 : desk.scrollTop() - 120;
				}
				desk.stop(false, true).animate({
					scrollTop : scrollupdown
				}, 300);
				desk.next('.scrollBar').stop(false, true).animate({
					top : scrollupdown / deskrealh * desk.height()
				}, 300);
			});
		},
		resize : function(){
			BLUEKING.appmanage.getScrollbar();
		},
		close : function(){
			$('#amg_dock_container').html('');
			$('#amg_folder_container .folderInner').html('');
			$('#desktop').show();
			$('#appmanage').hide();
			$('#amg_folder_container .folderItem').removeClass('folderItem_turn');
			BLUEKING.app.set();
			BLUEKING.deskTop.resize();
		}
	}
})();
