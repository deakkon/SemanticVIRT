<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$counter = 0;
$sqlURL = "select RECNO from datahistory";
$rezRecno = $baza->query_mysql($sqlURL);
while ($rowURL = mysql_fetch_array($rezRecno)){
	$currentRow = $rowURL['RECNO'];
	$sql = "update datahistory set rowNumber='".$counter."' where RECNO='".$currentRow."'";
	$baza->query_mysql($sql);
	$counter++;
}

?>