<?php
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.db.php");
require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.connection.php");

 class Check{
	private $status;
	private $device;
	private $item;
	private $trigger;
	private $action;
	private $db;

	function __construct($data){
		if(!$data['DEVICE'] || !$data['CHECKS']){
			return false;
		}
		$this->db		= new DB();
		$this->device	= $data['DEVICE'];
		$this->checks	= $data['CHECKS'];
	}

	function save(){
		foreach($this->checks as $item){
			$sql = "SELECT * FROM actions WHERE device_id='".$this->device."' AND item_id='".$item."'";
			$result = $this->db->db_query_row($sql);
			$actions[$item] = $result['action'];
		}
		$response['STATUS'] = 'SUCCESS';
		$response['RESPONSE'] = $actions;
		return $response;
	}

 }

?>
