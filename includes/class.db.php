<?php
	require_once($_SERVER['DOCUMENT_ROOT']."/includes/aatt_config.php");

class DB{
	private $username;
	private $password;
	private $database;
	private $host;
	private $res;
	
	function __construct(){
		switch($db){
			default:
			 $this->host 		= DBHOST;
			 $this->username	= DBUSER;
			 $this->database	= DBNAME;
			 $this->password	= DBPASS;
			 break;
		}
	}

	function connect(){
		$err_level = error_reporting(0);
        $this->res = mysql_connect($this->host, $this->username, $this->password) or die(mysql_error());
		error_reporting($err_level);
        mysql_select_db($this->database) or die(mysql_error());
        return $this->res;
    }

    function db_query_row($sql){
        $connect =  $this->connect();
        $result = mysql_query($sql,$connect);
        $back =  mysql_fetch_row($result,0);
        mysql_close();
        return $back;
    }

    function db_query_result($sql){
        $connect = $this->connect();
        $back = $this->db_query_row($sql,$connect);
        return $back[0];
    }

	function db_ins($table,$cols,$vals){
		$connect = $this->connect();
		$sql = "INSERT INTO $table ($cols) VALUES $vals";
		$result = mysql_query($sql,$connect);
		return mysql_affected_rows($connect);
	}

	function db_del($table,$where){
		$connect = $this->connect();
		$sql = "UPDATE $table SET deleted=1 WHERE $where";
		$result = mysql_query($sql.$connect);
		return mysql_affected_rows($connect);
	}

	function getError(){
		return mysql_error($this->res);
	}

}

?>	
