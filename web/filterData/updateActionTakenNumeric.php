<?php

include "dbConnect.php";
$baza = new baza();

$sql = "select distinct `actionTaken` from `actiontimes`";
$rez = $baza->query_mysql($sql);
//echo "num rows: ".mysql_num_rows($rez)."<br />";
$i=0;

while ($row = mysql_fetch_array($rez)) {
		echo $row[0];
		$actionCode[$i]=$row[0];
		$sql1 = "update actiontimes set actionTakenNumeric = '".$i."' where actionTaken='".$row[0]."'";
		$baza->query_mysql($sql1);
		$i++;
}

//print_r($actionCode);



?>