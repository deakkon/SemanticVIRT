<?php

class baza {
	
	//SPAJANJE NA MYSQL
	//-----------------
	function query_mysql($sql){
		//return ms_remote($sql);
		return baza::ms_local($sql);
	}
	
	function ms_local($sql){
		baza::db_connect_local();
		$result = mysql_query($sql) or die(mysql_error());
		//baza::db_disconnect();
		return $result;
	}

	function ms_remote($sql){
		set_time_limit(0);
		baza::db_connect_remote();
		$result = mysql_query($sql) or die(mysql_error());
		baza::db_disconnect();
		return $result;
	}

	function db_connect_local() {
		set_time_limit(0);
		$host="localhost";
		$user="root";
		$pass="";
		$baza="test";
		$dbc = mysql_pconnect($host, $user, $pass) or die (mysql_error());;
		$db = mysql_select_db($baza, $dbc) or die (mysql_error());;
	}
	
	function db_connect_remote() {

	}	

	function db_disconnect() {
		mysql_close();
	}	
}

?>