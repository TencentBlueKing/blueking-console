/*
**  许可证
*/
BLUEKING.license = (function(){
	return {
		init : function(){
		},
        get : function(callback){
		    // 获取许可证信息是否提示
			$.ajax({
				type : 'GET',
				url: urlPrefix + 'notice/get_license_notice/',
				success : function(res){
				    if(res.result){
						callback && callback(res.data[0].title);
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