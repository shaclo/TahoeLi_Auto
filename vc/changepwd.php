<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("publicconnect/JSON.php");

$json = new Services_JSON;


$new = new pass;
if(@uid&&@pwd){
    
    $d2 = @$_REQUEST['d2'];
    $contract = @$_REQUEST['contract'];
    $a = $new->changepwd($contract,$d2);
}else{
    $a = array("Result"=>"break01");
}
$a = $json->encode($a);
print($a);

class pass{
    
    public function changepwd($contract,$d2){
        //$connect_mia = new mysqli("localhost","root","","azuz");
		$connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz");
        $connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");

        $query1 = "UPDATE users SET pwd = '$d2' where (contract = '$contract');";    
		//echo $query1;
        $result_OK = "OK";
        $connect_mia->query($query1);
        $re = array(
            "Result"=>$result_OK
        );
        return $re;
        // if($row[0]>0){
        //     $query_1 = "select * from azuz.users where (user = '$uid' and pwd = '$pwd');";
        //     $result_1 = $connect_mia->query($query_1);
        //     $row_1= mysqli_fetch_array($result_1);
        //     $re = array(
        //         "Result"=>"OK",
        //         "contract"=>$row_1['contract'],
        //         "brand"=>$row_1['brand']
        //     );
        // }else{
        //     $re = array(
        //         "Result"=>"False"
        //     );
        // }
        // return $re;
    }
}


?>