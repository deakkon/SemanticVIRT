<html>
<head>
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript">

function requestCustomerInfo(uID,sID) { 
    xmlhttp=GetXmlHttpObject();
    if (xmlhttp==null) {
        alert ("Your browser does not support AJAX!");
        return;
    } 
    var url="getUserSessionDetails.php";
    url=url+"?uID="+uID+"&sID="+sID;
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 || xmlhttp.readyState=="complete") {
        	alert(http.responseText);
            document.getElementById('innerSessionUser').innerHTML=xmlhttp.responseText;
            //alert(http.responseText);
            
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
}
function GetXmlHttpObject() {
    var xmlhttp=null;
    try {
        // Firefox, Opera 8.0+, Safari
        xmlhttp=new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    return xmlhttp;
} 

</script>
</head>
<body>

<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

$sqlUID = "SELECT DISTINCT userID FROM  `ulogdata` LIMIT 0 , 30";
//$sqlSID = "SELECT DISTINCT sessionID FROM  `ulogdata` LIMIT 0 , 30";
$rezUID = $baza->query_mysql($sqlUID);
//$rezSID = $baza->query_mysql($sqlSID);
?>
<form method="GET" name="myForm">
<select id="userIDSelect"	name="userIDSelect">
	<option value='default' selected>Select user</option>
	<?php
	while ($row = mysql_fetch_array($rezUID)){
		echo '<OPTION value="'.$row['userID'].'">'.$row['userID'].'</OPTION>';
	}
	?>
</select> <select id="sessionSelect" name="sessionSelect">
	<option value='default' selected>Select user session</option>
	<?php
	for ($i=1;$i<11;$i++){
		//$j=$i+1;
		if($i!=10){
			echo '<OPTION value="0'.$row['Session'].$i.'">0'.$row['Session'].$i.'</OPTION>';
		} else {
			echo '<OPTION value="'.$row['Session'].$i.'">'.$row['Session'].$i.'</OPTION>';
		}
	}
	?>
</select> <!-- <button name="submit" 	onclick="showUser('getUserSessionDetails.php',encodeURIComponent(document.myForm.userIDSelect.value), encodeURIComponent(document.myForm.sessionSelect.value))">Show data</button>  -->
<button name="submit" onclick="requestCustomerInfo(encodeURIComponent(document.myForm.userIDSelect.value),encodeURIComponent(document.myForm.sessionSelect.value))">Show data</button>
</form>
<div id="innerSessionUser"></div>

</body>
</html>
