<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("../publicconnect/JSON.php");

$json = new Services_JSON;
$new = new gethav;

$d1 = @$_REQUEST['sdate'];
$d2 = @$_REQUEST['edate'];


$a = $new->gethavbrand($d1,$d2);

$a = $json->encode($a);
print($a);

class gethav{
    
    public function gethavbrand($d1,$d2){
        //$connect_mia = new mysqli("localhost","root","","azuz");
		$connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz");
        $connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");
		
        $query = "select count(DISTINCT contract)brand from daliyamt where txdate between '$d1' and '$d2' ";
		//echo $query;
        $result = $connect_mia->query($query);
		$row= mysqli_fetch_array($result);
		$a=array(
			//"contract"=>$row['contract'],
			"brandcount"=>$row['brand']
			);

		return $a;
    }
}


?>