<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();


//get users
$sqlUid ="select distinct userID from ulogdata;";
$rezUid = $baza->query_mysql($sqlUid);

//get sessions
$sqlSid = "select distinct sessionID from ulogdata;";
$rezSid = $baza->query_mysql($sqlSid);
/*
 $sqlListActions = "select sessionID,Message, Time, Msec, RECNO, userID from ulogdata
 where Message not like 'Logging%'
 and Message not like '%released'
 and Message not like '%stopped'";
 */

while($rowSID = mysql_fetch_array($rezSid)){
	$lClick = 0;
	$rClick = 0;
	$lClick = 0;
	$lClick = 0;

	$sqlListActions = "SELECT sessionID, actionTaken, COUNT(actionTaken), userID FROM  `actiontimes` 
						where sessionID = '".$rowSID[sessionID]."' group by sessionID, actionTaken;";
	$rezListActions = $baza->query_mysql($sqlListActions);
	
	while ($rowListActions = mysql_fetch_array($rezListActions)){
		echo $rowListActions [0]."		".$rowListActions[1]."		".$rowListActions[2]."		".$rowListActions[3]."<br />"; 
		$sqlInsertLA = "insert into actionsession (sessionID, actionTaken, numberTimes,userID) 
						values ('".$rowListActions[0]."','".$rowListActions[1]."','".$rowListActions[2]."','".$rowListActions[3]."')";
		$baza->query_mysql($sqlInsertLA);
	}
	
	


}

?>