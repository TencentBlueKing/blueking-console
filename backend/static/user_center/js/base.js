//侧栏展开折叠
$(".slide-switch").on("click","svg",function(){
    $(".content-right").toggleClass("content-close")
    $(".king-flex-slide").toggleClass("slide-open slide-close")
    if($(".king-flex-slide").hasClass("slide-close")){
        $(".flex-subnavs").hide();
    }
});

$(".king-flex-slide.slide-open").on("click","li>a",function(){
    if($(this).parents(".king-flex-slide").hasClass("slide-close")) return ;
    var _this = $(this).parent();
    var _thisParent = _this.siblings();
    if(_this.hasClass("pureLink")){
        _this.addClass("open").siblings().removeClass("open");
    }else{
        _this.toggleClass("open").siblings().removeClass("open");
        _this.find(".flex-subnavs").slideToggle();
    }

    _thisParent.find(".flex-subnavs").slideUp();
});

$(".king-flex-slide").on("click",".flex-subnavs a",function(){
    $(".flex-subnavs a").removeClass("on");
    $(this).addClass("on");
    if($(this).parents(".king-flex-slide").hasClass("slide-close")){
        $(this).parents("li").addClass("open").siblings().removeClass("open")
    }
});

$(".king-flex-slide").on("click",".pureLink",function(){
    $(this).addClass("open").siblings().removeClass("open");
});

// datatables 国际化
var language = {
    processing: '<img src="'+static_url+'user_center/img/loading_2_16x16.gif"><span style="font-size:14px;margin-left:5px;">' + gettext('正在加载...') + '</span>',
    search: gettext('搜索：'),
    lengthMenu: gettext("每页显示 _MENU_ 记录"),
    zeroRecords: gettext("没找到相应的数据！"),
    info: gettext("分页 _PAGE_ / _PAGES_ 共_TOTAL_条"),
    infoEmpty: "",
    infoFiltered: gettext("(从 _MAX_ 条数据中搜索)"),
    paginate: {
        first: gettext('首页'),
        last: gettext('尾页'),
        previous: gettext('上一页'),
        next: gettext('下一页'),
    }
}
