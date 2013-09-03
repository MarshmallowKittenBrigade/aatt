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
		$this->db		= new DB();
		$this->device	= $data['DEVICE'];
		$this->item		= $data['ITEM'];;
		$this->save();
	}

	function save(){
		$sql = "SELECT * FROM actions WHERE device_id='".$this->device."' AND item='".$this->item."'";
		return $db->db_query_result($sql);;
	}	

 }

?>
