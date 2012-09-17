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
	$sqlListActions = "select sessionID,Message, Time, Msec, RECNO, userID, Application,Window from ulogdata
						where Message not like 'Logging%' 
						and Message not like '%released' 
						and Message not like '%stopped'
						and Application ='firefox.exe'";
	$rezListActions = $baza->query_mysql($sqlListActions);

	while($rowListActions = mysql_fetch_array($rezListActions)){

		$recnoTemp = $rowListActions['RECNO'] + 1;
		$sqlRecno = "SELECT Time, Msec, sessionID, Message, RECNO, Application 
						FROM `ulogdata` WHERE RECNO='$recnoTemp';";
		$rezRecno = $baza->query_mysql($sqlRecno);
		$rowRecno = mysql_fetch_row($rezRecno);	
		/*
		if ($rowRecno[0] == '0'){
			$recnoTemp = $rowListActions['RECNO'] + 2;
			echo $rowListActions['RECNO']."				".$recnoTemp."<br />";
			$sqlRecno = "SELECT Time, Msec, sessionID, Message, RECNO FROM `ulogdata` WHERE RECNO='$recnoTemp';";
			$rezRecno = $baza->query_mysql($sqlRecno);
			$rowRecno = mysql_fetch_row($rezRecno);				
		} */
		//echo $rowListActions['RECNO']."		 ".$recnoTemp."		".$rowListActions['Message']."			<br />";		
		//echo "S1: ".$rowListActions['sessionID']."		S2: ".$rowRecno[2]."		<br />";
		
		if(strcmp ($rowListActions['sessionID'],$rowRecno[2]) == 0){		
			
				if (strlen($rowRecno[1]) == 1){
					$compareNewDate = $rowRecno[0].'.00'.$rowRecno[1];
				}elseif(strlen($rowRecno[1]) == 2){
					$compareNewDate = $rowRecno[0].'.0'.$rowRecno[1];
				}else {
					$compareNewDate = $rowRecno[0].'.'.$rowRecno[1];
				}
				
				if (strlen($rowListActions['Msec']) == 1){
					$compareOldDate = $rowListActions['Time'].'.00'.$rowListActions['Msec'];
				}elseif(strlen($rowListActions['Msec']) == 2){
					$compareOldDate = $rowListActions['Time'].'.0'.$rowListActions['Msec'];
				}else {
					$compareOldDate = $rowListActions['Time'].".".$rowListActions['Msec'];
				}

				if($compareOldDate != '.000' && $compareNewDate != '.000'){
					$sqlTD = "SELECT TIMEDIFF('".$compareNewDate."','".$compareOldDate."') AS LENGTH;";
					$rezTD = $baza->query_mysql($sqlTD);
					$rowTD = mysql_fetch_row($rezTD);
					echo $rowListActions['Message']." in row ".$rowListActions['RECNO']."  taken on $compareOldDate ended on $compareNewDate in row ".$rowRecno['4']." WITH MESSAGE ".$rowRecno['3']."  and lasted ".$rowTD[0]."<br />";
					$sqlInsertTimeAction = "insert into actiontimes 
							(userID,sessionID,actionTaken,actionTime,duration,originalRECNO,application,Window) 
							values 
							('".$rowListActions['userID']."',
							'".$rowListActions['sessionID']."',
							'".$rowListActions['Message']."',
							'".$compareOldDate."',
							'".$rowTD[0]."',
							'".$rowListActions['RECNO']."',
							'".$rowListActions['Application']."',
							'".addslashes($rowListActions['Window'])."');";
					echo $sqlInsertTimeAction."<br />"; 
					//$baza->query_mysql($sqlInsertTimeAction);
					$podaci = explode(':',$rowTD[0]);
					/*
					if($podaci[0] >= 1 || $podaci[1] >= 3 || $podaci[0] <= -1){
						echo $rowListActions['Message']." in row ".$rowListActions['RECNO']."  taken on $compareOldDate ended on $compareNewDate in row ".$rowRecno['4']." WITH MESSAGE ".$rowRecno['3']."  and lasted ".$rowTD[0]."<br />";
						echo "REMETA: ".$rowListActions['RECNO']."		".$podaci[1]."		".$rowTD[0]."<br />";
					}		*/			
				}

				
			}	
}

?>