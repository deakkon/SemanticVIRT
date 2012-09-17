<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();


$sqlNS = "select distinct sessionID from datahistory";
$rezNS = $baza->query_mysql($sqlNS);
while ($rowNS = mysql_fetch_array($rezNS)){
	
	$sqlNoU = "select count(URL)from datahistory NoU where sessionID='".$rowNS['sessionID']."'";	
	$rezNoU = $baza->query_mysql($sqlNoU);
	$rowNoU = mysql_fetch_row($rezNoU);
	//echo "SessionID: ".$rowNS['0']."		Number of visited links: ".$rowNoU[0]."<br />";
	$sqlInsert = "insert into nrvisitedlinks (sessionID,nrlinksVisited) values ('$rowNS[0]','$rowNoU[0]');";
	//$baza->query_mysql($sqlInsert);
	$counter++;	
}

$sqlIDNumberLinks = "select distinct userID from datahistory";
$rezIDNumberLinks = $baza->query_mysql($sqlIDNumberLinks);
$counter = 0;
while ($rowNoL = mysql_fetch_array($rezIDNumberLinks)){
	$sqlIDLinksVisited = "select count(URL)from datahistory NoU where userID='".$rowNoL['userID']."'";
	$rezIDV = $baza->query_mysql($sqlIDLinksVisited);
	$rowIDV = mysql_fetch_row($rezIDV);
	echo "UserID: ".$rowNoL['0']."		Number of visited links: ".$rowIDV[0]."<br />";	
	
	$sqlInsert = "insert into visitedlinksperuser (userID,visitedLinksNumber) values ('$rowNoL[0]','$rowIDV[0]');";
	//$baza->query_mysql($sqlInsert);
}
?>