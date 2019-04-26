<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("publicconnect/JSON.php");

$json = new Services_JSON;

$uid = @$_REQUEST['uid'];
$pwd = @$_REQUEST['pwd'];
$new = new mianpage;
if(@uid&&@pwd){
    $a = $new->submitlogin($uid,$pwd);    
}else{
    $a = array("Result"=>"break01");
}
$a = $json->encode($a);
print($a);

class mianpage{
    
    public function submitlogin($uid,$pwd){
        //$connect_mia = new mysqli("localhost","root","","azuz");
        $connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz");
		$connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");
        $query = "select count(*) from azuz.users where (user = '$uid' and pwd = '$pwd');";
        $result = $connect_mia->query($query);
        $row= mysqli_fetch_array($result);
        if($row[0]>0){
            $query_1 = "select * from azuz.users where (user = '$uid' and pwd = '$pwd');";
            $result_1 = $connect_mia->query($query_1);
            $row_1= mysqli_fetch_array($result_1);
            $re = array(
                "Result"=>"OK",
                "contract"=>$row_1['contract'],
                "brand"=>$row_1['brand']
            );
        }else{
            $re = array(
                "Result"=>"False"
            );
        }
        return $re;
    }
}


?>