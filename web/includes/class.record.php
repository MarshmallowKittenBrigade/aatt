<?php
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.db.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.connection.php");

 class Record{
	private $status;
	private $device;
	private $item;
	private $value;
	private $db;

	function __construct($data){
		$this->db		= new DB();
		$this->device	= $data['DEVICE'];
		$this->records	= $data['RECORDS'];
	}

	function save(){
		$tmp = '';
		$cols = "device_id,item_id,value,inserted";
		foreach ($this->records as $item=>$value){
			$tmp .="('$this->device','$item','$value',NOW()),";
		}
		$vals = substr($tmp,0,-1);
		$rows = $this->db->db_ins("records",$cols,$vals);
		if($rows>0){
			$response['STATUS'] = 'SUCCESS';
			$response['RESPONSE']['RECORDED'] = $rows;
		}else{
			$response['STATUS'] = 'FAIL';
			$response['RESPONSE'] = 'NOTRECORDED';
		}
		return $response;
	}	

 }

?>
