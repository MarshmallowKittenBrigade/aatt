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
		$this->item		= $data['RECORDS']['ITEM'];
		$this->value	= $data['RECORDS']['VALUE'];
		$this->save();
	}

	function save(){
		$cols = "device_id,item_id,value,inserted";
		$vals = "'".$this->device . "','" . $this->item . "','" . $this->value . "',NOW()";
		$rows = $this->db->db_ins("records",$cols,$vals);
		if($rows>0){
			$this->status = true;
		}else{
			$this->status = false;
		}
		return $this->status;
	}	

 }

?>
