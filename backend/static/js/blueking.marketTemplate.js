/*
** 应用市场模板
*/

// 应用
var apptrTemp = template.compile(
    '<li>'+
        '<a href="javascript:BLUEKING.marketApp.openDetailIframe(<%=relapp_id%>);">'+
            '<img src="<%=logo_url%>" onerror="BLUEKING.toolfunc.app_logo_error_handle()">'+
			'<% if(islapp){ %>'+
			'<span class="lapp_mark"></span>'+
			'<% } %>'+
        '</a>'+
        '<a href="javascript:BLUEKING.marketApp.openDetailIframe(<%=relapp_id%>);">'+
            '<span class="app-name"><%=name%><em>(<span style="font-family: 微软雅黑;width:260px;">' + gettext('本月访问量：') + '</span><span style="color:#DFA53A"><%=app_visit_count%></span>)</em></span>'+
        '</a>'+
        '<span class="app-desc" style="width:500px"><%=introduction%></span>'+
        '<span class="app-stat" style="right:80px;top:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:250px;">'+
            '<span style="color:#555555;font-family: Courier;">' + gettext('开发负责人：') + '</span><span style="color:#888888"><%=developer%></span>'+
        '</span>'+
        '<% if(is_has){ %>'+
            '<a href="javascript:;" app_id="<%=user_app_id%>" app_code="<%=code%>" app_type="app" class="btn-run-s" style="margin-right: 22px;" title="' + gettext('打开应用') + '">' + gettext('打开应用') + '</a>'+
            '<a href="javascript:;" app_id="<%=user_app_id%>" app_code="<%=code%>" app_type="app" class="btn-remove-s" style="right:10px" title="' + gettext('卸载应用') + '">' + gettext('卸载应用') + '</a>'+
        '<% } else { %>'+
            '<a href="javascript:;" app_id="" app_code="<%=code%>" app_type="app" class="btn-run-s" style="margin-right: 22px;" title="' + gettext('打开应用') + '">' + gettext('打开应用') + '</a>'+
            '<a href="javascript:;" app_id="<%=relapp_id%>" app_code="<%=code%>" app_type="app" class="btn-add-s" style="right:10px" title="' + gettext('添加应用') + '">' + gettext('添加应用') + '</a>'+
        '<% } %>'+
    '</li>'
);

// 最近打开应用
var appopenTemp = template.compile(
    '<li>'+
        '<a style="padding-top: 8.5px;padding-bottom: 8.5px;" href="javascript:BLUEKING.marketApp.openDetailIframe(\'<%=realid%>\');">'+
            '<div class="row-fluid">'+
                '<div class="app-name-m span9">'+
                    '<img src="<%=logo_url%>" onerror="BLUEKING.toolfunc.app_logo_error_handle()" />'+
                    '<% if(islapp){ %>'+
                    '<span class="lapp_mark"></span>'+
                    '<% } %>'+
                    '<span style="margin-left: 5px;"><%=name%></span>'+
                '</div>'+
             '</div>'+
        '</a>'+
    '</li>'
);
