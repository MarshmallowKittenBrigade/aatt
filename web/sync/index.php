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
$auth = $json->getAuth();
echo "\n$raw_post\n\n";
if(isset($auth['AUTH']) && $auth['AUTH'] == 'KEYNOTEXIST'){
 $data['STATUS'] = 'FAIL';
 $data['RESPONSE'] = 'NOTAUTHORIZED';
}else{
 $connection = new Connection($auth);
 $connection->establish();
 switch ($json->getAct()){
	case 'RECORD':
	 $rec = new Record($json->getData());
	 $data = $rec->save();
	 break;
	case 'CHECK':
	 $chk = new Check($json->getData());
	 $data = $chk->save();
	 break;
	default:
	 $data['STATUS'] = 'FAIL';
	 $data['RESPONSE'] = 'BADACT';
	 break;
 }
}
output($json->getAct(),$data,$starttime);
die();

function output($action,$return,$starttime){
    print json_encode($return);
    System::addLog($action.":".(microtime(true)-$starttime),LOG_INFO);
}

?>
