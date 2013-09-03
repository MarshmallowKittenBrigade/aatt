<?php

require_once($_SERVER['DOCUMENT_ROOT'].'/includes/class.db.php');
require_once($_SERVER['DOCUMENT_ROOT'].'/includes/class.system.php');

class Connection {

  private $app;
  private $account_code;
  private $account_key;
  private $mysql;

  function __construct($creds){
    $this->app = $creds['APP'];
    $this->account_code = $creds['ACCOUNT'];
	$this->account_key = md5($creds['KEY']."phoolsalt");
    $this->mysql = new DB();;
  }

  function establish() {
    if($this->app == APPNAME){
        $query = 'select count(*) from accounts where account_code="'.$this->account_code.'" AND account_key="'.$this->account_key.'"';
        $result = $this->mysql->db_query_result($query);
        if($result > 0){
            $return['STATUS'] = "SUCCESS";
            $return['RESPONSE'] = "AUTHORIZED";
        }else{
            $return['STATUS'] = "SUCCESS";
            $return['RESPONSE'] = "ACCOUNTNOTREG";
            print json_encode($return);
            die();
        }
    }else{
        $return['STATUS'] = "SUCCESS";
        $return['RESPONSE'] = "APPNOTREG";
        print json_encode($return);
        die();
    }
    return TRUE;
  }
}
?>
