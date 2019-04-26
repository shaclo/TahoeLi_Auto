/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function getreport(){
	var sdate = $("#sdate").val();
	var edate = $("#edate").val();
	$("#picktable tr").not("tr:first").remove();
	$("#litlist").children().remove();
	$("#pr1").html();
	$.ajax({
			url:"backs.php",
			data:{sdate:sdate,edate:edate},
			type:"get",
			dataType:"json",
			success:function(a){
				
				
				var td = '';
				var sumamt = 0;
				var sumtr = 0;
				var sumnum = 0;
				var sumpf = 0;
				for(var i =0;i<a.length;i++){
					
					if(a[i].transtrades==0){
						var d6 = '-';
					}else{
						var d6 = parseInt(a[i].amtsold/a[i].transtrades*100)/100;
					}
					if(a[i].transnum==0){
						var d7 = '-';
					}else{
						var d7 = parseInt(a[i].amtsold/a[i].transnum*100)/100;
					}
					if(a[i].passflow==0){
						var d8 = '-';
					}else{
						var d8 = parseInt(a[i].transtrades/a[i].passflow*100)+"%";
					}
					
					
					
					td = td+ "<tr class='"+a[i].classvalue+"'><td>"+a[i].contract+"</td><td>"+a[i].brand+"</td><td>"+a[i].place+"</td><td>"+a[i].category+"</td><td>"+a[i].txdate+"</td><td>"+a[i].amtsold+"</td><td>"+a[i].transtrades+"</td><td>"+a[i].transnum+"</td><td>"
						+a[i].passflow+"</td><td>"+d6+
						"</td><td>"+d7+
						"</td><td>"+d8+"</td></tr>"
					sumamt += parseInt(a[i].amtsold);
					sumtr += parseInt(a[i].transtrades);
					sumnum += parseInt(a[i].transnum);
					sumpf += parseInt(a[i].passflow);
				}
				console.log(sumpf);
				$("#picktable").append(td);
				$("#sumamt").html(sumamt);
				$("#sumtr").html(sumtr);
				$("#sumnum").html(sumnum);
				$("#sumpf").html(sumpf);

				$("#per1").html(parseInt(sumamt/sumtr*100)/100);
				$("#per2").html(parseInt(sumtr/a.length*100)/100);
				$("#per3").html(parseInt(sumtr/sumpf*10000)/100+"%");
				$("#per4").html(parseInt(sumamt/sumnum*100)/100);
			}
		})

		$.ajax({
			url:"getlit.php",
			data:{sdate:sdate,edate:edate},
			type:"get",
			dataType:"json",
			success:function(a){
				
				$("#litlist").append("<span class='litlisthead'>"+a.length+" 家租户没有报销售"+"</span>");
				for(var i =0;i<a.length;i++){
					$("#litlist").append("<span class='litlist'>"+a[i].brand+"</span>");
				}
				
			}
		})
		$.ajax({
			url:"gethav.php",
			data:{sdate:sdate,edate:edate},
			type:"get",
			dataType:"json",
			success:function(a){
				$("#havcount").html(a.brandcount);
			}
		})
}
