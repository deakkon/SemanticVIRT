<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

//insert 0 for nonexisting categories

$sqlSumCat = "select userID, sessionID, `category`, count(*) as count  from datahistory group by userID, sessionID, category";
$sumCatRez = $baza->query_mysql($sqlSumCat);
//insert visited categories
while($sumCatRow = mysql_fetch_array($sumCatRez)){
	echo "".$sumCatRow[userID]."','".$sumCatRow[sessionID]."','".$sumCatRow[category]."','".$sumCatRow[count]."<br />";
	
	$sqlInsertCount = "insert into categoriessum(userID,sessionID,category,count) 
						values ('".$sumCatRow[userID]."','".$sumCatRow[sessionID]."','".$sumCatRow[category]."','".$sumCatRow[count]."')"; 
	//$baza->query_mysql($sqlInsertCount);
}

$sqlUserDistinct = "select distinct userID  from datahistory";
$userRez = $baza->query_mysql($sqlUserDistinct);

$catSumRez = $baza->query_mysql($sqlSumCat);
/*
while($userRow = mysql_fetch_array($userRez)){
	$sqlSession = "select distinct sessionID from datahistory where userID='".$userRow[userID]."'";
	$sessionRez = $baza->query_mysql($sqlSession);
	while($sessionRow = mysql_fetch_array($sessionRez)){
		$sqlAllCat = "select distinct `category` from datahistory";
		$allCatRez = $baza->query_mysql($sqlAllCat);
		while($catRow = mysql_fetch_array($allCatRez)){
			$sqlExists = "select * from datahistory where userID='".$userRow[userID]."'
			and sessionID='".$sessionRow[sessionID]."' and category='".$catRow[category]."'";
			$rezExist = $baza->query_mysql($sqlExists);
			if (mysql_num_rows($rezExist) == 0){
				$sqlUpdate = "insert into categoriessum(userID,sessionID,category,count) 
						values ('".$userRow[userID]."','".$sessionRow[sessionID]."','".$catRow[category]."','0')";
				$baza->query_mysql($sqlUpdate);
					echo "!!! NOT EXISITS ".$userRow[userID]."			".$sessionRow[sessionID]."			".$catRow[category]."<br />";
			} else {
				//echo "EXISITS ".$userRow[userID]."			".$sessionRow[sessionID]."			".$catRow[category]."<br />";
			}
		}
	}
}*/

?>