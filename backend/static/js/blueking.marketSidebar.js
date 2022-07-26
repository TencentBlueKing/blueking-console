/*
**  左右侧边栏，内容顶部导航
*/
BLUEKING.marketSidebar = (function(){
	return {
		/*
		** 侧边栏初始化
		*/
		init: function(){
			// 调整左侧边栏
			BLUEKING.marketSidebar.adjustLeftSidebar();
			// 右下角 跳转到开发者中心 我要开发点击事件绑定
			$("#dev_btn").on('click', function(){
				var dev_url = BLUEKING.corefunc.get_dev_url();
				window.open(dev_url, '_blank');
			});
			// 设置应用市场左侧导航
			$("#set_market_nav_btn").on('click', function(){
				$('#error_set').slideUp(200);
				var _show = $('#set_market_nav').is(':visible');
				if(_show){
					$('#set_market_nav').slideUp(200);
					$('#set_market_nav_btn').css('background','');
				}else{
					$('#set_market_nav').slideDown(200);
				}
				return false;
			});
			$('input[name="market_nav"]').click(function(){
				var market_nav = Number($('input[name="market_nav"]:checked').val());
				$.post(urlPrefix + 'set_market_nav/',{
					'market_nav': market_nav
				},function(data){
					if(data.result){
						// 设置成功，重新加载应用
						window.location.reload();
						// 隐藏设置
						$('#set_market_nav').slideUp(200);
						$('#error_set').hide();
					}else{
						$('#error_set').show();
					}
				}, 'json');
				return false;
			})
			//绑定分类, 全部应用和我的应用点击事件
			$('#scrollDiv ul li[_value], .all, .my').click(function(){
				//关闭应用详细页面iframe
				BLUEKING.marketApp.closeDetailIframe();
				// 修改点击导航的样式
				$('#scrollDiv ul li').removeClass('nav-active');
				$('.all').removeClass('app-all-on');
				$('.my').removeClass('app-my-on');
				if($(this).attr('id') == 'all'){
					$(this).addClass('app-all-on');
					$('.app-list-box .title ul').show();
				}else if($(this).attr('id') == 'my'){
					$(this).addClass('app-my-on');
					$('.app-list-box .title ul').hide();
				}
				else{
					$(this).addClass('nav-active');
					$('.app-list-box .title ul').show();
				}
				//左侧导航搜索值
				$('#sidebar_select').val($(this).attr('_value'));
				//顶部导航跳至第一项
				$('.app-list-box .title li').removeClass('focus');
				$('.app-list-box .title li[_value=1]').addClass('focus');
				$('#topbar_select').val(1);
				// 清空搜索条件
				BLUEKING.marketSearchbox.clearSearchInput();
				//请求搜索数据
				BLUEKING.marketApp.getPageList(1, 0);
			});
			//顶部导航点击
			$('.app-list-box .title li').click(function(){
				$('.app-list-box .title li').removeClass('focus');
				$(this).addClass('focus');
				$('#topbar_select').val($(this).attr('_value'));
				BLUEKING.marketApp.getPageList(1, 1);	//顶部导航搜索
			});
		},
		/*
		** 调整左侧边栏
		*/
		adjustLeftSidebar: function(){
			var scrollObj = $('#scrollDiv').find('ul'); //移动对象
			var scrollUnits = scrollObj.find('li'); //移动单位
			var unitLen = scrollUnits.eq(0).outerHeight(); //移动单位高度
			var viewH = $('#viewArea').outerHeight(); //可视区高度
			var btnPre = $('#btn-control-pre'); //上一个
			var btnNext = $('#btn-control-next'); //下一个
			// 判断栏目个数高度是否超过可视区
			if(scrollUnits.length*unitLen > viewH && unitLen <= 34){
				btnPre.addClass('btn-arrow-up-grey').css('cursor', 'default');
				btnPre.bind('click', function(){
					BLUEKING.marketSidebar.scrollUp(scrollUnits, unitLen, btnPre, btnNext);
				});
				btnNext.bind('click', function(){
					BLUEKING.marketSidebar.scrollDown(scrollUnits, unitLen, btnPre, btnNext);
				});
			}else{
				btnPre.addClass('btn-arrow-up-grey').css('cursor', 'default');
				btnNext.addClass('btn-arrow-down-grey').css('cursor', 'default');
			}
		},
		// 向上滚动
		scrollUp: function(scrollUnits, unitLen, btnPre, btnNext){
			var sTop = $('#viewArea').scrollTop();
			sTop -= unitLen;
			$('#viewArea').scrollTop(sTop);
			if($('#viewArea').scrollTop() == 0){
				btnPre.addClass('btn-arrow-up-grey').css('cursor', 'default');
				btnNext.removeClass('btn-arrow-down-grey').css('cursor', 'pointer');
			}else{
				btnPre.removeClass('btn-arrow-up-grey').css('cursor', 'pointer');
				btnNext.removeClass('btn-arrow-down-grey').css('cursor', 'pointer');
			}
		},
		// 向下滚动
		scrollDown: function(scrollUnits, unitLen, btnPre, btnNext){
			var sTop = $('#viewArea').scrollTop();
			sTop += unitLen;
			$('#viewArea').scrollTop(sTop);
			if(sTop && sTop >= (scrollUnits.length - 11)*unitLen){
				btnNext.addClass('btn-arrow-down-grey').css('cursor', 'default');
				btnPre.removeClass('btn-arrow-up-grey').css('cursor', 'pointer');
			}else{
				btnPre.removeClass('btn-arrow-up-grey').css('cursor', 'pointer');
				btnNext.removeClass('btn-arrow-down-grey').css('cursor', 'pointer');
			}
		}
	}
})();
