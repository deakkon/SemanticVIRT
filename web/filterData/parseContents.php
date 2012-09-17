<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

//update when timeDiff set
$sqlURL = "select URL, Title, Date, RECNO, rowNumber, sessionID from datahistory where timeDiff = ''";
//upate when timeDiff needs a reset
//$sqlURL = "select URL, Title, Date, RECNO, rowNumber, sessionID from datahistory";
$rezURL = $baza->query_mysql($sqlURL);
while ($rowURL = mysql_fetch_array($rezURL)){
	
		$currentSession = $rowURL['sessionID'];
		$nextRow = $rowURL['rowNumber']+1;
		$dateTemp = $rowURL['Date'];
		$piecesOldDate = explode(" ", $dateTemp);
	
		$sqlRecno = "select Date, sessionID from datahistory where rowNumber ='".$nextRow."'";
		$rezRecno = $baza->query_mysql($sqlRecno);
		$rowRecno = mysql_fetch_row($rezRecno);	
		$nextSessionID = $rowRecno[1];
		$piecesNewDate = explode(" ", $rowRecno[0]);
		
		//print_r($piecesNewDate);
		echo "<br />";
		
		//echo "Num of el in old date: ".count($piecesOldDate)."			Num of el in new date: ".count($piecesNewDate)."<br />";
		
		if ($nextSessionID == $currentSession){
			
			if (count($piecesOldDate) == 6){
				//echo "longer version";
				$compareOldDate=$piecesOldDate[4];
			} else {
				$compareOldDate=$piecesOldDate[3];
			}
			
			if (count($piecesNewDate) == 6){
				//echo "longer veriosn new date version";
				$compareNewDate = $piecesNewDate[4];
			} else {
				$compareNewDate = $piecesNewDate[3];
			}

			
			$sqlTD = "SELECT TIMEDIFF('".$compareNewDate."','".$compareOldDate."') AS LENGTH;";
			$rezTD = $baza->query_mysql($sqlTD);
			$rowTD = mysql_fetch_row($rezTD);
			$sqlUTD = "update datahistory set timeDiff='".$rowTD[0]."' where rowNumber='".$rowURL['rowNumber']."'";
			$rezUTD = $baza->query_mysql($sqlUTD);
			/*
			echo "Corrent row: ".$rowURL['rowNumber'];
			echo " Current date: ".$dateTemp;
			echo " Next row: ".$nextRow;
			echo " Next row date: ".$rowRecno[0]."<br />";
			*/
			echo "Times we compare: ".$compareOldDate." and ".$compareNewDate." with ";
			//echo "<a target='_blank' href='".$rowURL['URL']."'>".$rowURL['URL']."</a>	".$rowURL['Title']."		".$rowURL['Date']."<br />";
			echo "TD: ".$rowTD[0]."<br /><br />";			
		} else {
			echo "New session: ".$nextSessionID."<br /><br />";
		}

}

?>