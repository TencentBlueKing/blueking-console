/*
**  皮肤设置应用
*/
BLUEKING.skinApp = (function(){
	return {
		/*
		**	初始化
		*/
		init : function(){
			$('.skin li').on('click', function(){
				$('.skin li').removeClass('selected');
				$(this).addClass('selected');
				var skin = $(this).attr('skin');
				$.ajax({
					url : urlPrefix + 'set_skin/' + skin + '/',
					success : function(){
						window.parent.ZENG.msgbox.show(gettext("设置成功，正在切换皮肤，如果长时间没更新，请刷新页面"), 4, 5000);
						window.parent.BLUEKING.base.setSkin(skin, function(){
							window.parent.ZENG.msgbox._hide();
						});
					}
				});
			});
		}
	}
})();
