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

while ($rez = mysql_fetch_array($rezSid)){
	echo $rez[0]."<br />";
	$sqlListActions = "select sessionID,Message, Time, Msec, RECNO from ulogdata
						where Message not like 'Logging%' 
						and sessionID='$rez[0]' ";
	$rezListActions = $baza->query_mysql($sqlListActions);

	while($rowListActions = mysql_fetch_array($rezListActions)){
		//echo $rowListActions['sessionID']."<br />";
		if (strpos($rowListActions['Message'], 'pressed') !== false 
				|| $rowListActions['Message'] == 'Mouse wheel'){
				
			//echo "length: ".strlen($rowListActions['Msec'])."<br />";
			$recnoTemp = $rowListActions['RECNO'] + 1;

			$sqlRecno = "SELECT Time, Msec, sessionID FROM `ulogdata` 
						 WHERE RECNO='$recnoTemp' 
						 and sessionID='".$rowListActions['sessionID']."';";
			$rezRecno = $baza->query_mysql($sqlRecno);
			$rowRecno = mysql_fetch_row($rezRecno);
			
			//echo "S1: ".$rowListActions['sessionID']."		S2: ".$rowRecno[2]."<br />";

			if($rowListActions['sessionID'] == $rowRecno[2]){
				if (strlen($rowListActions['Msec']) == 1){
					$compareNewDate = $rowListActions[0].'.00'.$rowRecno[1];
				}elseif(strlen($rowListActions['Msec']) == 2){
					$compareNewDate = $rowListActions[0].'.0'.$rowRecno[1];
				}else {
					$compareOldDate = $rowListActions['Time'].".".$rowListActions['Msec'];
				}


				if (strlen($rowRecno[1]) == 1){
					$compareNewDate = $rowRecno[0].'.00'.$rowRecno[1];
				}elseif(strlen($rowRecno[1]) == 2){
					$compareNewDate = $rowRecno[0].'.0'.$rowRecno[1];
				}else {
					$compareNewDate = $rowRecno[0].'.'.$rowRecno[1];
				}


				$sqlTD = "SELECT TIMEDIFF('".$compareNewDate."','".$compareOldDate."') AS LENGTH;";
				//$rezTD = $baza->query_mysql($sqlTD);
				$rowTD = mysql_fetch_row($rezTD);
				//echo $rowListActions['Message']." taken on $compareOldDate ended on $compareNewDate and lasted ".$rowTD[0]."<br />";
			}
		}
	}
}

?>