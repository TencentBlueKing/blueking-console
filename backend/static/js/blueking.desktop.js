/*
**  桌面
*/
BLUEKING.deskTop = (function(){
	return {
		init : function(){
			//绑定浏览器resize事件
			$(window).on('resize', function(){
				BLUEKING.deskTop.resize();
			});
			$('body').on('click', '#desktop', function(){
				BLUEKING.popupMenu.hide();
				BLUEKING.folderView.hide();
				BLUEKING.searchbar.hide();
				BLUEKING.docktool.hide();
			}).on('contextmenu', '#desktop', function(e){
				BLUEKING.popupMenu.hide();
				BLUEKING.folderView.hide();
				BLUEKING.searchbar.hide();
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
		},
		/*
		**  处理浏览器改变大小后的事件
		*/
		resize : function(){
			if($('#desktop').is(':visible')){
				BLUEKING.dock.setPos();
				//更新应用定位
				BLUEKING.app.setPos();
				//更新窗口定位
				BLUEKING.window.setPos();
				//更新文件夹预览定位
				BLUEKING.folderView.setPos();
			}else{
				BLUEKING.appmanage.resize();
			}
			BLUEKING.wallpaper.set(false);
		}
	}
})();
