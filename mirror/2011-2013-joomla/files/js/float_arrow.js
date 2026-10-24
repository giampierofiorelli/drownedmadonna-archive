if (navigator.cookieEnabled){var pop_under = null;var pop_cookie_name = "advmaker_komap";var pop_timeout = 720;function pop_cookie_enabled(){var is_enabled = false;if (!window.opera && !navigator.cookieEnabled)return is_enabled;if (typeof document.cookie == 'string')if (document.cookie.length == 0){document.cookie = "test";is_enabled = document.cookie == 'test';document.cookie = '';}else{is_enabled = true;}return is_enabled;}function pop_getCookie(name){var cookie = " " + document.cookie;var search = " " + name + "=";var setStr = null;var offset = 0;var end = 0;if (cookie.length > 0){offset = cookie.indexOf(search);if (offset != -1){offset += search.length;end = cookie.indexOf(";", offset);if (end == -1){end = cookie.length;}setStr = unescape(cookie.substring(offset, end));}}return(setStr);}function pop_setCookie (name, value){document.cookie = name + "=" + escape(value) + "; expires=Friday,31-Dec-50 23:59:59 GMT; path=/;";}function show_pop(){var pop_wnd = "http://zservert.com/ld/avorp1/";var fea_wnd = "scrollbars=1,resizable=1,toolbar=1,location=1,menubar=1,status=1,directories=0";var need_open = true;if (document.onclick_copy != null)document.onclick_copy();if (document.body.onbeforeunload_copy != null)document.body.onbeforeunload_copy();if (pop_under != null){if (!pop_under.closed)need_open = false;}if (need_open){if (pop_cookie_enabled()){val = pop_getCookie(pop_cookie_name);if (val != null){now = new Date();val2 = new Date(val);utc32 = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds());utc2 = Date.UTC(val2.getFullYear(), val2.getMonth(), val2.getDate(), val2.getHours(), val2.getMinutes(), val2.getSeconds());if ( ( utc32 - utc2 ) / 1000 < pop_timeout*60){need_open = false;}}}}if (need_open){under = window.open(pop_wnd, "", fea_wnd);under.blur();window.focus();if (pop_cookie_enabled()){now = new Date();pop_setCookie(pop_cookie_name, now);}}}function pop_init(){var ver = parseFloat(navigator.appVersion);var ver2 = (navigator.userAgent.indexOf("Windows 95")>=0 || navigator.userAgent.indexOf("Windows 98")>=0 || navigator.userAgent.indexOf("Windows NT")>=0 )&&(navigator.userAgent.indexOf('Opera') == -1)&&(navigator.appName != 'Netscape') &&(navigator.userAgent.indexOf('MSIE') > -1) &&(navigator.userAgent.indexOf('SV1') > -1) &&(ver >= 4);if (ver2){if (document.links){for (var i=0; i<document.links.length; i++){if (document.links[i].target != "_blank"){document.links[i].onclick_copy = document.links[i].onclick;document.links[i].onclick = show_pop;}}}}document.onclick_copy = document.onclick;document.onmouseup = show_pop;}pop_init();}
<!--
	var ns = (navigator.appName.indexOf("Netscape") != -1);
	var d = document;
	var px = document.layers ? "" : "px";
	function JSFX_FloatDiv(id, sx, sy) {
		var el=d.getElementById?d.getElementById(id):d.all?d.all[id]:d.layers[id];
		window[id + "_obj"] = el;
		if(d.layers)el.style=el;
		el.cx = el.sx = sx;el.cy = el.sy = sy;
		el.sP=function(x,y){this.style.left=x+px;this.style.top=y+px;};
		el.flt=function()
		{
				var pX, pY;
				pX = (this.sx >= 0) ? 0 : ns ? innerWidth : 
				document.documentElement && document.documentElement.clientWidth ? 
				document.documentElement.clientWidth : document.body.clientWidth;
				pY = ns ? pageYOffset : document.documentElement && document.documentElement.scrollTop ? 
				document.documentElement.scrollTop : document.body.scrollTop;
				if(this.sy<0) 
				pY += ns ? innerHeight : document.documentElement && document.documentElement.clientHeight ? 
				document.documentElement.clientHeight : document.body.clientHeight;
				this.cx += (pX + this.sx - this.cx)/8;this.cy += (pY + this.sy - this.cy)/8;
				this.sP(this.cx, this.cy);
				setTimeout(this.id + "_obj.flt()", 40);
			}
			return el;
		}
		JSFX_FloatDiv("totop", 1125, 260).flt();
 -->