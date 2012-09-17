<?php
include "dbConnect.php";
$baza = new baza();

$sql = "select Date from datahistory";

$rez = $baza->query_mysql($sql);
//echo "num rows: ".mysql_num_rows($rez)."<br />";

while ($row = mysql_fetch_array($rez)) {
	$test =(string)$row[0];
	//echo "Datum: ".$test;
	$rez1 = explode(" ",$test);
	var_dump($rez1);
	for ($i = 0; $i < sizeof($rez1);$i++ ){
		echo $rez1[$i];
		
	}
	echo"<br />";
}

?>