var esb_approval = $('#esb_approval').DataTable({
    processing: true,
    paging: true, //隐藏分页
    ordering: false, //关闭排序
    info: true, //隐藏左下角分页信息
    searching: false, //关闭搜索
    pageLength : 5, //每页显示几条数据
    lengthChange: false, //不允许用户改变表格每页显示的记录数
    language: language, //汉化
    serverSide: true,
    ajax: {
        url: site_url + 'user_center/esb_apply/get_not_done_record/',
    },
    columnDefs: [
        {
            targets: 0,
            data: "operator",
        },
        {
            targets: 1,
            data: "apply_time",
        },
        {
            targets: 2,
            data: "app_name",
        },
        {
            targets: 3,
            data: "sys_name",
        },
        {
            targets: 4,
            data: "api_name",
        },
        {
            targets: 5,
            data: "record_id",
            render: function ( data, type, full, meta) {
                return '<a class="mr15" href="###" onclick="approval_apply('+data+', \'pass\')">' + gettext('同意') + '</a>' +
                    '<a class="" href="###" onclick="approval_apply('+data+', \'reject\')">' + gettext('驳回') + '</a>'
            }
        },
    ],
    drawCallback: function(settings) {
      var pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');
      pagination.toggle(this.api().page.info().pages > 1);
    }
});
function approval_apply(record_id, approval_result){
	var param = {
		record_id: record_id,
		approval_result: approval_result
	};
	$.post(site_url+'user_center/esb_apply/save_approval_result/', param, function(res){
		if(res.result){
			art.dialog({width: 300,icon: 'succeed',lock: true,content: gettext('审批成功')}).time(2);
			setTimeout(function(){
				esb_approval.ajax.reload();
			}, 2200);
		}else{
			art.dialog({width: 300,icon: 'error',lock: true,content: res.message});
		}
	}, 'json')
}
