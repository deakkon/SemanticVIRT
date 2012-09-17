<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$sqlID =  "select distinct sessionID from nrvisitedlinks";
$rezID = $baza->query_mysql($sqlID);
while ($rowMsg = mysql_fetch_array($rezID)){
	//echo $rowMsg[0]."<br />";
	$id = explode("_",$rowMsg[0]);
	//echo $id[0]."<br />";
	$sqlUpdate = "UPDATE nrvisitedlinks SET userID='".$id[0]."' WHERE sessionID LIKE '".$id[0]."%'";
	$baza->query_mysql($sqlUpdate);
}


?>