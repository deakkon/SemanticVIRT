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

//get all possible actions


//NUM OF ACTIONS PER SESSION
while ($rowSid = mysql_fetch_array($rezSid)){

		$sqlNumOfSession = "SELECT COUNT(`Message`) as NoA FROM ulogdata where sessionID = '".$rowSid['sessionID']."'";	
		$rezNumOfSession = $baza->query_mysql($sqlNumOfSession);
		$rowNumOfSession = mysql_fetch_row($rezNumOfSession);	
		echo "Session: ".$rowSid['sessionID']."		had ".$rowNumOfSession[0]." actions <br />";		
		
}

//list of messages: left mb right mb etc...
//$sqlMsg = "select distinct Message from ulogdata;";
echo "left mouse actionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn<br />";
$sqlMsg = "SELECT RECNO, Date, Time, Msec FROM `ulogdata` WHERE `Message`='Left mouse button pressed' AND sessionID='ID01_Session01';";
$rezMsg = $baza->query_mysql($sqlMsg);
while ($rowMsg = mysql_fetch_array($rezMsg)){
	echo "Row: ".$rowMsg['RECNO'];
	$dateTemp = $rowMsg['Date'].' '.$rowMsg['Time'].".".$rowMsg['Msec'];
	ECHO "  dt: ".$dateTemp."<br />";
	$recnoTemp = $rowMsg['RECNO'] + 1;
	echo "Next row:".$recnoTemp;
	$sqlRecno = "SELECT Date, Time, Msec FROM `ulogdata` WHERE RECNO='$recnoTemp';";
		$rezRecno = $baza->query_mysql($sqlRecno);
		$rowRecno = mysql_fetch_row($rezRecno);
		$dateTempNextRow = $rowRecno[0].' '.$rowRecno[1].'.'.$rowRecno[2];
		echo "    ".$dateTempNextRow."<br />";

	//echo "difference in time: ".$timeDiff."<br />";
	$sqlTD = "SELECT TIMEDIFF('$dateTempNextRow','$dateTemp') AS LENGTH;";
		$rezTD = $baza->query_mysql($sqlTD);
		$rowTD = mysql_fetch_row($rezTD);	
	echo "TD: ".$rowTD[0]."<br /><br />";	
}

echo "right mouse actionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn<br />";
$sqlMsg = "SELECT RECNO, Date, Time, Msec FROM `ulogdata` WHERE `Message`='Right mouse button pressed' AND sessionID='ID01_Session01';";
$rezMsg = $baza->query_mysql($sqlMsg);
while ($rowMsg = mysql_fetch_array($rezMsg)){
	echo "Row: ".$rowMsg['RECNO'];
	$dateTemp = $rowMsg['Date'].' '.$rowMsg['Time'].".".$rowMsg['Msec'];
	ECHO "  dt: ".$dateTemp."<br />";
	$recnoTemp = $rowMsg['RECNO'] + 1;
	echo "Next row:".$recnoTemp;
	$sqlRecno = "SELECT Date, Time, Msec FROM `ulogdata` WHERE RECNO='$recnoTemp';";
		$rezRecno = $baza->query_mysql($sqlRecno);
		$rowRecno = mysql_fetch_row($rezRecno);
		$dateTempNextRow = $rowRecno[0].' '.$rowRecno[1].'.'.$rowRecno[2];
		echo "    ".$dateTempNextRow."<br />";

	//echo "difference in time: ".$timeDiff."<br />";
	$sqlTD = "SELECT TIMEDIFF('$dateTempNextRow','$dateTemp') AS LENGTH;";
		$rezTD = $baza->query_mysql($sqlTD);
		$rowTD = mysql_fetch_row($rezTD);	
	echo "TD: ".$rowTD[0]."<br /><br />";	
}

//$sqlMsg = "select distinct Message from ulogdata;";
echo "mouse wheeeeeeeeeeeeeeeelllllllllllllllllllllll<br />";
$sqlMsg = "SELECT RECNO, Date, Time, Msec FROM `ulogdata` WHERE `Message`='Mouse wheel' AND sessionID='ID01_Session01';";
$rezMsg = $baza->query_mysql($sqlMsg);
while ($rowMsg = mysql_fetch_array($rezMsg)){
	echo "Row: ".$rowMsg['RECNO'];
	$dateTemp = $rowMsg['Date'].' '.$rowMsg['Time'].".".$rowMsg['Msec'];
	ECHO "  dt: ".$dateTemp."<br />";
	$recnoTemp = $rowMsg['RECNO'] + 1;
	echo "Next row:".$recnoTemp;
	$sqlRecno = "SELECT Date, Time, Msec FROM `ulogdata` WHERE RECNO='$recnoTemp';";
		$rezRecno = $baza->query_mysql($sqlRecno);
		$rowRecno = mysql_fetch_row($rezRecno);
		$dateTempNextRow = $rowRecno[0].' '.$rowRecno[1].'.'.$rowRecno[2];
		echo "    ".$dateTempNextRow."<br />";

	//echo "difference in time: ".$timeDiff."<br />";
	$sqlTD = "SELECT TIMEDIFF('$dateTempNextRow','$dateTemp') AS LENGTH;";
		$rezTD = $baza->query_mysql($sqlTD);
		$rowTD = mysql_fetch_row($rezTD);	
	echo "TD: ".$rowTD[0]."<br /><br />";
	
}
/*
//get list of actions for user X
$sqlLinks = "SELECT distinct `Window` FROM `ulogdata`
				WHERE `Window` NOT LIKE '%PM%' 
					AND `sessionID` = 'ID01_Session01' 
					AND `Window` NOT LIKE '%Notification Area%' 
					AND `Window` NOT LIKE '%Unknown window%' and `Window` not like ' '
				LIMIT 0 , 30;";
$rezLinks = $baza->query_mysql($sqlLinks);
while($rowLinks = mysql_fetch_assoc($rezLinks)) {
	//echo $i."<br />";
	$shortLinkName = addslashes(substr($rowLinks['Window'],0,30));
	echo "Num of titles: ".mysql_num_rows($rezLinks)."<br />";
	//echo $rowLinks['Window']."<br />";
	
	$sqlListActions = "select Message,Date,Time,Msec from ulogdata where Window like '$shortLinkName%'";
	//echo $sqlListActions."<br />";	
	$rezListActions = $baza->query_mysql($sqlListActions);
	echo "Num of action for title: ".mysql_num_rows($rezListActions)."<br />";	
	while($rowListActions = mysql_fetch_array($rezListActions)){
		echo "action: ".$rowListActions['Message']."		time".$rowListActions['Date'].":".$rowListActions['Time'].":".$rowListActions['Msec']."<br />";
	}
}
*/
?>