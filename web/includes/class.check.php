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
		foreach($this->checks as $endpoint=>$attributes){
			foreach($attributes as $attribute){
				$sql = "SELECT * FROM state s join attribute a on s.attribute_id=a.id WHERE attribute_id='".$attribute."' AND endpoint_id='".$endpoint."'";
				$result = $this->db->db_query_row($sql);
				$actions[$endpoint][$attribute] = $result['current'];
			}
		}
		$response['STATUS'] = 'SUCCESS';
		$response['RESPONSE'] = $actions;
		return $response;
	}

 }

?>
