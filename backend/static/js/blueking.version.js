/*
**  版本信息
*/
BLUEKING.version = (function(){
	return {
		init : function(){
			BLUEKING.version.get(function(data){BLUEKING.version.set(data)});
			$('#version-info .close').on('click', function(){
				BLUEKING.version.hide();
			});
		},
        get : function(callback){
		    // 获取许可证信息是否提示
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_version_info/',
				success : function(res){
				    if(res.result){
    					callback && callback(res.data);
                    }
				}
			});
        },
        set : function(data){
            $("#version-info .body").html(versionInfoTemp({
                'version': data.version,
                'valid_period': data.valid_period,
                'expired_time': data.expired_time
            }));
        },
		show : function(){
			var mask = BLUEKING.maskBox.version();
			mask.show();
			$('#version-info').show();
		},
		hide : function(){
			var mask = BLUEKING.maskBox.version();
			mask.hide();
			$('#version-info').hide();
		}
	}
})();
