mui(".lis").on('tap','.cell3',function(e){
	var url = this.getAttribute("url");
	console.log(url);
	window.location.href = url;
})
mui(".lis").on('tap','.logout',function(e){
	var url = "index.html";
	logout();
	window.location.href = url;
})
