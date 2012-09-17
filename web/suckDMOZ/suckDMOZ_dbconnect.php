<?php

#####################################
#
# Built:07/18/01 -brs-
# Last-Touched:06/24/02 -brs-
# PHPBuild: Apache/1.3.14 (RHLinux7) PHP/4.0.3pl1
#
#####################################

function suckDMOZ_structure_dbconnect($fields,$proc){

 switch($proc){
  
  case "select":		
          if($fields[0]!=""&&$fields[1]!=""){
           $limit = " LIMIT $fields[0],$fields[1]";
          }

          $select_fields ="container_type,";
          $select_fields.="container_category_name,";
          $select_fields.="sub_container_type,";
          $select_fields.="sub_container_content,";
          $select_fields.="catid";

          $type	="select_many";
          $qry1	="SELECT $select_fields FROM DMOZ_structure WHERE ";
          $qry1.="container_category_name='".$fields[3]."' ".$limit;
          break;	
  case "create":
          $type	 ="create";
          $qry1  ="CREATE TABLE DMOZ_structure (";
          $qry1 .="container_type varchar(255) NOT NULL,";
          $qry1 .="container_category_name varchar(255) NOT NULL,";
          $qry1 .="sub_container_type varchar(255) NOT NULL,";
          $qry1 .="sub_container_content varchar(255) NOT NULL,";
          $qry1 .="catid varchar(10) NOT NULL,";
          $qry1 .="KEY container_category_name (container_category_name),";
          $qry1 .="KEY catid (catid),";
          $qry1 .="UNIQUE uniq (catid, sub_container_content));";
          break;

  case "insert":		

          $insert_fields ="container_type,";
          $insert_fields.="container_category_name,";
          $insert_fields.="sub_container_type,";
          $insert_fields.="sub_container_content,";
          $insert_fields.="catid";

          $insert_values="'".addslashes($fields[0])."',";
          $insert_values.="'".addslashes($fields[1])."',";
          $insert_values.="'".addslashes($fields[2])."',";
          $insert_values.="'".addslashes($fields[3])."',";
          $insert_values.="'".$fields[4]."'";

          $type="insert";
          $qry1	 =	"INSERT INTO DMOZ_structure($insert_fields) VALUES($insert_values)";
          break;
 }

 $db = mysql_connect(MY_MYSQL_DB_ADDR,MY_MYSQL_USER,MY_MYSQL_PASS);
 if(!(mysql_select_db(MY_MYSQL_DB_NAME, $db))){die(mysql_errno($db)." - ".mysql_error($db));}

 $result = @mysql_query($qry1,$db);
 
 if($error = @mysql_error($db)){
  $errno = @mysql_errno($db);
  $return[]="error";
  $return[]=$errno;
  $return[]=$error;
 }	
 else{
  switch($type){
   case "select_many":	$return[]=$type;	$return[]=@mysql_num_rows($result);	$return[]=$result;break;
   case "insert":		$return[]=$type;$return[]=@mysql_insert_id($db);break;
  }
 }
 
 if($return==""){$return[]=$result;}
 return $return;

}








function suckDMOZ_content_dbconnect($fields,$proc){
 switch($proc){

  case "select":		
          if($fields[0]!=""&&$fields[1]!=""){
           $limit = " LIMIT $fields[0],$fields[1]";
          }
          if($fields[3]!=""){
           $where = " WHERE container_category_name='".$fields[3]."' ";
          }

          $select_fields ="container_type,";
          $select_fields.="container_category_name,";
          $select_fields.="sub_container_type,";
          $select_fields.="sub_container_content,";
          $select_fields.="catid";

          $type="select_many";
          $qry1="SELECT $select_fields FROM DMOZ_content ".$where.$limit;
          break;			
  case "create":
          $type	 ="create";
          $qry1  ="CREATE TABLE DMOZ_content (";
          $qry1 .="container_type varchar(255) NOT NULL,";
          $qry1 .="container_category_name varchar(255) NOT NULL,";
          $qry1 .="sub_container_type varchar(255) NOT NULL,";
          $qry1 .="sub_container_content varchar(255) NOT NULL,";
          $qry1 .="catid varchar(10) NOT NULL,";
          $qry1 .="KEY container_category_name (container_category_name),";
          $qry1 .="KEY catid (catid),";
          $qry1 .="UNIQUE uniq (catid, sub_container_content));";
          break;

  case "insert":		

          $insert_fields ="container_type,";
          $insert_fields.="container_category_name,";
          $insert_fields.="sub_container_type,";
          $insert_fields.="sub_container_content,";
          $insert_fields.="catid";

          $insert_values="'".addslashes($fields[0])."',";
          $insert_values.="'".addslashes($fields[1])."',";
          $insert_values.="'".addslashes($fields[2])."',";
          $insert_values.="'".addslashes($fields[3])."',";
          $insert_values.="'".$fields[4]."'";

          $type="insert";
          $qry1	 =	"INSERT INTO DMOZ_content($insert_fields) VALUES($insert_values)";
          break;
 }

 $db = mysql_connect(MY_MYSQL_DB_ADDR,MY_MYSQL_USER,MY_MYSQL_PASS);
 if(!(mysql_select_db(MY_MYSQL_DB_NAME, $db))){die(mysql_errno($db)." - ".mysql_error($db));}

 $result = @mysql_query($qry1,$db);
 
 if($error = @mysql_error($db)){
  $errno = @mysql_errno($db);
  $return[]="error";
  $return[]=$errno;
  $return[]=$error;
 }	
 else{
  switch($type){
   case "select_many":	$return[]=$type;	$return[]=@mysql_num_rows($result);	$return[]=$result;break;
   case "insert":		$return[]=$type;$return[]=@mysql_insert_id($db);break;
  }
 }
 
 if($return==""){$return[]=$result;}
 return $return;

}





