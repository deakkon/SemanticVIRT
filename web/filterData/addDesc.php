<?php 
	include("phpHTMLParser.php");
	include("simple_html_dom.php");
?>

<html>
<head>
<style>
table {
	text-align: left;
	border-collapse: collapse;
}

tr:hover {
	background: blue;
	color: white
}

th,td {
	padding: 7px
}
</style>
</head>
<body>
<div>
	<?php
	
	
	
	$myFile = "testFile.txt";
	$fh = fopen($myFile, 'w') or die("can't open file");	

	$sql = "select url from testurl";
	$host="localhost";
	$user="root";
	$pass="";
	$baza="test";
	$dbc = mysql_connect($host, $user, $pass) or die (mysql_error());;
	$db = mysql_select_db($baza, $dbc) or die (mysql_error());;
	$result = mysql_query($sql) or die(mysql_error());

	while ($row = mysql_fetch_assoc($result)){
						//echo "URL: ".$row['url']."<br />";
						$content = file_get_contents("$row[url]");
						$parser = new phpHTMLParser("$content");
						$HTMLObject = $parser->parse_tags(array("a", "title"));
						$aTags = $HTMLObject->getTagsByName("a");
						foreach ($aTags as $a) {
						if ($a->href != "") {
						echo $a->href . "<br/>";
						echo $a->innerHTML . "<br/><br/>";
					}
			}			
	}	
	
	echo "<table>\n";
	/*
	$row = 0;
	$handle = fopen(" -  - Internet Usage.csv", "r");
	
	while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
		if ($row == 0) {
			// this is the first line of the csv file
			// it usually contains titles of columns
			$num = count($data);
			echo "<thead>\n<tr>";
			$row++;
			for ($c=0; $c < $num; $c++) {
				echo "<th>" . $data[$c] . "</th>";
			}
			echo "</tr>\n</thead>\n\n<tbody>";
		} else {
			// this handles the rest of the lines of the csv file
			$num = count($data);
			echo "<tr>";
			$row++;
	
			for ($c=0; $c < $num; $c++) {
				if($c != 1){
					echo "<td></td>";
				} else {
					/*
						echo "<td>" . $data[$c] . "</td>";
						$content = file_get_contents("$data[$c]");
						$parser = new phpHTMLParser("$content");
						$HTMLObject = $parser->parse_tags(array("a", "title"));
						$aTags = $HTMLObject->getTagsByName("a");
						foreach ($aTags as $a) {
						if ($a->href != "") {
						echo $a->href . "<br/>";
						echo $a->innerHTML . "<br/><br/>";
						}
						}
						*/
	/*
					$html = file_get_html("$data[$c]");
					echo "<b>Link: ".$data[$c]."</b><br />";
					foreach($html->find("a") as $element)
					echo $element->href . "<br>";
				}
			}
	
			echo "</tr>\n";
		}
	}
	fclose($handle);
	
	echo "</tbody>\n</table>";
	*/
	?>
</div>
<div id='d'></div>
</body>
</html>
