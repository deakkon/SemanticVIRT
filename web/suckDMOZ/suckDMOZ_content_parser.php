<?php

#####################################
#
# Built:07/21/01 -brs-
# Last-Touched:06/24/02 -brs-
# PHPBuild: Apache/1.3.14 (RHLinux7) PHP/4.0.3pl1
# DMOZ parser
#
#####################################

require_once("suckDMOZ_config.php");
require_once("suckDMOZ_dbconnect.php");

if($argv[0]){

 function parse_content($data,$id){
  global $closeThisContainer;

 $short_tags = array(
  'Target' => '<Target r:resource=',
  'catid' => '<tag catid=',
  'link' => '<link r:resource=',
  'link1' => '<link1 r:resource='
 );

 $open_tags = array(
  'priority' => '<priority>',
  'catid' => '<catid>',
  'd:Title' => '<d:Title>',
  'mediadate' => '<mediadate>',
  'ages' => '<ages>',
  'd:Description' => '<d:Description>'
 );

 $close_tags = array(
  'priority' => '</priority>',
  'catid' => '</catid>',
  'd:Title' => '</d:Title>',
  'mediadate' => '</mediadate>',
  'ages' => '</ages>',
  'd:Description' => '</d:Description>'
 );

 //----- find content between tags
  while (list ($key, $val) = each ($open_tags)){
   if(eregi($open_tags[$key]."([^<]{1,})".$close_tags[$key], $data,$content)){ 
    if($key=="catid"){$id=$content[1];}
    store_data($closeThisContainer[0],$closeThisContainer[1],$key,$content[1],$id,"content");
   }
  }

 //----- find content in single (no close) tags
  if(!$found_complete_tag){
   while (list($key,$val) = each($short_tags)){
    if(eregi($val."\"([^\"]{1,})\"/>",$data,$content)){
     if($key=="catid"){$id=$content[1];}
     store_data($closeThisContainer[0],$closeThisContainer[1],$key,$content[1],$id,"content");
    }
   }
  }

  return $id;

 }



 function parse_container($data,$id){
  global $closeThisContainer;

 $open_containers = array(
  'Topic' => '<Topic r:id=',
  'External Page' => '<ExternalPage about='
 );

 $close_containers = array(
  'Topic' => '</Topic>',
  'External Page' => '</ExternalPage>'
 );

  if(strlen($closeThisContainer[0])>=2){
   if(ereg("<tag catid=\"([0-9]{1,})\"/>",$data,$catid)){
    $id = $catid[1];
    //store_data($closeThisContainer[0],$closeThisContainer[1],"","",$id);
   }
   if(eregi($close_containers[$closeThisContainer[0]], $data)){
    //store_data($closeThisContainer[0],$closeThisContainer[1],"","",$id);
    unset($closeThisContainer[0]);unset($closeThisContainer[1]);
   }
   else{
    $id = parse_content($data,$id);
   }
  }

  else{
   while (list ($key, $val) = each ($open_containers)){
    if(eregi($val."\"([^\"]{1,})\">", $data,$container)){
     $closeThisContainer[0]=$key;$closeThisContainer[1]=$container[1];
    }
   }
  }


  return $id;

 }



 function run_parser(){
  global $closeThisContainer,$start_time,$count_rows;

  header("Content-type: text/plain"); 

  $info = get_file_info("1",CONTENT_RDF,"",$start_time,"");
  $filesize = $info[0];
  $benchmark = $info[1];
  $adj_filesize = $info[2];

  if(ECHO_CONTENT_STATS){
   $start_time=getmicrotime();
   $count_rows=0;
   echo_status($start_time,$count_rows,"START (FILESIZE: ".$adj_filesize.")");
  }

  set_time_limit(0); // unlimited

  $createtable = suckDMOZ_content_dbconnect($fields,"create");
  if($createtable[0]=="error"){
   if($createtable[2]=="No Database Selected"){die("Database Error, Could Not Create 'DMOZ_content'");}
   else{echo $createtable[2]."\n";}
  }

  if (!($fp = fopen(CONTENT_RDF, 'r'))) {
     die("Could not open ".constant("CONTENT_RDF")." for parsing!\n");
  }

  while (!feof ($fp)){
     $data = fgets($fp, 1024);
   $id  = parse_container($data,$id);
   
   $string_size = strlen($data)-1;
   $eaten=$eaten+$string_size;
   $next_benchmark=$next_benchmark+$string_size;
   if($next_benchmark>$benchmark){
    $next_benchmark=0;
    $info2 = get_file_info("2",CONTENT_RDF,$eaten,$start_time,$count_rows);
    $echo ="REMAINING: {".$info2[0]."} (".$info2[1]."%) [".$info2[2]."]";
    $echo.="\n[APPROX TOTAL RUN TIME: ".$info2[3]."]";
    $echo.="\n[APPROX TOTAL ROWS: ".$info2[4]."]";
    $echo.="\n[APPROX MPH: ".$info2[5]."]";
    if(ECHO_CONTENT_STATS){echo_status($start_time,$count_rows,$echo);}
   }
  }

  fclose($fp);

  if(ECHO_CONTENT_STATS){echo_status($start_time,$count_rows,"FINISHED");}

 }

 run_parser();

}
else{

 echo "This script must be run from the command line: <br><br>php -q ".constant("SUCKDMOZ_DIR")."/suckDMOZ_content_parser.php  > ".constant("SUCKDMOZ_DIR")."/DMOZ_content_parser_result.txt &";

}


?> 