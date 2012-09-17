<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();





//modify actionsession, add 0 for action not present
/*
 
$sqlUser = "select distinct userID from actionsession";
$userData=$baza->query_mysql($sqlUser);


while ($rowUser = mysql_fetch_row($userData)){
		//echo $rowUser[0]."<br />";
		$sqlSession = "select distinct sessionID from actionsession where userID='".$rowUser[0]."'";
		$sessionData=$baza->query_mysql($sqlSession);
		while($rowSession = mysql_fetch_row($sessionData)){
			//echo $rowSession[0]."<br />";
			$sqlActions = "select distinct `actionTaken` from actionsession";
			$actionsData=$baza->query_mysql($sqlActions);
			while($rowAction = mysql_fetch_row($actionsData)){
				//echo $rowUser[0]."	".$rowSession[0]." 	".$rowAction[0]."<br />";
				$sqlActionNr = "select numberTimes from actionsession where sessionID = '".$rowSession[0]."' and actionTaken='".$rowAction[0]."'";
				//echo $sqlActionNr."<br />";				
				$actionNrData = $baza->query_mysql($sqlActionNr);
				if (mysql_num_rows($actionNrData)==0){
					echo "sid".$rowSession[0]."    actionTaken='".$rowAction[0]."'<br />";
					$sqlUpdaate = "insert into actionsession (userID, sessionID, actionTaken, numberTimes) VALUES ('".$rowUser[0]."','".$rowSession[0]."','".$rowAction[0]."','0')";
					$baza->query_mysql($sqlUpdaate);
				}
				/*
				while ($redAN = mysql_fetch_row($actionNrData)){
					if ($redAN == "null"){
						echo "sid".$rowSession[0]."<br />";
					}					
				}
			}
		}
}
*/

//modify actiontimes, add 0 Msec duration for action not present

$sqlUser = "select distinct userID from actiontimes";
//$userData=$baza->query_mysql($sqlUser);
/*
while ($rowUser = mysql_fetch_row($userData)){
		//echo $rowUser[0]."<br />";
		$sqlSession = "select distinct sessionID from  actiontimes where userID='".$rowUser[0]."'";
		$sessionData=$baza->query_mysql($sqlSession);
		while($rowSession = mysql_fetch_row($sessionData)){
			//echo $rowSession[0]."<br />";
			$sqlActions = "select distinct `actionTaken` from actiontimes";
			$actionsData=$baza->query_mysql($sqlActions);
			while($rowAction = mysql_fetch_row($actionsData)){
				//echo $rowUser[0]."	".$rowSession[0]." 	".$rowAction[0]."<br />";
				$sqlActionNr = "select durationMSEC from actiontimes where sessionID = '".$rowSession[0]."' and actionTaken='".$rowAction[0]."'";
				//echo $sqlActionNr."<br />";				
				$actionNrData = $baza->query_mysql($sqlActionNr);
				if (mysql_num_rows($actionNrData)==0){
					echo "sid".$rowSession[0]."    actionTaken='".$rowAction[0]."'<br />";
					$sqlUpdaate = "insert into actiontimes (userID, sessionID, actionTaken, durationMSEC) VALUES ('".$rowUser[0]."','".$rowSession[0]."','".$rowAction[0]."','0')";
					//$baza->query_mysql($sqlUpdaate);
				}
				/*
				while ($redAN = mysql_fetch_row($actionNrData)){
					if ($redAN == "null"){
						echo "sid".$rowSession[0]."<br />";
					}					
				}*//*
			}
		}
}
*/
//modify idleTimes, add 0 Msec duration for action not present

$sqlUser = "select distinct userID from idleTimes";
$userData=$baza->query_mysql($sqlUser);

while ($rowUser = mysql_fetch_row($userData)){
		//echo $rowUser[0]."<br />";
		$sqlSession = "select distinct sessionID from  ulogdata where userID='".$rowUser[0]."'";
		$sessionData=$baza->query_mysql($sqlSession);
		while($rowSession = mysql_fetch_row($sessionData)){
			//echo $rowSession[0]."<br />";
			//$sqlActions = "select distinct `actionTaken` from idleTimes";
			//$actionsData=$baza->query_mysql($sqlActions);
			//while($rowAction = mysql_fetch_row($actionsData)){
				//echo $rowUser[0]."	".$rowSession[0]." 	".$rowAction[0]."<br />";
				$sqlActionNr = "select * from  idleTimes where sessionID = '".$rowSession[0]."'";
				//echo $sqlActionNr."<br />";				
				$actionNrData = $baza->query_mysql($sqlActionNr);
				if (mysql_num_rows($actionNrData)==0){
					echo "sid".$rowSession[0]."    actionTaken='".$rowAction[0]."'<br />";
					$sqlUpdaate = "insert into idleTimes (userID, sessionID, idleTime) VALUES ('".$rowUser[0]."','".$rowSession[0]."','0')";
					$baza->query_mysql($sqlUpdaate);
				}
				/*
				while ($redAN = mysql_fetch_row($actionNrData)){
					if ($redAN == "null"){
						echo "sid".$rowSession[0]."<br />";
					}					
				}*/
			//}
		}
}
?>