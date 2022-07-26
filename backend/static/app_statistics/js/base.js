$(function(){
	var tabItem = $('.tab-nav .tab-item');
	var tabPane = $('.tab-content .tab-pane');
	tabItem.on('click',function(){
		// debugger
		var index = $(this).index();
		if(!$(this).hasClass('active')){
			$(this).addClass('active');
			$(this).siblings().removeClass('active');
			$(tabPane[index]).addClass('active');
			$(tabPane[index]).siblings().removeClass('active');
            $(tabPane[index]).find('.search-btn').click();
		}
	});
    // 选择日期范围
    $('.range-time').daterangepicker({
        locale : {
            "format" : 'YYYY-MM-DD',
            "applyLabel": gettext("确定"),
            "cancelLabel": gettext("取消"),
            "weekLabel": gettext('周'),
            "customRangeLabel": gettext("自定义"),
            "daysOfWeek": [
                gettext("日"),
                gettext("一"),
                gettext("二"),
                gettext("三"),
                gettext("四"),
                gettext("五"),
                gettext("六")
            ],
            "monthNames": [
                gettext("一月"),
                gettext("二月"),
                gettext("三月"),
                gettext("四月"),
                gettext("五月"),
                gettext("六月"),
                gettext("七月"),
                gettext("八月"),
                gettext("九月"),
                gettext("十月"),
                gettext("十一月"),
                gettext("十二月")
            ],
            "firstDay": 1// 周开始时间
        },
        startDate: moment().format('YYYY') + "-01-01",
        endDate: moment().format('YYYY-MM-DD'),
    });
    // 选择用户
    $(".user_name").select2({data: [], placeholder: gettext('全部')});
    // 选择应用
    $(".app_name").select2({data: [], placeholder: gettext('全部')});
    // 选择展示方式(周，月，日)
    $(".show_way").select2({
        minimumResultsForSearch: Infinity,
        data:[{id: 0, text: gettext("按月")}, {id: 1, text: gettext("按周")}, {id: 2, text: gettext("按日")}],
        placeholder: gettext('全部')
    });
    $(".show_way").select2('val', 0);
    // 选择应用开发者
    $(".app_developer").select2({data: [], placeholder: gettext('全部')});
    // 选择应用状态
    $(".app_state").select2({
        data: [
            {id: '', text: gettext("全部")},
            {id: '4', text: gettext("已上线")},
            {id: '3', text: gettext("已提测")},
            {id: '1', text: gettext("开发中")},
            {id: '0', text: gettext("已下架")}
        ],
        placeholder: gettext('全部')
    });

    // 后端ajax请求用户数据
    if($(".user_name").length){
        $.get(site_url + "app_statistics/get_all_user/", {}, function(res){
            if(res.result){
                $(".user_name").select2({data: res.data, placeholder: gettext('全部')});
            }else{
                console.log(res.message);
            }
        }, 'json');
    }
    // 后端ajax请求所有应用
    if($(".app_name").length){
        $.get(site_url + "app_statistics/get_all_app/", {}, function(res){
            if(res.result){
                $(".app_name").select2({data: res.data, placeholder: gettext('全部')});
            }else{
                console.log(res.message);
            }
        }, 'json');
    }
    // 后端ajax请求用户数据
    if($(".app_developer").length){
        $.get(site_url + "app_statistics/get_all_app_developer/", {}, function(res){
            if(res.result){
                $(".app_developer").select2({data: res.data, placeholder: gettext('全部')});
            }else{
                console.log(res.message);
            }
        }, 'json');
    }
 });
