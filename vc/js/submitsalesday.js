//urlr = "http://223.71.105.240:18730/vc/";
// urlr = "http://223.71.105.241/vc/";
//urlr = "http://172.23.110.16/vc/";
//urlr = "http://localhost/vc/";
//urlr = "http://www.beijingdaxingtahoecn.top:18730/vc/";

mui(".mui-button-row").on('tap','.mui-btn-primary',function(e){
	var d1 = document.getElementById('sales').value;
	var d2 = document.getElementById('count').value;
	var d3 = document.getElementById('pf').value;
	var d4 = document.getElementById('ct').value;
	var datet = document.getElementById("resultdate").innerText;
	var contract = localStorage.contract;
	console.log(datet,contract);
	if(!d1||!d2||!d3||!d4){
		mui.alert('请填写完整数据')
	}else{
		console.log(d1,d2,d3,d4);
		var mask = mui.createMask();//callback为用户点击蒙版时自动执行的回调；
		mask.show();//显示遮罩
		mui.toast("正在提报");
		//JSON请求入数据库
		url = "daliysales.php";
 		mui.ajax(url,{
			data:{
				currdate:datet,
				contract:contract,
				d1:d1,
				d2:d2,
				d3:d3,
				d4:d4
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