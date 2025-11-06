/*
**  应用列表
*/
BLUEKING.marketApp = (function(){
	return {
		/*
		**	应用列表初始化
		*/
		init : function(){
			//toolTip
			$('[rel="tooltip"]').tooltip();
			//表单提示
			$("[datatype]").focusin(function(){
				$(this).parent().addClass('info').children('.infomsg').show().siblings('.help-inline').hide();
			}).focusout(function(){
				$(this).parent().removeClass('info').children('.infomsg').hide().siblings('.help-inline').show();
			});
			BLUEKING.marketApp.get_nearest_open_app_list();
			/*
			 * 应用添加、打开、卸载操作
			 */
			//添加应用
			$(document).on('click', '.btn-add-s', function(){
				var appid = $(this).attr('app_id');
				$(this).removeClass().addClass('btn-loading-s');
				try{
					window.parent.BLUEKING.app.add(appid, function(data){
						// data的值 0:app添加失败，1：app添加成功，2：用户已经添加了该应用
						//刷新当前页
						$("#pagination ul li.active").each(function(){
							var cur_page = parseInt($(this).text());
							if(cur_page){
								BLUEKING.marketApp.getPageList(cur_page);
							}
						});
						if(data=='1'){
							window.parent.BLUEKING.app.get();
						}else if(data=='2'){
							ZENG.msgbox.show(gettext('您早就添加了该应用，请不要重复添加！'), 5, 2000);
						}else{
							ZENG.msgbox.show(gettext('添加失败！'), 5, 2000);
						}
					});
				}catch(err){console.log(err)}
			});

			//卸载应用
			$(document).on('click', '.btn-remove-s', function(){
				try{
					window.parent.BLUEKING.app.remove_new($(this).attr('app_id'), function(data){
						if(data==0){
							ZENG.msgbox.show(gettext('删除失败！'), 5, 2000);
						}else{
							if(data==1){
								window.parent.BLUEKING.app.get();
							}else if(data==3){
								ZENG.msgbox.show(gettext("您早就删除了该应用，请不要重复操作！"), 1, 2000);
							}
							//刷新当前页
							$("#pagination ul li.active").each(function(){
								var cur_page = parseInt($(this).text());
								if(cur_page){
									BLUEKING.marketApp.getPageList(cur_page);
								}
							});
						}
					});
				}catch(err){console.log(err)}
			});

			//打开应用
			$(document).on('click', '.btn-run-s', function(){
				try{
					if($(this).attr('app_id') == ''){
						window.top.BLUEKING.api.open_app_by_other($(this).attr('app_code'));
					}else{
						window.parent.BLUEKING.window.create($(this).attr('app_id'));
					}
				}catch(err){console.log(err)}
			});
		},
		/*
		** 用户最近打开的应用列表
		*/
		get_nearest_open_app_list: function(){
			$.ajax({
				type : 'GET',
				data : {},
				url : urlPrefix + 'market_get_nearest_open_app/',
				success : function(data){
					var app_list = data.app_list;
					var html_data = '';
					if(app_list.length > 0){
						for(var i in app_list){
							html_data += appopenTemp({
				                'name': app_list[i].name,
				                'code': app_list[i].code,
				                'realid': app_list[i].realid,
				                'logo_url': app_list[i].logo_url,
								'islapp': app_list[i].islapp
							})
						}
					}else{
						html_data = '<div class="detail_tips">'+
										gettext('<p>最近一个月里</p><p>您还没有打开任何应用哦！</p>')+
									'</div>';
					}
					$("#nearest_app").html(html_data);
				}
			});
		},
		/*
		** 分页拉取应用数据
		*/
		getPageList: function(current_page, flag){
			// flag：0：左侧边栏选择，1：顶部导航选择，2：普通搜索
			ZENG.msgbox.show(gettext('正在加载中，请稍后...'), 6, 100000);
			var from = (current_page-1) * parseInt($('#pagination_setting').attr('per')),
				to = (current_page)*parseInt($('#pagination_setting').attr('per'));
			var keyword = $.trim($('#keyword').val());
			//组装请求数据
			var data_post = {};
			switch(flag){
				case 0:
					//左侧导航搜索
					data_post = {
						'from': from,
						'to': to,
						'topbar_select': $('#topbar_select').val(),	// 顶部导航选择
						'sidebar_select': $('#sidebar_select').val(),	//左侧导航选择
					}
					break;
				case 1:
					//顶部导航搜索
					data_post = {
						'from': from,
						'to': to,
						'topbar_select': $('#topbar_select').val(),	// 顶部导航选择
						'sidebar_select': $('#sidebar_select').val(),	// 左侧导航选择
						'keyword': keyword,				// 查询关键字
					}
					break;
				case 2:
					//左侧导航跳至全部应用
					data_post = {
						'from': from,
						'to': to,
						'topbar_select': $('#topbar_select').val(),	// 顶部导航选择
						'keyword': keyword,				// 查询关键字
					}
					break;
				default:
					data_post = {
						'from': from,
						'to': to,
						'topbar_select': $('#topbar_select').val(),	// 顶部导航选择
						'sidebar_select': $('#sidebar_select').val(),	// 左侧导航选择
						'keyword': keyword,				// 查询关键字
					}
			}
			// ajax强求搜索
			$.ajax({
				type : 'GET',
				url : urlPrefix + 'market_get_list/',
				data : data_post,
				success : function(data){
					var per_count = parseInt($('#pagination_setting').attr('per'));
					var total = data.total;
					var app_info_list = data.app_info_list;
					if((total % per_count) > 0){
						var total_page = parseInt(total/per_count + 1);
					}else{
						var total_page = parseInt(total/per_count);
					}
					$('#pagination_setting').attr('count', total_page);//共多少页
					var html_data = '';
					for(var i in app_info_list){
						html_data += apptrTemp({
			                'name': app_info_list[i].name,
			                'code': app_info_list[i].code,
			                'introduction': app_info_list[i].introduction,
			                'use_count': app_info_list[i].use_count,
			                'user_app_id': app_info_list[i].user_app_id,
			                'relapp_id': app_info_list[i].relapp_id,
			                'logo_url': app_info_list[i].logo_url,
			                'is_saas': app_info_list[i].is_saas,
			                'developer': app_info_list[i].developer,
			                'is_has': app_info_list[i].is_has,
			                'app_visit_count': app_info_list[i].app_visit_count,
							'islapp': app_info_list[i].islapp
						})
					}
					$('.app-list').html(html_data);
					if($("#keyword").val() == ''){
						$('#app_total').html(interpolate(gettext('共有 <strong id="app_total" class="color_red">%(total)s</strong> 个应用'), {total: total}, true));
					}else{
						$('#app_total').html(interpolate(gettext('共搜到 <strong id="app_total" class="color_red">%(total)s</strong> 个应用'), {total: total}, true));
					}
					if(total != 0){
						BLUEKING.marketApp.initPagination(current_page);
						$('#pagination').show()
					}else{
						$('#pagination').hide()
					}
					ZENG.msgbox._hide();
				}
			});
		},
		/*
		** 初始分页
		*/
		initPagination: function(current_page){
			try{
				var options = {
		            currentPage: current_page,
		            totalPages: parseInt($('#pagination_setting').attr('count')),
		            numberOfPages:7,
		            alignment: 'center',
		            onPageClicked: function(e, originalEvent, type, page){
		            	if(page != current_page){
		                	BLUEKING.marketApp.getPageList(page);
		                }
		            },
		            shouldShowPage:function(type, page, current){
		                switch(type)
		                {
		                    case "first":
		                    case "last":
		                        return false;
		                    default:
		                        return true;
		                }
		            },
		            itemTexts: function (type, page, current) {
		                    switch (type) {
			                    case "prev":
			                        return gettext("上一页");
			                    case "next":
			                        return gettext("下一页");
			                    case "page":
	                        		return page;
		                    }
		            },
		            tooltipTitles: function (type, page, current) {
	                    switch (type) {
		                    case "first":
		                        return "Tooltip for first page";
		                    case "prev":
		                        return gettext("上一页");
		                    case "next":
		                        return gettext("下一页");
		                    case "last":
		                        return "Tooltip for last page";
		                    case "page":
		                        return interpolate(gettext('第%s页'), [page]);
	                    }
	               }
		        }
		        $('#pagination').bootstrapPaginator(options);
			}catch(err){console.log(err);}
		},
		/*
		** 获取全部应用数据，但页面展示隐藏
		*/
		get_all_app_on_background: function(){
			$('.all').addClass('app-all-on');
			$('.app-list-box .title ul').show();
			//左侧导航搜索值
			$('#sidebar_select').val('0');
			//顶部导航跳至第一项
			$('.app-list-box .title li').removeClass('focus');
			$('.app-list-box .title li[_value=1]').addClass('focus');
			$('#topbar_select').val(1);
			// 清空搜索条件
			BLUEKING.marketSearchbox.clearSearchInput();
			//请求搜索数据
			BLUEKING.marketApp.getPageList(1, 0);
		},
		/*
		** 显示应用详情
		*/
		openDetailIframe: function(app_id){
			var url = urlPrefix + 'market_app_detail/'+ app_id + '/';
			ZENG.msgbox.show(gettext('正在载入中，请稍后...'), 6, 100000);
			$('#detailIframe iframe').attr('src', url).load(function(){
				$('#detailIframe').show();
				ZENG.msgbox._hide();
			});
		},
		/*
		** 关闭应用详情
		*/
		closeDetailIframe: function(callback){
			$('#detailIframe').hide();
			callback && callback();
		},
	}
})();
