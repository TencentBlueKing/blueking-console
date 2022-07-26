/* Copyright (c) 2010 Brandon Aaron (http://brandonaaron.net)
 * Dual licensed under the MIT (MIT_LICENSE.txt)
 * and GPL Version 2 (GPL_LICENSE.txt) licenses.
 *
 * Version: 1.1.1
 * Requires jQuery 1.3+
 * Docs: http://docs.jquery.com/Plugins/livequery
 */
(function(a){a.extend(a.fn,{livequery:function(e,d,c){var b=this,f;if(a.isFunction(e)){c=d,d=e,e=undefined}a.each(a.livequery.queries,function(g,h){if(b.selector==h.selector&&b.context==h.context&&e==h.type&&(!d||d.$lqguid==h.fn.$lqguid)&&(!c||c.$lqguid==h.fn2.$lqguid)){return(f=h)&&false}});f=f||new a.livequery(this.selector,this.context,e,d,c);f.stopped=false;f.run();return this},expire:function(e,d,c){var b=this;if(a.isFunction(e)){c=d,d=e,e=undefined}a.each(a.livequery.queries,function(f,g){if(b.selector==g.selector&&b.context==g.context&&(!e||e==g.type)&&(!d||d.$lqguid==g.fn.$lqguid)&&(!c||c.$lqguid==g.fn2.$lqguid)&&!this.stopped){a.livequery.stop(g.id)}});return this}});a.livequery=function(b,d,f,e,c){this.selector=b;this.context=d;this.type=f;this.fn=e;this.fn2=c;this.elements=[];this.stopped=false;this.id=a.livequery.queries.push(this)-1;e.$lqguid=e.$lqguid||a.livequery.guid++;if(c){c.$lqguid=c.$lqguid||a.livequery.guid++}return this};a.livequery.prototype={stop:function(){var b=this;if(this.type){this.elements.unbind(this.type,this.fn)}else{if(this.fn2){this.elements.each(function(c,d){b.fn2.apply(d)})}}this.elements=[];this.stopped=true},run:function(){if(this.stopped){return}var d=this;var e=this.elements,c=a(this.selector,this.context),b=c.not(e);this.elements=c;if(this.type){b.bind(this.type,this.fn);if(e.length>0){a.each(e,function(f,g){if(a.inArray(g,c)<0){a.event.remove(g,d.type,d.fn)}})}}else{b.each(function(){d.fn.apply(this)});if(this.fn2&&e.length>0){a.each(e,function(f,g){if(a.inArray(g,c)<0){d.fn2.apply(g)}})}}}};a.extend(a.livequery,{guid:0,queries:[],queue:[],running:false,timeout:null,checkQueue:function(){if(a.livequery.running&&a.livequery.queue.length){var b=a.livequery.queue.length;while(b--){a.livequery.queries[a.livequery.queue.shift()].run()}}},pause:function(){a.livequery.running=false},play:function(){a.livequery.running=true;a.livequery.run()},registerPlugin:function(){a.each(arguments,function(c,d){if(!a.fn[d]){return}var b=a.fn[d];a.fn[d]=function(){var e=b.apply(this,arguments);a.livequery.run();return e}})},run:function(b){if(b!=undefined){if(a.inArray(b,a.livequery.queue)<0){a.livequery.queue.push(b)}}else{a.each(a.livequery.queries,function(c){if(a.inArray(c,a.livequery.queue)<0){a.livequery.queue.push(c)}})}if(a.livequery.timeout){clearTimeout(a.livequery.timeout)}a.livequery.timeout=setTimeout(a.livequery.checkQueue,20)},stop:function(b){if(b!=undefined){a.livequery.queries[b].stop()}else{a.each(a.livequery.queries,function(c){a.livequery.queries[c].stop()})}}});a.livequery.registerPlugin("append","prepend","after","before","wrap","attr","removeAttr","addClass","removeClass","toggleClass","empty","remove","html");a(function(){a.livequery.play()})})(jQuery);
//jQuery Cookie v1.4.1
!function(a){"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof exports?a(require("jquery")):a(jQuery)}(function(a){function c(a){return h.raw?a:encodeURIComponent(a)}function d(a){return h.raw?a:decodeURIComponent(a)}function e(a){return c(h.json?JSON.stringify(a):String(a))}function f(a){0===a.indexOf('"')&&(a=a.slice(1,-1).replace(/\\"/g,'"').replace(/\\\\/g,"\\"));try{return a=decodeURIComponent(a.replace(b," ")),h.json?JSON.parse(a):a}catch(c){}}function g(b,c){var d=h.raw?b:f(b);return a.isFunction(c)?c(d):d}var b=/\+/g,h=a.cookie=function(b,f,i){if(arguments.length>1&&!a.isFunction(f)){if(i=a.extend({},h.defaults,i),"number"==typeof i.expires){var j=i.expires,k=i.expires=new Date;k.setTime(+k+864e5*j)}return document.cookie=[c(b),"=",e(f),i.expires?"; expires="+i.expires.toUTCString():"",i.path?"; path="+i.path:"",i.domain?"; domain="+i.domain:"",i.secure?"; secure":""].join("")}for(var l=b?void 0:{},m=document.cookie?document.cookie.split("; "):[],n=0,o=m.length;o>n;n++){var p=m[n].split("="),q=d(p.shift()),r=p.join("=");if(b&&b===q){l=g(r,f);break}b||void 0===(r=g(r))||(l[q]=r)}return l};h.defaults={},a.removeCookie=function(b,c){return void 0===a.cookie(b)?!1:(a.cookie(b,"",a.extend({},c,{expires:-1})),!a.cookie(b))}});


var BKANALYSIS = {
	// 统计分析等API url前缀
	api_urlprefix: '',
	//当前访问的应用编码
	app_code:'',
	//统计在线时长的离线时间限制 2分钟
	user_online_time: 12000,
	//定时提交统计的时间间隔
	submit_time: 10*60*1000,
	// 初始化
	init: function(){
		var bklocation = window.location.href;
		var list = bklocation.split('/');
		//根据window url 判断app_code
		if(list.length >= 5 && list[3] == "o"){
			//应用编码
			BKANALYSIS.app_code = list[4];
		}else{
			//平台和系统应用
			BKANALYSIS.app_code = 'workbench';
		}
		// 初始化 api url
		var current_host = window.location.host;
		var current_protocol = window.location.protocol;
		BKANALYSIS.api_urlprefix = current_protocol + "//" + current_host + '/console/analysis/';
	},
	//定时提交调用的函数
	app_record_data_submit: function(){
		if($.cookie("r_f") && $.cookie("r_s")){
			var old_record_first = $.parseJSON($.cookie("r_f"));
			var old_record_second = $.parseJSON($.cookie("r_s"));
			if(BKANALYSIS.is_empty(old_record_first["msg"]) || BKANALYSIS.is_empty(old_record_second["msg"])){
				try{
					BKANALYSIS.save_app_click_record();
				}catch(err){}
			}
		}
	},
	//定时提交在线时长调用的函数
	app_online_time_submit: function(){
		if($.cookie("o_f") && $.cookie("o_s")){
			var old_o_f = $.parseJSON($.cookie("o_f"));
			var old_o_s = $.parseJSON($.cookie("o_s"));
			//判断cookie值，为空则不提交
			if(BKANALYSIS.is_empty(old_o_f["msg"]) || BKANALYSIS.is_empty(old_o_s["msg"])){
				try{
					BKANALYSIS.save_app_online_record();
				}catch(err){}
			}
		}
	},
	// 日期转换为字符串格式
	date_to_string: function(date){
		var year = date.getFullYear();
		var month = date.getMonth() + 1;
		var day = date.getDate();
		return year+"-"+month+"-"+day;
	},
	//判断dict对象是否为空
	is_empty: function(obj){
		for (var key in obj){
			return true;
		}
		return false;
	},
	//统计应用点击量
	app_click_record: function(num){
		var app_code = BKANALYSIS.app_code;
		if(app_code == '') return false;
		var is_exsit_first = $.cookie("r_f");
		var is_exsit_second = $.cookie("r_s");
		// 设置cookie
		if(is_exsit_first == null || is_exsit_second == null){
			//初始化数据
			var init_f = {"lock": true, "msg":{}};
			var init_s = {"lock": false, "msg":{}};
			//设置cookie
			$.cookie("r_f", $.toJSON(init_f), {expires: 7, path: '/'});
			$.cookie("r_s", $.toJSON(init_s), {expires: 7, path: '/'});
			//重新获取cookie
			is_exsit_first = $.cookie("r_f");
			is_exsit_second = $.cookie("r_s");
		}
		//判断cookie是否存在，并累加点击次数
		if(is_exsit_first && is_exsit_second){
			//累计点击量（lock为true）
			var old_record_first = $.parseJSON($.cookie("r_f"));
			var old_record_second = $.parseJSON($.cookie("r_s"));
			if(old_record_first["lock"]){
				if(old_record_first["msg"][app_code]){
		    		old_record_first["msg"][app_code] += num;
		    	}else{
		    		old_record_first["msg"][app_code] = num;
		    	}
				//累加点击次数后，重新设置cookie
		    	$.cookie("r_f", $.toJSON(old_record_first), {expires: 7, path: '/'});
			}else if(old_record_second["lock"]){
				if(old_record_second["msg"][app_code]){
					old_record_second["msg"][app_code] += num;
			    }else{
			    	old_record_second["msg"][app_code] = num;
			    }
				//累加点击次数后，重新设置cookie
				$.cookie("r_s", $.toJSON(old_record_second), {expires: 7, path: '/'});
			}
		}
		return true;
	},
	//应用点击次数提交
	save_app_click_record: function(){
		//获取cookie
		var is_exsit_first = $.cookie("r_f");
		var is_exsit_second = $.cookie("r_s");
		//判断cookie是否存在，并提交数据
		if(is_exsit_first && is_exsit_second)
		{
			//解析cookie值
			var old_record_first = $.parseJSON($.cookie("r_f"));
		    var old_record_second = $.parseJSON($.cookie("r_s"));
			//计时器提交数据（lock为true的数据）
			if(old_record_first["lock"]){
				//lock为false
				old_record_first["lock"] = false;
				$.cookie("r_f", $.toJSON(old_record_first), {expires: 7, path: '/'});
				//锁定lock为false的cookie
				old_record_second["lock"] = true;
				$.cookie("r_s", $.toJSON(old_record_second), {expires: 7, path: '/'});
				//提交lock为true的数据
				$.ajax({
		   			type:"GET",
		   			url: BKANALYSIS.api_urlprefix + "app_liveness_save/",
		   			data:	{"app_msg": $.toJSON(old_record_first["msg"])},
		   			success:function(data){
   				        //数据提交成功，cookie清空
						if(data.result){
							old_record_first["msg"] = {};
							$.cookie("r_f", $.toJSON(old_record_first), {expires: 7, path: '/'});
						}
					},
		   			dataType: "jsonp",
		   			async: false
		   		});
			}else if(old_record_second["lock"]){
				//lock为false
				old_record_second["lock"] = false;
				$.cookie("r_s", $.toJSON(old_record_second), {expires: 7, path: '/'});
				//锁定lock为false的cookie
				old_record_first["lock"] = true;
				$.cookie("r_f", $.toJSON(old_record_first), {expires: 7, path: '/'});
				//提交数据
				$.ajax({
		   			type:"GET",
		   			url: BKANALYSIS.api_urlprefix + "app_liveness_save/",
		   			data: {"app_msg": $.toJSON(old_record_second["msg"])},
		   			success:function(data){
   						//数据提交成功，cookie清空，失败不清空
						if(data.result){
							old_record_second["msg"] = {};
							//lock设为false
							$.cookie("r_s", $.toJSON(old_record_second), {expires: 7, path: '/'});
						}
					},
		   			dataType: "jsonp",
		   			async: false
		   		});
			}
		}
	},
	//统计在线时长
	app_online_record: function(time){
		var app_code = BKANALYSIS.app_code;
		if(app_code == '') return false;
		//获取当前日期，并转换
		var date_now_string = BKANALYSIS.date_to_string(new Date());
		//获取两个cookie值
		var online_f = $.cookie("o_f");
		var online_s = $.cookie("o_s");
		// 设置cookie
		if(online_f == null || online_s == null){
			//初始化数据，cookie时长设置为一周
			var init_f = {"lock": true, "msg":{}};
			var init_s = {"lock": false, "msg":{}};
			//设置cookie
			$.cookie("o_f", $.toJSON(init_f), {expires: 7, path: '/'});
			$.cookie("o_s", $.toJSON(init_s), {expires: 7, path: '/'});
			//重新获取cookie
			online_f = $.cookie("o_f");
			online_s = $.cookie("o_s");
		}
		//判断cookie是否存在，并保存数据
		if(online_f && online_s){
			//累计在线时长（lock为true）
			var old_online_f = $.parseJSON(online_f);	//获取原有的cookie值
			var old_online_s = $.parseJSON(online_s);
			//获取lock为true 的cookie,并写入
			if(old_online_f["lock"]){
				if(old_online_f["msg"][app_code]){
					//判断当天的记录是否存在
					if(old_online_f["msg"][app_code][date_now_string]){
						old_online_f["msg"][app_code][date_now_string] += time;
					}else{
						old_online_f["msg"][app_code][date_now_string] =  time;
					}
		    	}else{
		    		old_online_f["msg"][app_code] = {};
		    		old_online_f["msg"][app_code][date_now_string] = time;
		    	}
				//重新写入cookie
		    	$.cookie("o_f", $.toJSON(old_online_f), {expires: 7, path: '/'});
			}else if(old_online_s["lock"]){
				if(old_online_s["msg"][app_code]){
					if(old_online_s["msg"][app_code][date_now_string]){
						old_online_s["msg"][app_code][date_now_string] += time;
					}else{
						old_online_s["msg"][app_code][date_now_string] = time;
					}
			    }else{
			    	old_online_s["msg"][app_code] = {};
			    	old_online_s["msg"][app_code][date_now_string] = time;
			    }
				//重新写入cookie
				$.cookie("o_s", $.toJSON(old_online_s), {expires: 7, path: '/'});
			}
		 }
		return true;
	},
	//在线时长数据保存到后台
	save_app_online_record: function(){
		//获取cookie值
		var online_f = $.cookie("o_f");
		var online_s = $.cookie("o_s");
		//发送请求
		if(online_f && online_s){
			var old_online_f = $.parseJSON(online_f);
		    var old_online_s = $.parseJSON(online_s);
			//计时器提交数据（lock为false的数据）
			if(old_online_f["lock"]){
				old_online_f["lock"] = false; 		//将lock为true的锁设为false，并提交该锁的值
				$.cookie("o_f", $.toJSON(old_online_f), {expires: 7, path: '/'});
				//重新设置lock为true的cookie
				old_online_s["lock"] = true;		//将lock为false的锁设为true，重新设置该cookie，开始存入数据
				$.cookie("o_s", $.toJSON(old_online_s), {expires: 7, path: '/'});
				//发送请求
				$.ajax({
		   			type: "GET",
		   			url: BKANALYSIS.api_urlprefix + "app_online_time_save/",
		   			data:	{"app_msg": $.toJSON(old_online_f["msg"])},
		   			success:function(data){
   				        //数据提交成功操作
						if(data.result){
							//异步操作完成后，将lock为false的cookie msg设为空
							old_online_f["msg"] = {};
							$.cookie("o_f", $.toJSON(old_online_f), {expires: 7, path: '/'});
						}
					},
		   			dataType: "jsonp",
		   			async: false
		   		});
			}else if(old_online_s["lock"]){
				//将lock为true的锁设为false，并提交该锁的值
				old_online_s["lock"] = false;
				$.cookie("o_s", $.toJSON(old_online_s), {expires: 7, path: '/'});
				//重新设置lock为true的cookie
				old_online_f["lock"] = true;
				$.cookie("o_f", $.toJSON(old_online_f), {expires: 7, path: '/'});
				//发送请求
				$.ajax({
		   			type: "GET",
		   			url: BKANALYSIS.api_urlprefix + "app_online_time_save/",
		   			data: {"app_msg": $.toJSON(old_online_s["msg"])},
		   			success:function(data){
   			            //数据提交成功操作
						if(data.result){
							old_online_s["msg"] = {};
							//不换成功失败lock状态互换
							$.cookie("o_s", $.toJSON(old_online_s), {expires: 7, path: '/'});
						}
					},
		   			dataType: "jsonp",
		   			async: false
		   		});
			}
		}
	},
	//应用的打开次数
	app_record_by_user: function(){
		if(BKANALYSIS.app_code == '') return false;
		$.ajax({
        	url: BKANALYSIS.api_urlprefix + 'app_record_by_user/'+ BKANALYSIS.app_code + '/',
        	type: 'GET',
        	dataType: 'jsonp',
        	data: {}
        });
	},
}


$(document).ready(function(){
	// 初始化
	BKANALYSIS.init();
	//注册周期事件
	window.onload = function(){
		//定时提交应用点击次数等
		if(BKANALYSIS.app_code != 'workbench'){
			// 平台不统计活跃度
			window.setInterval(BKANALYSIS.app_record_data_submit, BKANALYSIS.submit_time);
		}
		window.setInterval(BKANALYSIS.app_online_time_submit, BKANALYSIS.submit_time);
	};
	// 访问首页且不在蓝鲸桌面打开 且打开的不是蓝鲸桌面
	var current_pathname = window.location.pathname;
	if(typeof(window.top.BLUEKING) == 'undefined' && BKANALYSIS.app_code != 'workbench' && (current_pathname == '/o/' + BKANALYSIS.app_code || current_pathname == '/o/' + BKANALYSIS.app_code + '/')){
		try{
			BKANALYSIS.app_record_by_user();
		}catch(err){console.log(err)}
	}
	/*
	 * 活跃度统计（内建应用进行统计）
	 */
	// 绑定点击事件
	$("a, button, input:button, input:submit, .btn").livequery('click', function() {
		try{
			// 调用统计接口
			BKANALYSIS.app_click_record(1);
		}catch(err){}
	});
	/*
	 * 在线时长统计，平台、系统应用及内建应用都使用
	 */
	//离线时间限制为2分钟（默认，后台可配）
	try{
		var time_limit = parseInt(BKANALYSIS.user_online_time) ? parseInt(BKANALYSIS.user_online_time) : 12000;
	}catch(err){
		var time_limit = 12000;
	}
	//默认激活时间、失去焦点时间、最后活动时间均为当前时间
	var as_date_now = new Date();
	var as_s_time = as_date_now,
		as_e_time = as_date_now,
		as_l_active = as_date_now;
	//页面激活
	window.onfocus = function(){
		as_date_now = new Date();		//当前时间
		as_s_time = as_date_now;		//激活时间
		//逻辑判断，激活时间与上次失效时间间隔小于等于两分钟，认为是在线状态,统计，否则为离线状态，不统计
		var short_time = as_s_time - as_e_time;
		//保存在线时间(时间差大于0且小于2分钟，则记录cookie)
		if(short_time <= time_limit && short_time > 0){
			try{
				BKANALYSIS.app_online_record(short_time);
			}catch(err){
			}
		}
		// 失去焦点的时间、最后活动时间调为和激活时间一致
		as_e_time = as_date_now;
		as_l_active = as_date_now;
	}
	function reset_active_time(){
		as_date_now = new Date();	//当前时间
		as_e_time = as_date_now;		//刷新失去焦点的时间
		//逻辑判断，最后活动时间与现在时间比较，大于2分钟，则记录最后活动时间与激活时间的差值,否则记录失去焦点时间和激活时间差值
		if(as_date_now - as_l_active > time_limit){
			//保存在线时间（最后活动时间与激活时间差，大于0保存）
			if(as_l_active - as_s_time > 0){
				try{
					BKANALYSIS.app_online_record(as_l_active - as_s_time);
				}catch(err){
				}
			}
		}else{
			//保存在线时间（失去焦点时间与激活时间差，大于0保存）
			if(as_e_time - as_s_time > 0){
				try{
					BKANALYSIS.app_online_record(as_e_time - as_s_time);
				}catch(err){
				}
			}
		}
		//变量重置
		as_s_time = as_date_now;
		as_e_time = as_date_now;
		as_l_active = as_date_now;
	}
	//页面失去焦点
	window.onblur = function(){
		reset_active_time();
	}
	//页面关闭或刷新（判断方法同失去焦点）
	window.onunload = function (){
		reset_active_time();
	}
	//页面有click活动，防止长时间页面不活动
	window.onclick = function(){
		as_date_now = new Date();	//当前时间
		//最后活动时间与现在时间比较，大于2分钟，则记录最后时间与激活时间的差值，否则更新最后活动时间
		if(as_date_now - as_l_active > time_limit){
			//保存在线时间（最后活动时间与激活时间差，大于0保存）
			if(as_l_active - as_s_time > 0){
				try{
					BKANALYSIS.app_online_record(as_l_active - as_s_time);
				}catch(err){
				}
			}
			//更新激活时间和失去焦点时间为当前时间
			as_s_time = as_date_now;
			as_e_time = as_date_now;
		}
		//最后活动时间重置
		as_l_active = as_date_now;
	}
});
