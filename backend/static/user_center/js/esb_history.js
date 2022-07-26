var esb_history = $('#esb_history').DataTable({
    processing: true,
    paging: true, //隐藏分页
    ordering: false, //关闭排序
    info: true, //隐藏左下角分页信息
    searching: true, //关闭搜索
    pageLength : 5, //每页显示几条数据
    lengthChange: false, //不允许用户改变表格每页显示的记录数
    language: language, //汉化
    serverSide: true,
    ajax: {
        url: site_url + 'user_center/esb_apply/get_done_record/',
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
            data: "approval_result",
            render: function ( data, type, full, meta) {
                var result = '';
                if(data == 'pass'){
                    result = gettext('同意');
                }else{
                    result = gettext('拒绝');
                }
                return result
            }
        },
    ],
    drawCallback: function(settings) {
      var pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');
      pagination.toggle(this.api().page.info().pages > 1);
    }
});
var sLabel = $(".content-right").find(".dataTables_filter label");
var sInput = sLabel.find("input");
sInput.attr('placeholder', gettext('查询，模糊查询，支持：申请人、组件'));
