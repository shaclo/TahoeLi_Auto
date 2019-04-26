function loginfunctoin(){
//	window.location.href="main.html";
	var uid = document.getElementById('user').value;
	var pwd = document.getElementById('password').value;
	if(!uid||!pwd){
		mui.toast('请输入用户名和密码')
	}else{
		//JSON请求入数据库
		//urlr = "http://223.71.105.240:18730/vc/";
		//  urlr = "http://223.71.105.241/vc/";
		//urlr = "http://172.23.110.16/vc/";
		//urlr = "http://localhost/vc/";
		//urlr = "http://www.beijingdaxingtahoecn.top:18730/vc/";
		url = "inputsaleinfo.php";
		mui.ajax(url,{
			data:{
				uid:uid,
				pwd:pwd
			},
			dataType:'json',//服务器返回json格式数据
			type:'get',//HTTP请求类型
			timeout:5000,//超时时间设置为10秒；
			//headers:{'Content-Type':'application/json'},	              
			success:function(data){
				//服务器返回响应，根据响应结果，分析是否登录成功；
				//mui.toast(data.Result);
				if(data.Result=="OK"){
					//document.cookie="brand="+data.brand;
					//document.cookie="contract="+data.contract;
					localStorage.brand = data.brand;
					localStorage.contract = data.contract;
					mui.toast('登录成功，欢迎'+data.brand);
					window.location.href = "main.html";
				}else{
					mui.toast('用户名或密码错')
				}
			},
			error:function(xhr,type,errorThrown){
				//异常处理；
				mui.toast('登录失败，请稍后重试或联系管理员')
			}
		});
		
	}
}

function getCookie(key) {
	var arr,reg = RegExp('(^| )'+key+'=([^;]+)(;|$)');
	if (arr = document.cookie.match(reg))    //["username=liuwei;", "", "liuwei", ";"]
		return decodeURIComponent(arr[2]);
	else
		return null;
}

function logout(){
	localStorage.removeItem('contract');
	localStorage.removeItem('brand');
	return;
}