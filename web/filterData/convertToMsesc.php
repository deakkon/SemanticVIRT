<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$sqlTimeDuration = "select id, duration, timeline from actiontimes";
$rezTD = $baza->query_mysql($sqlTimeDuration);

while ($rowTD = mysql_fetch_row($rezTD)){
	
	/* convert duration to miliseconds*/
	$td = explode(":",$rowTD[1]);
	$td1 = explode(".",$td[2]);
	$miliseconds =  $td[0]*3600000+$td[1]*60000+$td[2]*1000;
	echo  $rowTD[1]."	".$td[0]."	".$td[1]."	".$td[2]."			".$miliseconds."	<br />";
	
	/* convert timeline to miliseconds */
	$tl = explode(":",$rowTD[2]);
	$tl1 = explode(".",$tl[2]);
	$timeline =  $tl[0]*3600000+$tl[1]*60000+$tl[2]*1000;
	echo  $rowTD[2]."	".$tl[0]."	".$tl[1]."	".$tl[2]."			".$timeline."<br />id".$rowTD[0]."<br /><br />";	
	
	$sqlUpdate = "update actiontimes SET durationMSEC=".$miliseconds.",timelineMSEC=".$timeline." where id=".$rowTD[0];
	$rezUpdate = $baza->query_mysql($sqlUpdate);
	
}


?>