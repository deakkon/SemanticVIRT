<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();
print_r($_GET);

$uID = $_GET["uID"];
//$sID = $_GET["sID"];
$sID ="01";
//$uID = $_GET["valueID"];
//$sID = $_GET["valueSession"];
echo "value transfered is ".$uID." and ".$sID."<br/>";
$queryString = "SELECT * from ulogdata where userID = '$uID' AND sessionID = '".$uID."_Session".$sID."'";
echo $queryString."<br />";
$row = $baza->query_mysql($queryString);
echo mysql_num_rows($row)."<br />";
while ($rez = mysql_fetch_array($row)){
	echo $rez [0]."	".
	 $rez ['sessionID']."	".
	 $rez ['Date']."	".
	 $rez ['Time']."	".
	 $rez ['Msec']."	".
	 $rez ['Application']."	".
	 $rez ['Window']."	".
	 $rez ['Message']."	".
	 $rez ['X']."	".
	 $rez ['Y']."	".
	 $rez ['Rel__dist_']."	".
	 $rez ['Total_dist_']."	".
	 $rez ['Rate'].
	 $rez ['Extra_info']."<br />";	
}

echo "END OF RESULTS<BR />";
?>