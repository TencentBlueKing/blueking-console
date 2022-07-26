/*
** 搜索框
*/
BLUEKING.marketSearchbox = (function(){
	return {
		/*
		** 初始化搜索框
		*/
		init: function(){
			// entry 按键
			$("#keyword").on('keyup', function(e){
				if(e.keyCode=='13'){
					$('#search_button').click();
				}
			});
			// 搜索按钮 点击事件绑定
			$("#search_button").on('click', function(){
				// 点击搜索时，隐藏app详情页
				BLUEKING.marketApp.closeDetailIframe();
				// 改变样式
				$('#scrollDiv ul li').removeClass('nav-active');
				$('.all').removeClass('app-all-on').addClass('app-all-on');
				$('.my').removeClass('app-my-on');
				$('.app-list-box .title ul').show();
				$('.app-list-box .title li').removeClass('focus').eq(0).addClass('focus');
				//顶部导航跳至1
				$('#topbar_select').val(1);
				//左侧导航跳至全部应用
				$('#sidebar_select').val(0);
				// 普通搜索
				BLUEKING.marketApp.getPageList(1, 2);
			});
		},
		/*
		** 清空搜索框
		*/
		clearSearchInput: function(){
			$("#keyword").val('');
		},
	}
})();
