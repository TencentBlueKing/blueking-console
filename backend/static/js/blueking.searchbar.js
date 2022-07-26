/*
**  搜索栏
*/
BLUEKING.searchbar = (function(){
	return {
		/*
		**  初始化
		*/
		init : function(){
			//搜索框初始化滚动条
			$("#search-suggest .resultBox-div").mCustomScrollbar({
		        theme:"minimal",
		        callbacks:{
		        	onInit:function(){
			        	$("#search-suggest .resultBox-div").removeAttr('style');
			        	$("#search-suggest .resultBox-div").css({'max-height':'400px', 'position':'relative','overflow':'visible'});
			        }
		        }
		    });
		    // 搜索框点击不做任何操作
			$('#pageletSearchInput').on('click', function(){
				return false;
			});
			// 绑定搜索结果应用点击事件
			$('#search-suggest .resultBox').on('click', 'li', function(){
				switch($(this).attr('type')){
					case 'app':
						BLUEKING.window.create($(this).attr('appcode'), '', $(this).attr('appcode'), 1);
						break;
				}
			});
			// 绑定搜索框最右侧搜索图标点击事件
			$('#search-suggest .openAppMarket a, #pageletSearchButton').on('click', function(){
				BLUEKING.searchbar.openAppMarket($('#pageletSearchInput').val());
			});
			// 绑定在聚焦搜索框时按entry键事件
			$('#pageletSearchInput').on('keydown', function(e){
				if(e.keyCode == '13'){
					// 若未有选择的搜索结果应用，则应用市场中搜索
					if($('#search-suggest .resultBox .resultList a.selected').length == 0 && $('#search-suggest > .resultList a.selected').length == 0){
						BLUEKING.searchbar.openAppMarket($(this).val());
					}else{
						$('#search-suggest .resultList a.selected').click();
					}
				}
			});
			//聚焦搜索框时触发搜索框搜索
			$('#pageletSearchInput').focus(function(){
				if(typeof(searchFunc) == 'undefined' || searchFunc == null){
					BLUEKING.searchbar.get();
				}
			});
			// 一开始进入桌面时搜索框失去焦点
			$('#pageletSearchInput').blur();
			// 一开始显示搜索框
			$('#search-bar').show();
		},
		get : function(){
			var oldSearchVal = '';
			// 每隔1秒检测是否有输入且与是否有改变
			searchFunc = setInterval(function(){
				var searchVal = $('#pageletSearchInput').val();
				if(searchVal != ''){
					if(searchVal != oldSearchVal){
						oldSearchVal = searchVal;
						BLUEKING.searchbar.getSuggest(searchVal);
					}else{
						$('#search-suggest').show();
					}
					$('#search-bar').removeClass('above').addClass('above');
				}else{
					$('#search-suggest').hide();
					$('#search-bar').removeClass('above');
				}
			}, 1000);
			BLUEKING.searchbar.set();
			Mousetrap.bind(['up'], function(){
				if($('#search-suggest .resultBox .resultList a.selected').length == 0 && $('#search-suggest > .resultList a.selected').length == 0){
					$('#search-suggest > .resultList:last a').addClass('selected');
				}else{
					if($('#search-suggest .resultBox .resultList:first a').hasClass('selected')){
						$('#search-suggest .resultList a').removeClass('selected');
					}else{
						if($('#search-suggest > .resultList a.selected').length != 0){
							var i = $('#search-suggest > .resultList a.selected').parent('.resultList').index();
							$('#search-suggest .resultList a').removeClass('selected');
							if(i > 1){
								$('#search-suggest > .resultList:eq(' + (i - 1) + ') a').addClass('selected');
							}else{
								$('#search-suggest .resultBox .resultList:last a').addClass('selected');
							}
						}else{
							var i = $('#search-suggest .resultBox .resultList a.selected').parent('.resultList').index();
							$('#search-suggest .resultList a').removeClass('selected');
							if(i > 0){
								$('#search-suggest .resultBox .resultList:eq(' + (i - 1) + ') a').addClass('selected');
							}
						}

						$('#search-suggest .resultBox-div').mCustomScrollbar("scrollTo","+=30"); //向上滚动30px
					}
				}
				return false;
			});
			Mousetrap.bind(['down'], function(){
				if($('#search-suggest .resultBox .resultList a.selected').length == 0 && $('#search-suggest > .resultList a.selected').length == 0){
					if($('#search-suggest .resultBox .resultList').length == 0){
						$('#search-suggest > .resultList:first a').addClass('selected');
					}else{
						$('#search-suggest .resultBox .resultList:first a').addClass('selected');
					}
				}else{
					if($('#search-suggest > .resultList:last a').hasClass('selected')){
						$('#search-suggest .resultList a').removeClass('selected');
					}else{
						if($('#search-suggest .resultBox .resultList a.selected').length != 0){
							var i = $('#search-suggest .resultBox .resultList a.selected').parent('.resultList').index();
							$('#search-suggest .resultList a').removeClass('selected');
							if(i < $('#search-suggest .resultBox .resultList').length - 1){
								$('#search-suggest .resultBox .resultList:eq(' + (i + 1) + ') a').addClass('selected');
							}else{
								$('#search-suggest > .resultList:first a').addClass('selected');
							}
						}else{
							var i = $('#search-suggest > .resultList a.selected').parent('.resultList').index();
							$('#search-suggest .resultList a').removeClass('selected');
							if(i < $('#search-suggest > .resultList').length - 1){
								$('#search-suggest > .resultList:eq(' + (i + 1) + ') a').addClass('selected');
							}else{
								$('#search-suggest .resultBox .resultList:first a').addClass('selected');
							}
						}

						$('#search-suggest .resultBox-div').mCustomScrollbar("scrollTo","-=30"); //向下滚动30px
					}
				}
				return false;
			});
			Mousetrap.bind(['backspace'], function(){return true;});
		},
		set : function(){
			$('#search-bar').show();
			$('#search-suggest .resultList a').removeClass('selected');
			$('#pageletSearchInput').focus();
		},
		getSuggest : function(val){
			var suggest = '';
			//从后台获取匹配数据
			$.get(urlPrefix + 'search_apps/', {'search': val}, function(data){
				var apps = data.apps;
				for(i=0;i<apps.length;i++){
					suggest += suggestTemp({
						'name' : apps[i].name,
						'appid' : apps[i].appid,
						'type' : apps[i].type,
						'code': apps[i].code
					});
				}
				$('#search-suggest .resultBox').html(suggest);
				if(suggest == ''){
					$('#search-suggest .resultBox').hide();
				}else{
					$('#search-suggest .resultBox').show();
				}
				BLUEKING.searchbar.set();
				$('#search-suggest').show();
			}, 'json')
		},
		openAppMarket : function(searchkey){
			if(searchkey != ''){
				// 在应用市场中搜索
				BLUEKING.window.create_market_search(searchkey);
			}
			BLUEKING.searchbar.hide();
		},
		hide: function(){
			if(typeof(searchFunc) != 'undefined'){
				clearInterval(searchFunc);
				searchFunc = null;
			}
			$('#search-bar').removeClass('above');
			$('#search-suggest').hide();
			$('#pageletSearchInput').val('');
			$('#search-suggest .resultBox').html('');
			Mousetrap.unbind(['up', 'down']);
		}
	}
})();
