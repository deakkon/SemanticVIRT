<?php
require_once 'simplehtmldom/simple_html_dom.php';
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();
set_time_limit(0);
//phpinfo();

/* URL DOMAIN/YEAR/SECTION/MONTH/DAY/TITLE OF URL STRUCTURE
	
NEWS NODE
	TITLE DIV class='cnn_contentarea' h1
	LINKS DIV class='cnn_strycrcntr'
	CONTENT div class='cnn_strycntntlft'
	SECTION HEAD UL ID='listing-container' CLASS='nsData'


CNN DEFINED TOPICS IN NEWSPULSE
	<ul id="nsTopicList"> <span>NAME OF SECTION</span>

ENTERTAINMENT BLOG
	RECENT POSTS <div id="recent-posts-3" class="cnnPad9Top widget widget_recent_entries">
	STORY TEXT <div class="cnnRightPost">
	RECOMMENDATION <div class="cnn_strybtmmbx1"><h4>We recommend</h4>

TECH
	CONTENT <div id="cnn_LatestNews_Display">

BLOG
	BLOG TITLE <div class="cnnBlogContentTitle">
	BLOG TEXT div class="cnnBlogContentPost">
	BLOG RECOMMEND <div class="cnn_strybtmmbx1">

CNN MONEY
	CONTENT <div class="storytext">
	HOT LIST <div id="cnnMustReads">
	RIGHT NOW <div id="cnnTopStories"> GET <a>
	TITLE h1 class="storyheadline"

SPORT
	TITLE <div id="cnnStoryHeadline"> h1
	CONTENT div id="cnnContentColumn">
	
TRAVEL
	<div id="archive-display-page"> a href and link text
	<div class="cnn_sdbxcntnt cnn_spccovcbx1 cnn_strycrcntrpad cnn_skn_hottopic"> a href and link text
 */

//ini_set("memory_limit","1600M");
/*
//$html->clear();
$html1 = new simple_html_dom();
//categories
$html1->load_file('http://www.cnn.com');
$es = $html1->find('ul[id=us-menu] li a');
foreach ($es as $item){
	echo $item->href."<br />";
}
//print_r($es);
 * 
 */
echo "****************************************<br /><br /><br /><br />";
//
$sqlURL = "select URL, RECNO, rowNumber, sessionID, Title from datahistory where content =  ' ' and URL not like '%.cnn.com/'";
//$sqlURL = "select URL, Title, Date, RECNO, rowNumber, sessionID from datahistory";
$rezURL = $baza->query_mysql($sqlURL);
/*
while ($rowURL = mysql_fetch_array($rezURL)){
		ECHO $rowURL[0];	
		foreach ($es as $item){
			$pos = strpos($rowURL[0],$item->href);
			if ($item->href != '/' && $post == TRUE)
					echo $rowURL[0]."				".$item->href."<br />";
			ELSE 
				ECHO "FALSE<BR />";
		}
		
}*/

while($rowURL = mysql_fetch_array($rezURL)){
	
	$html = new simple_html_dom();
	$text = '';
	$i = 0;	
	echo $rowURL['2']."		".$rowURL['4']."		".$rowURL['0']."<br />";
	$html ->load_file($rowURL['0']);	
	//$html = file_get_html($rowURL['0']);
	//echo $html."<br />";
	//get content
	$newsContent = $html->find('div[class=cnn_strycntntlft]');
	$entertainmentContent = $html->find('div[class=cnnRightPost]');
	$techContent = $html->find('div[id=cnn_LatestNews_Display]');
	$blogContent = $html->find('div[class=cnnBlogContentPost]');
	$moneyContent = $html->find('div[class=storytext]');
	$sportContent = $html->find('div[id=cnnContentColumn]');
	$travelContent = $html->find('div[class=cnn_strycntntlft]');
	$sportsIll = $html->find('div[class=cnnStoryContent]');
	$entry = $html->find('div[class=entry]');	
	
	//echo "Title: ";
	
	foreach($newsContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
		if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
		
	}
	
	foreach($entertainmentContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
		if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}

	foreach($techContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}

	foreach($blogContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}

	foreach($moneyContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}

	foreach($sportContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}

	foreach($travelContent as $post) {  
	    # remember comments count as nodes  
	    #$articles[] = array($post->children(3)->outertext,  
	                        #$post->children(6)->first_child()->outertext);  
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}
	}
	
	foreach ($sportsIll as $post){
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}		
	}
	
	foreach ($entry as $post){
			if ($i == 0){
			//echo $post->plaintext."<br />";
			$text = addslashes($post->plaintext);
			$i++;	
		}		
	}

	if ($i == 0){
		$text = "-";
	}

	echo $text."<br />";
	echo "*******************************************************<br />";
	$insertTextSQL = "UPDATE datahistory set content='".$text."' where rowNumber = '".($rowURL['2'])."'";
	$baza->query_mysql($insertTextSQL);	
}

?>