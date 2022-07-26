/*
**  许可证
*/
BLUEKING.license = (function(){
	return {
		init : function(){
            BLUEKING.license.get(function(msg){BLUEKING.license.set(msg)});
			$('#license_notice .notice_btn').on('click', function(){
				BLUEKING.license.hide();
			});
		},
        get : function(callback){
		    // 获取许可证信息是否提示
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_license_notice/',
				success : function(res){
				    if(!res.result){
    					callback && callback(res.message);
                    }
				}
			});
        },
        set : function(msg){
            $("#license_notice .notice_msg").text(msg);
            BLUEKING.license.show();
        },
		show : function(){
			$('#license_notice').show();
		},
		hide : function(){
			$('#license_notice').hide();
		}
	}
})();