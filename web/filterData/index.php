<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();


$dirname = ".";
$dir = opendir($dirname);

while(false != ($file = readdir($dir)))
{
	if(($file != ".") and ($file != ".."))
	{
		echo("<a href='$file'>$file</a> <br />");
	}
}

?>