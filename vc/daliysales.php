<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("publicconnect/JSON.php");

$json = new Services_JSON;


$new = new daliysales;
if(@uid&&@pwd){
    $d1 = @$_REQUEST['d1'];
    $d2 = @$_REQUEST['d2'];
    $d3 = @$_REQUEST['d4'];
    $d4 = @$_REQUEST['d3'];
    $contract = @$_REQUEST['contract'];
    $currdate = @$_REQUEST['currdate'];
    $a = $new->submitamt($contract,$currdate,$d1,$d2,$d3,$d4);
}else{
    $a = array("Result"=>"break01");
}
$a = $json->encode($a);
print($a);

class daliysales{
    
    public function submitamt($contract,$currdate,$d1,$d2,$d3,$d4){
        //$connect_mia = new mysqli("localhost","root","","azuz");
        $connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz");
		$connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");

        $postdate = date("Y-m-d H:i:s");
        $query = "SELECT count(*) FROM azuz.daliyamt where (contract='$contract' and txdate = '$currdate')";
        $result = $connect_mia->query($query);
        $row= mysqli_fetch_array($result);
        if($row[0]>0){
            //UPDATE
            $query1 = "UPDATE azuz.daliyamt SET amtsold = '$d1',transtrades='$d2',transnum='$d3',passflow='$d4' where (contract = '$contract' and txdate = '$currdate');";    
            //$query2 = "INSERT INTO azuz.daliyamthis VALUES('$contract','$currdate','$d1','$d2','$d3','$d4','$postdate');";    
        }else{
            //INSERT
            $query1 = "INSERT INTO azuz.daliyamt VALUES('$contract','$currdate','$d1','$d2','$d3','$d4','$postdate');";
            //$query2 = "INSERT INTO azuz.daliyamthis VALUES('$contract','$currdate','$d1','$d2','$d3','$d4','$postdate');";
        }
        $result_OK = "OK";
        $connect_mia->query($query1);
        $connect_mia->query($query2);
        $re = array(
            "Result"=>$result_OK
        );
        return $re;
    }
}


?>