/*
**  应用市场 一个不属于其他模块的模块
*/
BLUEKING.marketBase = (function(){
	return {
		/*
		**	应用市场初始化
		*/
		init : function(){
			BLUEKING.marketSearchbox.init();
			BLUEKING.marketSidebar.init();
			BLUEKING.marketApp.init();
			BLUEKING.marketBase.run();
		},
		run: function(){
			var app_id = 0,
				keyword = "",
				search_str = window.location.search,
				params = search_str.substring(1).split("&");
				for(var i = 0; i < params.length; i++){
					var	param = params[i].split("=");
					// 默认打开某个app详情
					if(param[0]=="id"){
						app_id = parseInt(params[i].replace("id=", ""));
					}
					// 搜索应用
					if(param[0]=="searchkey"){
						keyword = params[i].replace("searchkey=", "");
					}
				}
			// 选择加载的页面
			if(keyword != ''){
				// 搜索结果页面
				$("#search_button").click();
			}else if(app_id != 0){
				// 后台获取全部应用，但隐藏(用于首次进入为查看详情时，返回无显示)
				BLUEKING.marketApp.get_all_app_on_background();
				// 应用详情页面
				$('#detailIframe').show();
			}else{
				// 全部应用页面
				$('.all').click();
			}
		},
		/*
		**	应用详情初始化
		*/
		init_app_detail: function(){
            $(parent.document).find('#detailIframe').show();
            /* 复制代码 */
            var clip = new ClipboardJS("#copy_appurl", {
            	text: function(trigger) {
					return BLUEKING.corefunc.get_bk_url() + '?app=' + $('#copy_appurl').attr('app_code');
				}
			});
            clip.on('success',function(){
                art.dialog({
                    title: gettext("温馨提示"),
                    width: 340,
                    icon: 'succeed',
                    lock: false,
                    fixed:true,
                    content: gettext('复制成功！您可以使用ctrl+v进行粘贴！'),
                    okVal: gettext("关闭"),
                    time: 3
				}).time(2)
            });
            /* end 复制代码 */

            //添加应用
            $('.btn-add').click(function(){
                var appid = $(this).attr('app_id');
                try{
                    window.top.BLUEKING.app.add(appid, function(){
                        window.top.BLUEKING.app.get();
                        location.reload();
                    });
                }catch(err){console.log(err)}
            });
            //打开应用
            $('.btn-run').click(function(){
                try{
                    if($(this).attr('app_id') == ''){
                        window.top.BLUEKING.api.open_app_by_other($(this).attr('app_code'));
                    }else{
                        if($(this).attr('app_type') == 'app'){
                            window.top.BLUEKING.window.create($(this).attr('app_id'));
                        }else{
                            window.top.BLUEKING.widget.create($(this).attr('app_id'));
                        }
                    }
                }catch(err){console.log(err)}
            });
		},
	}
})();
