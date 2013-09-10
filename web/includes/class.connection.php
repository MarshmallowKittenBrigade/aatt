<?php

require_once($_SERVER['DOCUMENT_ROOT'].'/includes/class.db.php');
require_once($_SERVER['DOCUMENT_ROOT'].'/includes/class.system.php');

class Connection {

  private $app;
  private $account_code;
  private $account_key;
  private $db;

  function __construct($creds){
    $this->app = $creds['APP'];
    $this->account_code = $creds['ACCOUNT'];
	$this->account_key = md5($creds['KEY']."phoolsalt");
    $this->db = new DB();;
  }

  function establish() {
	$sql = "select count(*) as apps from app where app_name='$this->app'";
	$result = $this->db->db_query_result($sql);
    if($result['apps'] > 0){
        $query = 'select count(*) from account where account_code="'.$this->account_code.'" AND account_key="'.$this->account_key.'"';
        $result = $this->db->db_query_result($query);
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
