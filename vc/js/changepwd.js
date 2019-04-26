// urlr = "http://223.71.105.240:18730/vc/";
// urlr = "http://223.71.105.241/vc/";
//urlr = "http://172.23.110.16/vc/";
//urlr = "http://localhost/vc/";
//urlr = "http://www.beijingdaxingtahoecn.top:18730/vc/";

mui(".mui-button-row").on('tap','.mui-btn-primary',function(e){
	var d2 = document.getElementById('d2').value;
	
	var contract = localStorage.contract;
	if(!d2){
		mui.alert('请填写完整数据')
	}else{
		
		var mask = mui.createMask();//callback为用户点击蒙版时自动执行的回调；
		mask.show();//显示遮罩
		mui.toast("正在提报");
		//JSON请求入数据库
		url = "changepwd.php";
 		mui.ajax(url,{
			data:{
				contract:contract,
				d2:d2
			},
			dataType:'json',//服务器返回json格式数据
			type:'get',//HTTP请求类型
			timeout:10000,//超时时间设置为10秒；
			//headers:{'Content-Type':'application/json'},	              
			success:function(data){
				//服务器返回响应，根据响应结果，分析是否登录成功；
				console.log(data);
				
				if(data.Result=="OK"){
					//mui.alert("报数成功");
					window.location.href = "submitsalesok.html";
				}else{
					mui.alert('报数失败，请联系管理员');
				}
			},
			error:function(xhr,type,errorThrown){
				//异常处理；
				console.log(type);
			}
		});
		
	}
})

mui(".mui-button-row").on('tap','.mui-btn-danger',function(e){
	mui.toast("取消操作");
	window.location.href = "main.html";
})