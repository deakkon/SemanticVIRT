<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$sqlIdle = "SELECT `userID`,`sessionID`,'Date',`Time`,`Msec`,`Message`,`Window`,`Application`,`RECNO` FROM `ulogdata` WHERE `Message` like '%released' or `Message` like '%stopped'";
$dataIdle = $baza->query_mysql($sqlIdle);

while ($rowIdle = mysql_fetch_row($dataIdle)){

//	echo $rowIdle['Message']."<br />";
		//echo $rowIdle[5]."			".$rowIdle[6]."<br />";

	$recnoTemp = $rowIdle['8'] + 1;
	//echo $recnoTemp."<br />";
	$sqlRecno = "SELECT Time, Msec, sessionID, Message, RECNO, Application
						FROM `ulogdata` WHERE RECNO='$recnoTemp';";
	$rezRecno = $baza->query_mysql($sqlRecno);
	$rowRecno = mysql_fetch_row($rezRecno);

	if(strcmp ($rowIdle['1'],$rowRecno[2]) == 0){
			
		if (strlen($rowRecno[1]) == 1){
			$compareNewDate = $rowRecno[0].'.00'.$rowRecno[1];
		}elseif(strlen($rowRecno[1]) == 2){
			$compareNewDate = $rowRecno[0].'.0'.$rowRecno[1];
		}else {
			$compareNewDate = $rowRecno[0].'.'.$rowRecno[1];
		}

		if (strlen($rowIdle['4']) == 1){
			$compareOldDate = $rowIdle['3'].'.00'.$rowIdle['4'];
		}elseif(strlen($rowIdle['4']) == 2){
			$compareOldDate = $rowIdle['3'].'.0'.$rowIdle['4'];
		}else {
			$compareOldDate = $rowIdle['3'].".".$rowIdle['4'];
		}
		
		//echo "dates: ".$compareNewDate."			".$compareOldDate."<br />";

		if($compareOldDate != '.000' && $compareNewDate != '.000'){
			$sqlTD = "SELECT TIMEDIFF('".$compareNewDate."','".$compareOldDate."') AS LENGTH;";
			$rezTD = $baza->query_mysql($sqlTD);
			$rowTD = mysql_fetch_row($rezTD);

			$td = explode(":",$rowTD[0]);
			$td1 = explode(".",$td[2]);
			$miliseconds =  $td[0]*3600000+$td[1]*60000+$td[2]*1000;
			//echo  $rowTD[1]."	".$td[0]."	".$td[1]."	".$td[2]."			".$miliseconds."	<br />";		
			
			//echo $rowIdle['5']." in row ".$rowIdle['8']."  taken on $compareOldDate ended on $compareNewDate in row ".$rowRecno['4']." WITH MESSAGE ".$rowRecno['3']."  and lasted ".$rowTD[0]."<br />";
			//$recnoPrevious = $rowIdle[8];
			$sqlInsertTimeAction = "insert into idleTimes
							(userID,sessionID,Message,idleTime,RECNO) 
							values 
							('".$rowIdle[0]."',
							'".$rowIdle[1]."',
							'".$rowIdle[5]."',
							'".$miliseconds."',
							'".$recnoTemp."');";
			//$sqlUpdateRECNO = "update idleTimes set RECNO ='".$rowIdle[8]."'";
			//echo $sqlInsertTimeAction."<br />";
			//$baza->query_mysql($sqlInsertTimeAction);
			//$podaci = explode(':',$rowTD[0]);
			/*
			 if($podaci[0] >= 1 || $podaci[1] >= 3 || $podaci[0] <= -1){
			 echo $rowIdle['Message']." in row ".$rowIdle['RECNO']."  taken on $compareOldDate ended on $compareNewDate in row ".$rowRecno['4']." WITH MESSAGE ".$rowRecno['3']."  and lasted ".$rowTD[0]."<br />";
			 echo "REMETA: ".$rowIdle['RECNO']."		".$podaci[1]."		".$rowTD[0]."<br />";
			 }		*/
		}


	}

}

?>