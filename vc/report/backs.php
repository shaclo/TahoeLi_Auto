<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("../publicconnect/JSON.php");

$json = new Services_JSON;
$new = new daliyreport;

$d1 = @$_REQUEST['sdate'];
$d2 = @$_REQUEST['edate'];

$a = $new->getdaliysales($d1,$d2);

$a = $json->encode($a);
print($a);

class daliyreport{
    
    public function getdaliysales($d1,$d2){
        //$connect_mia = new mysqli("localhost","root","","azuz");
        $connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz"); 
		$connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");
		
        $query = "SELECT b.cont2,b.brand,b.place,b.category,a.txdate,a.amtsold,a.transtrades,a.transnum,a.passflow
FROM daliyamt as a,users as b WHERE a.contract = b.contract and a.txdate between '$d1' and '$d2' order by b.place,b.category,a.txdate";
		//echo $query;
        $result = $connect_mia->query($query);
		$i=0;
        while($row= mysqli_fetch_array($result)){
			if($row['amtsold']>0){$class="have";}else{$class = "non";}
			$a[$i]=array(
				"contract"=>$row['cont2'],
				"brand"=>$row['brand'],
				"place"=>$row['place'],
				"category"=>$row['category'],
				"txdate"=>$row['txdate'],
				"amtsold"=>$row['amtsold'],
				"transtrades"=>$row['transtrades'],
				"transnum"=>$row['transnum'],
				"passflow"=>$row['passflow'],
				"classvalue"=>$class
				);
			$i++;
		}
		return $a;
    }
}


?>