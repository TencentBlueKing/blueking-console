/*
**  任务栏
*/
BLUEKING.taskbar = (function(){
	return {
		/*
		**  初始化
		*/
		init : function(){
			//当浏览器窗口改变大小时，任务栏的显示也需进行刷新
			$(window).on('resize', function(){
				BLUEKING.taskbar.resize();
			});
			//绑定任务栏点击事件
			BLUEKING.taskbar.click();
			//绑定任务栏前进后退按钮事件
			BLUEKING.taskbar.pageClick();
		},
		click : function(){
			$('#task-content-inner').on('click', 'a.task-item', function(){
				if($(this).hasClass('task-item-current')){
					BLUEKING.window.hide($(this).attr('appid'));
				}else{
					BLUEKING.window.show2top($(this).attr('appid'));
				}
			}).on('contextmenu', 'a.task-item', function(e){
				$('.popup-menu').hide();
				$('.quick_view_container').remove();
				var popupmenu = BLUEKING.popupMenu.task($(this));
				var l = $(window).width() - e.clientX < popupmenu.width() ? e.clientX - popupmenu.width() : e.clientX;
				var t = e.clientY - popupmenu.height();
				popupmenu.css({
					left : l,
					top : t
				}).show();
				return false;
			});
		},
		pageClick : function(){
			$('#task-next-btn').on('click', function(){
				if($(this).hasClass('disable') == false){
					var w = $('#task-bar').width(), realW = $('#task-content-inner .task-item').length * 114, showW = w - 112, overW = realW - showW;
					var marginL = parseInt($('#task-content-inner').css('margin-left')) - 114;
					if(marginL <= overW * -1){
						marginL = overW * -1;
						$('#task-next a').addClass('disable');
					}
					$('#task-pre a').removeClass('disable');
					$('#task-content-inner').animate({
						marginLeft : marginL
					}, 200);
				}
			});
			$('#task-pre-btn').on('click', function(){
				if($(this).hasClass('disable') == false){
					var marginL = parseInt($('#task-content-inner').css('margin-left')) + 114;
					if(marginL >= 0){
						marginL = 0;
						$('#task-pre a').addClass('disable');
					}
					$('#task-next a').removeClass('disable');
					$('#task-content-inner').animate({
						marginLeft : marginL
					}, 200);
				}
			});
		},
		resize : function(){
			$('#task-content-inner').removeClass('fl');
			if(BLUEKING.CONFIG.dockPos == 'left'){
				$('#task-bar').css({
					'left' : $('#dock-bar').width(),
					'right' : 0
				});
			}else if(BLUEKING.CONFIG.dockPos == 'right'){
				$('#task-bar').css({
					'left' : 0,
					'right' : $('#dock-bar').width()
				});
				$('#task-content-inner').addClass('fl');
			}else{
				$('#task-bar').css({
					'left' : 0,
					'right' : 0
				});
			}
			var w = $('#task-bar').width(), realW = $('#task-content-inner .task-item').length * 114, showW = w - 112;
			$('#task-content-inner').css('width', realW);
			if(realW >= showW){
				$('#task-next, #task-pre').show();
				$('#task-content').css('width', showW);
				$('#task-content-inner').addClass('fl').stop(true, false).animate({
					marginLeft : 0
				}, 200);
				$('#task-next a').removeClass('disable');
				$('#task-pre a').addClass('disable');
			}else{
				$('#task-next, #task-pre').hide();
				$('#task-content').css('width','100%');
				$('#task-content-inner').css({
					'margin-left' : 0,
					'margin-right' : 0
				});
			}
		}
	}
})();
