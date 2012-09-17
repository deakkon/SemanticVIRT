<?php
require_once 'simplehtmldom/simple_html_dom.php';
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();
set_time_limit(0);


$categories = array( 1 => 'video',
2 => "newspulse",
3 => "US",
4 =>"WORLD",
5 =>"POLITICS",
6 =>"JUSTICE",
7 =>"SHOWBIZ",
8 =>"TECH",
9 =>"HEALTH",
10 =>"LIVING",
11 =>"TRAVEL",
12 =>"OPINION",
13 =>"ireport",
14 =>"money",
15 =>"sportsillustrated.cnn.com/?xid=cnnnav",
16 => "CRIME",
17 => "SPECIALS",
18 => "SPORT",
19 => "blogs",
20 => "topics",
21 => "/si/",
22 => ".si.",
23 => "ads.cnn.com",
24 => "cnn.com/linkto/ticker.html",
25 => "/search/",
26 => "ASIA",
27 => "MIDDLEEAST",
28 => "EUROPE",
29 => "cnn-cnet");

$categoriesReplace = array( 1 => 'VIDEO',
2 => "RECENT NEWS",
3 => "REGIONAL US",
4 =>"WORLD",
5 =>"POLITICS",
6 =>"JUSTICE",
7 =>"SHOWBIZ",
8 =>"TECH",
9 =>"HEALTH",
10 =>"LIVING",
11 =>"TRAVEL",
12 =>"OPINION",
13 =>"USER GENERATED CONTENT",
14 =>"MONEY",
15 =>"SPORT",
16 => "CRIME",
17 => "SPECIALS",
18 => "SPORT",
19 => "BLOG",
20 => "TOPIC COVERAGE",
21 => "SPORT",
22 => "SPORT",
23 => "ADVERTISEMENT",
24 => "POLITICS",
25 => "SEARCH",
26 => "REGIONAL ASIA",
27 => "REGIONAL MIDDLEEAST",
28 => "REGIONAL EUROPE",
29 => "TECH");


print_r($categories);
print count($categories);
print $categories[3];

//UPDATE HOME PAGES
$sqlHomePage = "update datahistory set category ='HOME' 
				WHERE URL = 'http://cnn.com/' or URL = 'http://www.cnn.com/' OR URL = 'http://edition.cnn.com/'
				OR URL = 'http://www.cnn.com/?refresh=1'";
$baza->query_mysql($sqlHomePage);	

for ($i=1; $i <= count($categories); $i++){
	
	$sqlSelectURL = "update datahistory set category = '".$categoriesReplace[$i]."' where URL LIKE '%".$categories[$i]."%'";
	$baza->query_mysql($sqlSelectURL);	
}


?>