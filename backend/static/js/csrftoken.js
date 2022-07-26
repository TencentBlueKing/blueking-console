// AJAX请求，获取csrftoken
HandleAjaxCsrftoken = (function(){
    return {
        getCookie: function(name){
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        csrfSafeMethod: function(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },
        handle_func_v1: function(){
            $('html').ajaxSend(function(event, xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // 引用jquery cookie使用
                    //var csrftoken = $.cookie('bkcsrftoken');
                    // Only send the token to relative URLs i.e. locally.
                    var csrftoken = HandleAjaxCsrftoken.getCookie('bk_csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });
        },
        handle_func_v2: function(){
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!HandleAjaxCsrftoken.csrfSafeMethod(settings.type) && !this.crossDomain) {
                        var csrftoken = HandleAjaxCsrftoken.getCookie('bk_csrftoken');
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
        }
    }
})();
$(function(){
    var jquery_version = $().jquery;
    var current_version = jquery_version.split('.');
    var compare_version = [1, 10, 0];
    var result = true;
    for(var i = 0; i < 3 && result; i++){
        if(parseInt(current_version[i]) < compare_version[i]){
            result = false;
        }else if(parseInt(current_version[i]) > compare_version[i]){
            break;
        }
    }
    //大于或等于1.10.0
    if(result){
        HandleAjaxCsrftoken.handle_func_v2();
    }
    else{
        HandleAjaxCsrftoken.handle_func_v1();
    }
})
