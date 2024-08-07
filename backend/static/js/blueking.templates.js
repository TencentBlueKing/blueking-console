//桌面应用
var appbtnTemp = template.compile(
	'<li id="<%=id%>" class="appbtn <%=isoutline%>" appid="<%=appid%>" appcode="<%=code%>" type="<%=type%>">'+
		'<div>' +
			'<img src="<%=imgsrc%>" alt="<%=title%>" onerror="BLUEKING.toolfunc.app_logo_error_handle()">' +
			'<% if(islapp){ %>'+
			'<span class="lapp_mark"></span>'+
			'<% } %>'+
		'</div>'+
		'<span style="word-wrap:break-word;"><%=name%></span>'+
	'</li>'
);
//桌面"添加应用"应用
var addbtnTemp = template.compile(
	'<li class="appbtn add">'+
		'<i class="addicon"></i>'+
		'<span>' + gettext('添加') + '</span>'+
	'</li>'
);
//任务栏
var taskTemp = template.compile(
	'<a id="<%=id%>" class="task-item task-item-current" title="<%=title%>" appid="<%=appid%>" app_code="<%=app_code%>" type="<%=type%>">'+
		'<div class="task-item-icon">'+
			'<img src="<%=imgsrc%>" alt="<%=title%>" onerror="BLUEKING.toolfunc.app_logo_error_handle()">'+
			'<% if(islapp){ %>'+
			'<span class="lapp_mark"></span>'+
			'<% } %>'+
		'</div>'+
		'<div class="task-item-txt"><%=title%></div>'+
	'</a>'
);
//应用窗口
var windowTemp = template.compile(
	'<div id="<%=id%>" class="window-container window-current" appid="<%=appid%>" realappid="<%=realappid%>" type="<%=type%>" state="show" style="<% if(isopenmax){ %>width:100%;height:100%;<% }else{ %>width:<%=width%>px;height:<%=height%>px;<% } %>z-index:<%=zIndex%>" ismax="<% if(isopenmax){ %>1<% }else{ %>0<% } %>">'+
		'<div style="height:100%">'+
			'<div class="title-bar">'+
				'<img class="icon" src="<%=imgsrc%>" alt="<%=title%>" onerror="BLUEKING.toolfunc.app_logo_error_handle()"><span class="title"><%=title%></span>'+
				'<div class="title-handle">'+
					'<a class="ha-hide" btn="hide" href="javascript:;" title="' + gettext('最小化') + '"><b class="hide-b"></b></a>'+
					'<% if(istitlebar){ %>'+
						'<a class="ha-max" btn="max" href="javascript:;" title="' + gettext('最大化') + '" <% if(isopenmax){ %>style="display:none"<% } %>><b class="max-b"></b></a>'+
						'<a class="ha-revert" btn="revert" href="javascript:;" title="' + gettext('还原') + '" <% if(!isopenmax){ %>style="display:none"<% } %>><b class="revert-b"></b><b class="revert-t"></b></a>'+
					'<% } %>'+
					'<% if(istitlebarFullscreen){ %>'+
						'<a class="ha-fullscreen" btn="fullscreen" href="javascript:;" title="' + gettext('全屏') + '">+</a>'+
					'<% } %>'+
					'<a class="ha-close" btn="close" href="javascript:;" title="' + gettext('关闭') + '">×</a>'+
				'</div>'+
			'</div>'+
			'<div class="window-frame">'+
				'<div class="window-mask window-mask-noflash"></div>'+
				'<div class="window-loading"></div>'+
				'<iframe id="<%=id%>_iframe" frameborder="0" src="<%=url%>" name="<%=id%>_iframe" org_url="<%=org_url%>"></iframe>'+
			'</div>'+
			'<div class="set-bar">'+
				'<div class="fl">'+
					'<% if(issetbar && !isthird){ %>'+
						'<a class="btn go_back ml3"><i class="icon icon63" title="' + gettext('返回上一页') + '"></i><span class="btn-con">' + gettext('返回上一页') + '</span></a>'+
						'<a class="btn refresh_current"><i class="icon icon79" title="' + gettext('刷新当前页面') + '"></i><span class="btn-con">' + gettext('刷新当前页面') + '</span></a>'+
					'<% } %>'+
					'<a class="btn refresh"><i class="icon icon158" title="' + gettext('刷新') + '"></i><span class="btn-con">' + gettext('刷新应用') + '</span></a>'+
					'<% if(issetbar && !isthird){ %>'+
						'<a class="btn copy_current_url" id="<%=id%>_copy_url"><i class="icon icon80" title="' + gettext('复制当前页面链接') + '"></i><span class="btn-con">' + gettext('复制当前页面链接') + '</span></a>'+
					'<% } %>'+
				'</div>'+
				'<div class="fr">'+
				'<% if(issetbar){ %>'+
					'<a class="btn detail"><i class="icon icon120" title="' + gettext('详情') + '"></i><span class="btn-con">' + gettext('详情') + '</span></a>'+
				'<% } %>'+
			'</div></div>'+
		'</div>'+
		'<% if(isresize){ %>'+
			'<div class="window-resize window-resize-t" resize="t"></div>'+
			'<div class="window-resize window-resize-r" resize="r"></div>'+
			'<div class="window-resize window-resize-b" resize="b"></div>'+
			'<div class="window-resize window-resize-l" resize="l"></div>'+
			'<div class="window-resize window-resize-rt" resize="rt"></div>'+
			'<div class="window-resize window-resize-rb" resize="rb"></div>'+
			'<div class="window-resize window-resize-lt" resize="lt"></div>'+
			'<div class="window-resize window-resize-lb" resize="lb"></div>'+
		'<% } %>'+
	'</div>'
);
//文件夹窗口
var folderWindowTemp = template.compile(
	'<div id="<%=id%>" class="folder-window window-container window-current" appid="<%=appid%>" realappid="<%=realappid%>" type="<%=type%>" state="show" style="width:<%=width%>px;height:<%=height%>px;z-index:<%=zIndex%>">'+
		'<div style="height:100%">'+
			'<div class="title-bar">'+
				'<img class="icon" src="<%=imgsrc%>" alt="<%=title%>"><span class="title"><%=title%></span>'+
				'<div class="title-handle">'+
					'<a class="ha-hide" btn="hide" href="javascript:;" title="' + gettext('最小化') + '"><b class="hide-b"></b></a>'+
					'<% if(istitlebar){ %>'+
						'<a class="ha-max" btn="max" href="javascript:;" title="' + gettext('最大化') + '"><b class="max-b"></b></a>'+
						'<a class="ha-revert" btn="revert" href="javascript:;" title="' + gettext('还原') + '" style="display:none"><b class="revert-b"></b><b class="revert-t"></b></a>'+
					'<% } %>'+
					'<a class="ha-close" btn="close" href="javascript:;" title="' + gettext('关闭') + '">×</a>'+
				'</div>'+
			'</div>'+
			'<div class="window-frame">'+
				'<div class="folder_body"></div>'+
			'</div>'+
			'<div class="set-bar"><div class="fr">'+
				'<a class="btn refresh"><i class="icon icon158"></i><span class="btn-con">' + gettext('刷新') + '</span></a>'+
			'</div></div>'+
		'</div>'+
		'<% if(isresize){ %>'+
			'<div class="window-resize window-resize-t" resize="t"></div>'+
			'<div class="window-resize window-resize-r" resize="r"></div>'+
			'<div class="window-resize window-resize-b" resize="b"></div>'+
			'<div class="window-resize window-resize-l" resize="l"></div>'+
			'<div class="window-resize window-resize-rt" resize="rt"></div>'+
			'<div class="window-resize window-resize-rb" resize="rb"></div>'+
			'<div class="window-resize window-resize-lt" resize="lt"></div>'+
			'<div class="window-resize window-resize-lb" resize="lb"></div>'+
		'<% } %>'+
	'</div>'
);
//文件夹预览
var folderViewTemp = template.compile(
	'<div id="<%=id%>" class="quick_view_container" appid="<%=appid%>" realappid="<%=realappid%>" style="top:<%=top%>px;left:<%=left%>px">'+
		'<div class="perfect_nine_box">'+
			'<div class="perfect_nine_t">'+
				'<div class="perfect_nine_t_m"></div>'+
			'</div>'+
			'<span class="perfect_nine_t_l"></span>'+
			'<span class="perfect_nine_t_r"></span>'+
			'<div class="perfect_nine_middle">'+
				'<span class="perfect_nine_m_l">'+
					'<div class="perfect_nine_m_l_t" style="top:0px;height:<%=mlt%>px"></div>'+
					'<div class="perfect_nine_m_l_m" style="top:<%=mlt%>px;height:20px;display:<% if(mlm){ %>block<% }else{ %>none<% } %>"></div>'+
					'<div class="perfect_nine_m_l_b" style="top:<% if(mlm){ %><%=mlt+20%><% }else{ %><%=mlt%><% } %>px;height:<%=mlb%>px"></div>'+
				'</span>'+
				'<span class="perfect_nine_m_r">'+
					'<div class="perfect_nine_m_r_t" style="top:0px;height:<%=mrt%>px"></div>'+
					'<div class="perfect_nine_m_r_m" style="top:<%=mrt%>px;height:20px;display:<% if(mrm){ %>block<% }else{ %>none<% } %>"></div>'+
					'<div class="perfect_nine_m_r_b" style="top:<% if(mrm){ %><%=mrt+20%><% }else{ %><%=mrt%><% } %>px;height:<%=mrb%>px"></div>'+
				'</span>'+
				'<div class="perfect_nine_context">'+
					'<div class="quick_view_container_control">'+
						'<a href="javascript:;" class="quick_view_container_open">' + gettext('打开') + '</a>'+
					'</div>'+
					'<div class="quick_view_container_list" id="quick_view_container_list_<%=appid%>" realid="<%=appid%>">'+
						'<div class="quick_view_container_list_in" id="quick_view_container_list_in_<%=appid%>" style="height:<%=height%>px">'+
							'<%==apps%>'+
						'</div>'+
						'<div class="scrollBar"></div>'+
						'<div class="scrollBar_bgc"></div>'+
					'</div>'+
				'</div>'+
			'</div>'+
			'<div class="perfect_nine_b">'+
				'<div class="perfect_nine_b_m"></div>'+
			'</div>'+
			'<span class="perfect_nine_b_l"></span>'+
			'<span class="perfect_nine_b_r"></span>'+
		'</div>'+
	'</div>'
);
//搜索结果列表
var suggestTemp = template.compile(
	'<li class="resultList" appid="<%=appid%>" appcode="<%=code%>" type="<%=type%>">'+
		'<a href="javascript:;"><div><%=name%></div></a>'+
	'</li>'
);
//新建&修改文件夹窗口
var editFolderDialogTemp = template.compile(
	'<div id="addfolder">'+
		'<a class="folderSelector"><img src="<%=src%>"></a>'+
		'<div class="folderNameTxt">' + gettext('请输入文件夹名称：') + '</div>'+
		'<div class="folderInput"><input type="text" class="folderName" id="folderName" value="<%=name%>"></div>'+
		'<div class="folderNameError">' + gettext('文件夹名称不能只包含空字符') + '</div>'+
		'<div class="fcDropdown">'+
		'</div>'+
	'</div>'
);
//新手帮助提示
var helpTemp = template.compile(
	'<div id="help">'+
		'<div id="step1" class="step" step="1" style="position:relative;left:50%;top:50%;margin-left:-160px;margin-top:-60px;width:370px;height:100px">'+
			'<p style="text-align:center">'+
				'<span class="h2">' + gettext('欢迎您使用蓝鲸') + '</span>'+
				'<br>' + gettext('下面我会简单介绍如何使用，以便您快速上手') + '<br>'+
				'<a href="javascript:;" class="donot_tip">' + gettext('我已了解') + '</a>'+
				'<a href="javascript:;" class="next">' + gettext('下一步') + '</a>'+
			'</p>'+
		'</div>'+
		'<div id="step2" class="step" step="2" style="top:170px;left:340px;width:250px">'+
			'<b class="jt jt_left" style="left:-40px;top:65px"></b>'+
			'<p>'+
				'<span class="h1">①</span><span class="h2">' + gettext('桌面') + '</span>'+
				'<br>' + gettext('您可以在应用市场添加自己需要的应用到桌面') + '<br>'+
				'<br>' + gettext('单击桌面的图标，就能打开应用') + '<br>'+
				'<a href="javascript:;" class="next">' + gettext('下一步') + '</a>'+
			'</p>'+
		'</div>'+
		'<div id="step3" class="step" step="3" style="top:240px;left:90px;width:250px;">'+
			'<b class="jt jt_left" style="left:-40px;top:45px"></b>'+
			'<p>'+
				'<span class="h1">②</span><span class="h2">' + gettext('应用码头') + '</span>'+
				'<br>' + gettext('展示蓝鲸智云系统应用') + '<br>'+
				'<a href="javascript:;" class="next">' + gettext('下一步') + '</a>'+
			'</p>'+
		'</div>'+

		'<div id="step4" class="step" step="4" style="top:60px;left:850px;width:260px">'+
			'<b class="jt jt_left" style="left:-40px;top:45px"></b>'+
			'<p>'+
				'<span class="h1">③</span><span class="h2">' + gettext('翻页导航') + '</span>'+
				'<br>' + gettext('您可以快速切换当前桌面') + '<br>'+
				'<a href="javascript:;" class="next">' + gettext('下一步') + '</a>'+
			'</p>'+
		'</div>'+
		'<div id="step5" class="step" step="5" style="bottom:50px;left:550px;width:250px">'+
			'<b class="jt jt_bottom" style="bottom:-40px;left:122.5px"></b>'+
			'<p>'+
				'<span class="h1">④</span><span class="h2">' + gettext('任务栏') + '</span>'+
				'<br>' + gettext('打开应用后，任务栏中就会出现对应的缩略图') + '<br>'+
				'<a href="javascript:;" class="over">' + gettext('&nbsp;完&nbsp;成&nbsp;') + '</a>'+
			'</p>'+
		'</div>'+

	'</div>'
);
// 版本信息
var versionInfoTemp = template.compile(
	'<p>'+
		gettext('名称：蓝鲸智云</br>')+
	    gettext('版本号：<%=version%></br>')+
	'</p>'
);