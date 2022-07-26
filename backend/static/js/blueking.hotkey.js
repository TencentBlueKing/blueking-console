/*
**  快捷键
*/
BLUEKING.hotkey = (function(){
	return {
		init : function(){
			Mousetrap.bind(['backspace'], function(){
				return true;
			});
			//显示桌面（最小化所有窗口）
			Mousetrap.bind(['alt+d'], function(){
				BLUEKING.window.hideAll();
				return false;
			});
			//显示全局视图
			Mousetrap.bind(['ctrl+up', 'command+up'], function(){
				BLUEKING.appmanage.set();
				return false;
			});
			Mousetrap.bind(['ctrl+1', 'command+1'], function(){
				BLUEKING.dock.switchDesk(1);
				return false;
			});
			Mousetrap.bind(['ctrl+2', 'command+2'], function(){
				BLUEKING.dock.switchDesk(2);
				return false;
			});
			Mousetrap.bind(['ctrl+3', 'command+3'], function(){
				BLUEKING.dock.switchDesk(3);
				return false;
			});
			Mousetrap.bind(['ctrl+4', 'command+4'], function(){
				BLUEKING.dock.switchDesk(4);
				return false;
			});
			Mousetrap.bind(['ctrl+5', 'command+5'], function(){
				BLUEKING.dock.switchDesk(5);
				return false;
			});
			Mousetrap.bind(['ctrl+left', 'command+left'], function(){
				if(parseInt(BLUEKING.CONFIG.desk) - 1 < 1){
					BLUEKING.dock.switchDesk(5);
				}else{
					BLUEKING.dock.switchDesk(parseInt(BLUEKING.CONFIG.desk) - 1);
				}
				return false;
			});
			Mousetrap.bind(['ctrl+right', 'command+right'], function(){
				if(parseInt(BLUEKING.CONFIG.desk) + 1 > 5){
					BLUEKING.dock.switchDesk(1);
				}else{
					BLUEKING.dock.switchDesk(parseInt(BLUEKING.CONFIG.desk) + 1);
				}
				return false;
			});
			Mousetrap.bind(['alt+1'], function(){
				BLUEKING.window.switchWindow(1);
				return false;
			});
			Mousetrap.bind(['alt+2'], function(){
				BLUEKING.window.switchWindow(2);
				return false;
			});
			Mousetrap.bind(['alt+3'], function(){
				BLUEKING.window.switchWindow(3);
				return false;
			});
			Mousetrap.bind(['alt+4'], function(){
				BLUEKING.window.switchWindow(4);
				return false;
			});
			Mousetrap.bind(['alt+5'], function(){
				BLUEKING.window.switchWindow(5);
				return false;
			});
			Mousetrap.bind(['alt+6'], function(){
				BLUEKING.window.switchWindow(6);
				return false;
			});
			Mousetrap.bind(['alt+7'], function(){
				BLUEKING.window.switchWindow(7);
				return false;
			});
			Mousetrap.bind(['alt+8'], function(){
				BLUEKING.window.switchWindow(8);
				return false;
			});
			Mousetrap.bind(['alt+9'], function(){
				BLUEKING.window.switchWindow(9);
				return false;
			});
			Mousetrap.bind(['alt+up'], function(){
				BLUEKING.window.switchWindowLeft();
				return false;
			});
			Mousetrap.bind(['alt+right'], function(){
				BLUEKING.window.switchWindowRight();
				return false;
			});
			$('#hotkey-info .close').on('click', function(){
				BLUEKING.hotkey.hide();
			});
		},
		show : function(){
			var mask = BLUEKING.maskBox.hotkey();
			mask.show();
			$('#hotkey-info').show();
		},
		hide : function(){
			var mask = BLUEKING.maskBox.hotkey();
			mask.hide();
			$('#hotkey-info').hide();
		},
	}
})();
