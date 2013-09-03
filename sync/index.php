<?php

require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.db.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.connection.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.json.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.record.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.check.php");

$starttime = microtime(true);
$auth = array();
$return = array();

$raw_post = file_get_contents('php://input');
$json = new Json($raw_post);
print_r($json->getRaw());
$auth = $json->getAuth();

$connection = new Connection($auth);
$connection->establish();

if(isset($auth['AUTH']) && $auth['AUTH'] == 'KEYNOTEXIST'){
	echo "BAD REQUEST";
}else{
 switch ($json->getAction()){
	case 'RECORD':
	 $data = new Record($json->getData());
	 break;
	case 'CHECK':
	 $data = new Check($json->getData());
	 break;
	default:
	 $data['STATUS'] = 'FAIL';
	 $data['RESPONSE'] = 'BADACT';
	 break;
 }
output($json->getAction(),$data,$starttime);
die();
}

function output($action,$return,$starttime){
    print json_encode($return);
    System::addLog($action." - ".(microtime(true)-$starttime),LOG_INFO);
}

?>
