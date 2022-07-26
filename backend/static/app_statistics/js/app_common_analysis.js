$(function(){
	$('.search-btn').click(function(){
		// loading
		var loading_html = '<div style="height:400px">'+
						     '<div style="margin-top:180px;">'+
							   '<img src="' + static_url + 'app_statistics/img/loading_2_24x24.gif">'+
							   '<span style="margin-left: 5px;">' + gettext('数据正在加载，请稍等...') + '</span>'+
							 '</div>'+
						   '</div>'
		$("#chart_content").html(loading_html);
		var form = $(this).closest('.form');
		// 用户和应用
		var user_name = '';
		if(form.find('.user_name').length){
			user_name = form.find('.user_name').select2('val');
		}
		var app_name = '';
		if(form.find('.app_name').length){
			app_name = form.find('.app_name').select2('val');
		}
		// 时间
		var range_time = form.find('.range-time').val();
		var range_time_list = range_time.split(' - ');
		var stime = range_time_list[0];
		var etime = range_time_list[1];
		//展示方式
		var show_way = '';
		if(form.find('.show_way').length){
			show_way = form.find('.show_way').select2('val');
		}
		// 开发者
		var app_developer = '';
		if(form.find('.app_developer').length){
			app_developer = form.find('.app_developer').select2('val');
		}
		// 应用状态
		var app_state = '';
		if(form.find('.app_state').length){
			app_state = form.find('.app_state').select2('val');
		}
		// 所有参数
		var param = {
			'user_name': user_name,
			'app_code': app_name,
			'stime': stime,
			'etime': etime,
			'show_way': show_way,
			'app_developer': app_developer,
			'app_state': app_state
		}
		// 统计类型
		var analysis_type = form.attr('analysis_type');
		// 按照类型
		var according_type = form.attr('according_type');
		// 请求url
		var url = site_url + 'app_statistics/'+analysis_type+'/'+according_type+'/';
		$.get(url, param, function(html_data){
			$("#chart_content").html(html_data);
		}, 'html');
	});
	$('.tab-pane:first .search-btn').click();
})
