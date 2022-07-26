/*
**  壁纸
*/
BLUEKING.wallpaper = (function(){
	return {
		/*
		**	初始化
		*/
		init : function(){
			BLUEKING.wallpaper.get(function(){BLUEKING.wallpaper.set()});
		},
		/*
		**	获得壁纸
		**	通过ajax到后端获取壁纸信息，同时设置壁纸
		*/
		get : function(callback){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'get_wallpaper/',
				success : function(msg){
					var w = msg.split('<{|}>');
					BLUEKING.CONFIG.wallpaperState = parseInt(w[0]);
					switch(BLUEKING.CONFIG.wallpaperState){
						case 1:
						case 2:
							BLUEKING.CONFIG.wallpaper = w[1];
							BLUEKING.CONFIG.wallpaperType = w[2];
							BLUEKING.CONFIG.wallpaperWidth = parseInt(w[3]);
							BLUEKING.CONFIG.wallpaperHeight = parseInt(w[4]);
							break;
						case 3:
							BLUEKING.CONFIG.wallpaper = w[1];
							break;
					}
					callback && callback();
				}
			});
		},
		/*
		**	设置壁纸
		**	平铺和居中可直接用css样式background解决
		**	而填充、适应和拉伸则需要进行模拟
		*/
		set : function(isreload){
			/*
			**  判断壁纸是否需要重新载入
			**  比如当浏览器尺寸改变时，只需更新壁纸，而无需重新载入
			*/
			var isreload = typeof(isreload) == 'undefined' ? true : isreload;
			if(isreload){
				var times = 500;
				//IE下不加动画
				try{
					if($.browser.msie){
						var times = 0;
					}
				}catch(err){}
				$('#zoomWallpaperGrid').attr('id', 'zoomWallpaperGrid-ready2remove').css('zIndex', -11);
				setTimeout(function(){
					$('#zoomWallpaperGrid-ready2remove').remove();
					$('#zoomWallpaperGrid').removeClass('radi');
				}, times);
			}
			var w = $(window).width(), h = $(window).height();
			switch(BLUEKING.CONFIG.wallpaperState){
				case 1:
				case 2:
					// var date = new Date().getTime(); //防止缓存
					// var _wallpaper_user = BLUEKING.CONFIG.wallpaper + "?v=" + date;

          // 2019-11-11 remove date, for cache
          var d = new Date();
          var date = d.getFullYear() + "" + (d.getMonth() + 1) + "" + d.getDate();
          var _wallpaper_user = BLUEKING.CONFIG.wallpaper + "?v=" + date;

					switch(BLUEKING.CONFIG.wallpaperType){
						//平铺
						case 'pingpu':
							if(isreload){
								$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;top:0;left:0;height:100%;width:100%;background:#fff url(' + _wallpaper_user + ') repeat"></div>');
							}
							break;
						//居中
						case 'juzhong':
							if(isreload){
								$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;top:0;left:0;height:100%;width:100%;background:#fff url(' + _wallpaper_user + ') no-repeat 50% 50%"></div>');
							}
							break;
						//填充
						case 'tianchong':
							var t = (h - BLUEKING.CONFIG.wallpaperHeight) / 2, l = (w - BLUEKING.CONFIG.wallpaperWidth) / 2;
							if(isreload){
								$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;left:0;top:0;overflow:hidden;height:' + h + 'px;width:' + w + 'px;background:#fff"><img id="zoomWallpaper" src="' + _wallpaper_user + '" style="position:absolute;height:' + BLUEKING.CONFIG.wallpaperHeight + 'px;width:' + BLUEKING.CONFIG.wallpaperWidth + 'px;top:' + t + 'px;left:' + l + 'px"><div style="position:absolute;height:' + h + 'px;width:' + w + 'px;background:#fff;opacity:0;filter:alpha(opacity=0)"></div></div>');
							}else{
								$('#zoomWallpaperGrid, #zoomWallpaperGrid div').css({
									height : h + 'px',
									width : w + 'px'
								});
								$('#zoomWallpaper').css({
									top : t + 'px',
									left : l + 'px'
								});
							}
							break;
						//适应
						case 'shiying':
							var imgH, imgW, t, l;
							if(BLUEKING.CONFIG.wallpaperHeight / BLUEKING.CONFIG.wallpaperWidth > h / w){
								imgH = h;
								imgW = BLUEKING.CONFIG.wallpaperWidth * (h / BLUEKING.CONFIG.wallpaperHeight);
								t = 0;
								l = (w - imgW) / 2;
							}else if(BLUEKING.CONFIG.wallpaperHeight / BLUEKING.CONFIG.wallpaperWidth < h / w){
								imgW = w;
								imgH = BLUEKING.CONFIG.wallpaperHeight * (w / BLUEKING.CONFIG.wallpaperWidth);
								l = 0;
								t = (h - imgH) / 2;
							}else{
								imgH = BLUEKING.CONFIG.wallpaperHeight;
								imgW = BLUEKING.CONFIG.wallpaperWidth;
								t = l = 0;
							}
							if(isreload){
								$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;left:0;top:0;overflow:hidden;height:' + h + 'px;width:' + w + 'px;background:#fff"><img id="zoomWallpaper" src="' + _wallpaper_user + '" style="position:absolute;height:' + imgH + 'px;width:' + imgW + 'px;top:' + t + 'px;left:' + l + 'px"><div style="position:absolute;height:' + h + 'px;width:' + w + 'px;background:#fff;opacity:0;filter:alpha(opacity=0)"></div></div>');
							}else{
								$('#zoomWallpaperGrid, #zoomWallpaperGrid div').css({
									height : h + 'px',
									width : w + 'px'
								});
								$('#zoomWallpaper').css({
									height : imgH + 'px',
									width : imgW + 'px',
									top : t + 'px',
									left : l + 'px'
								});
							}
							break;
						//拉伸
						case 'lashen':
							if(isreload){
								$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;left:0;top:0;overflow:hidden;height:' + h + 'px;width:' + w + 'px;background:#fff"><img id="zoomWallpaper" src="' + _wallpaper_user + '" style="position:absolute;height:' + h + 'px;width:' + w + 'px;top:0;left:0"><div style="position:absolute;height:' + h + 'px;width:' + w + 'px;background:#fff;opacity:0;filter:alpha(opacity=0)"></div></div>');
							}else{
								$('#zoomWallpaperGrid').css({
									height : h + 'px',
									width : w + 'px'
								}).children('#zoomWallpaper, div').css({
									height : h + 'px',
									width : w + 'px'
								});
							}
							break;
					}
					break;
				case 3:
					if(isreload){
						$('body').append('<div id="zoomWallpaperGrid" class="radi" style="position:absolute;z-index:-10;top:0;left:0;height:100%;width:100%;overflow:hidden"><div></div><iframe id="iframeWallpaper" frameborder="no" border="0" scrolling="no" class="iframeWallpaper" style="position:absolute;left:0;top:0;overflow:hidden;width:100%;height:100%" src="' + _wallpaper_user + '"></iframe></div>');
					}
					break;
			}
		},
		/*
		**	更新壁纸
		**	通过ajax到后端进行更新，同时获得壁纸
		*/
		update : function(wallpaperstate, wallpapertype, wallpaper){
			$.ajax({
				type : 'POST',
				url : urlPrefix + 'set_wallpaper/',
				data : 'wpstate=' + wallpaperstate + '&wptype=' + wallpapertype + '&wp=' + wallpaper,
				success : function(){
					BLUEKING.wallpaper.get(function(){
						BLUEKING.wallpaper.set();
					});
				}
			});
		}
	}
})();
