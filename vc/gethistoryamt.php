<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');
require_once("publicconnect/JSON.php");

$json = new Services_JSON;


$new = new gethistoryamt;
$contract = @$_REQUEST['contract'];
$a = $new->gethis($contract);

$a = $json->encode($a);
print($a);

class gethistoryamt{
    
    public function gethis($contract){
        //$connect_mia = new mysqli("localhost","root","","azuz");
        $connect_mia = new mysqli("localhost","shaclo","1984Konami","azuz");
		$connect_mia->query("set character set 'utf8'");
        $connect_mia->query("set names 'utf8'");

        $nowdate = date("Y-m-d");
		$fristdate = date("Y-m")."-01";
		$now = date("d");
        $query = "SELECT date_format(txdate,'%Y-%m-%d') txdate,amtsold,`transtrades`,`transnum`,`passflow` FROM azuz.daliyamt where (contract='$contract' and txdate between '$fristdate' and '$nowdate') order by txdate desc";
       
		$query2 =  "SELECT count('txdate')datenumber FROM azuz.daliyamt where (contract='$contract' and txdate between '$fristdate' and '$nowdate') order by txdate desc";
		$result2 = $connect_mia->query($query2);
        $row2 = mysqli_fetch_array($result2);
		$number = $now-$row2['datenumber'];
		
		$sumsales = 0;
		$result = $connect_mia->query($query) or die($query);
		$i=0;
        while($row= mysqli_fetch_array($result)){
			$sumsales += $row['amtsold'];
			$a[$i]=array(
				"txdate"=>$row['txdate'],
				"amtsold"=>$row['amtsold'],
				"transtrades"=>$row['transtrades'],
				"transnum"=>$row['transnum'],
				"passflow"=>$row['passflow']
				);
			$i++;
		}

        $re = array(
            "number"=>$number,
			"sumsales"=>$sumsales,
			"salesdetail"=>$a
        );
        return $re;
    }
}


?>