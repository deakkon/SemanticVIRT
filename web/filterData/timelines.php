<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$sqlAT = "select * from actiontimes";
$rezAT = $baza->query_mysql($sqlAT);
//select `originalRECNO` from actiontimes where sessionID in (select distinct sessionID from actiontimes)
$sqlSid = "select distinct sessionID from actiontimes;";
$rezSid = $baza->query_mysql($sqlSid);
$i = 0;
while ($rowSID = mysql_fetch_array($rezSid)){

	//get the first row
	$sqlAT = "select originalRECNO,actionTime from actiontimes where sessionID = '".$rowSID[sessionID]."'";
	$rezAT = $baza->query_mysql($sqlAT);
	$rowAT = mysql_fetch_row($rezAT);
	$timeAT = $rowAT[1];
	echo $rowAT[0]."				".$rowSID[sessionID]."				".$timeAT."<br />";
	//get all actions in a session and calculate time flow
	
	$sqlActionTimeline = "select originalRECNO,actionTime,sessionID,actionTaken 
							from actiontimes 
								where sessionID='".$rowSID[sessionID]."'";						

	$rezActionTimeline = $baza->query_mysql($sqlActionTimeline);
	
	while ($rowActionTimeline = mysql_fetch_array($rezActionTimeline)){
		
		$sqlTD = "SELECT TIMEDIFF('".$rowActionTimeline[actionTime]."','".$timeAT."') AS LENGTH;";
		$rezTD = $baza->query_mysql($sqlTD);
		$rowTD = mysql_fetch_row($rezTD);
		echo $rowActionTimeline[originalRECNO]."				".$rowActionTimeline[sessionID]."					".$rowActionTimeline[actionTime]."					".$rowTD[0]."<br />";
		$sqlTimelineUpdate = "update actiontimes set timeline='".$rowTD[0]."' where originalRECNO = '".$rowActionTimeline[originalRECNO]."'";
		//$rezTimelineUpdate = $baza->query_mysql($sqlTimelineUpdate);
	}
}
?>