function getmicrotime(){ 
	list($usec, $sec) = explode(" ",microtime()); 
	return ((float)$usec + (float)$sec); 
}





function echo_status($start_time,$count_rows,$milestone){

 $end_time = getmicrotime();
 $time = $start_time - $end_time;
 $dot = strrpos($time,".");
 $script_time = abs(substr($time,0,$dot+2));

  $h="0";$m="0";$s = intval($script_time % 60);
  if($script_time>60){$m = intval($script_time / 60) % 60;} 
 if($script_time>3600){$h = intval($script_time / 3600);}

 echo "\n";
 echo " -- ".$milestone." --\n";
 echo "TIME [".date("m/d/y - H:i:s")."]\n";
 echo "Script run time: ".$h.":".$m.":".$s."\n";
 echo "Total Rows: ".$count_rows."\n";
 echo " --\n";
 echo "\n";
 
 flush();

}





function footspeed($num_per_sec,$length){
 $mph = round($num_per_sec*.6818*$length);
 return $mph; // length is in feet - or suppossed to be ;)
}




function get_file_info($proc,$filename,$currentbytes,$start_time,$count_rows){
 $ext = array("B","KB","MB","GB","TB"); 
  switch($proc){
   case "1":
    $file_size = filesize($filename); 
    $j = 0;
    while($file_size>=pow(1024,$j)){
     ++$j;
     $adj_file_size=round($file_size/pow(1024,$j-1)*100)/100;
     $adj_file_size=$adj_file_size.$ext[$j-1];
    }
    $file_size_benchmark=$file_size/20;

    $return[0]=$file_size;
    $return[1]=$file_size_benchmark;
    $return[2]=$adj_file_size;
    break;

   case "2":
    $file_size = filesize($filename);
    $file_left = $file_size-$currentbytes;
    $j = 0;
    while($file_left>=pow(1024,$j)){
     ++$j;
     $adj_file_left=round($file_left/pow(1024,$j-1)*100)/100;
     $adj_file_left=$adj_file_left.$ext[$j-1];
    }
    $percent_left = round($file_left/$file_size*100);

    $cur_time = getmicrotime();
  
    $elapsed_time=abs($start_time-$cur_time);
    $tot_time=abs($file_size*$elapsed_time/$currentbytes);
    $approx_time_left=$tot_time-$elapsed_time;

    $lh="0";$lm="0";$ls = intval($approx_time_left % 60);
    if($approx_time_left>60){$lm = intval($approx_time_left / 60) % 60;} 
    if($approx_time_left>3600){$lh = intval($approx_time_left / 3600);}

    $th="0";$tm="0";$ts = intval($tot_time % 60);
    if($tot_time>60){$tm = intval($tot_time / 60) % 60;} 
    if($tot_time>3600){$th = intval($tot_time / 3600);}

    $tot_rows = round($tot_time*$count_rows/$elapsed_time);

    $mph = footspeed($tot_rows/$elapsed_time,"1");

    $return[0]=$adj_file_left;
    $return[1]=$percent_left;
    $return[2]=$lh.":".$lm.":".$ls; // approx time left
    $return[3]=$th.":".$tm.":".$ts; // approx total time
    $return[4]=$tot_rows; // approx total rows
    $return[5]=$mph; // approx mph
    break;
  }
 return $return;
}




function store_data($container_type,$container_category_name,$sub_container_type,$sub_container_content,$catid,$mode){
	global $count_rows,$start_time,$echo_tally;

	$fields[0]=$container_type;
	$fields[1]=$container_category_name;
	$fields[2]=$sub_container_type;
	$fields[3]=$sub_container_content;
	$fields[4]=$catid;
	if($mode=="structure"){
  $result = suckDMOZ_structure_dbconnect($fields,"insert");
	}
 else{
  $result = suckDMOZ_content_dbconnect($fields,"insert");
 }
 $echo_tally++;
	$count_rows++;
	
	if($echo_tally>100000){
		$echo_tally=0;		
		if(ECHO_CONTENT_STATS){echo_status($start_time,$count_rows,"100,000 MORE ROWS");}
	}

}




?>