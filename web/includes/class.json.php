<?php
require_once($_SERVER['DOCUMENT_ROOT'].'/includes/class.system.php');

class Json {

  private $input = array();

  function __construct($input) {
        $this->input = json_decode($input,TRUE);
  }

  function getArray(){
        return $this->input;
  }

  function getArrayByKey($key){
        if(isset($this->input[$key])){
          foreach ($this->input[$key] as $k=>$v){
                $return[$k] = $v;
          }
        }else{
              $return[$key] = "KEYNOTEXIST";
        }
        return $return;
  }

  function getValueByKey($key){
        if(isset($this->input[$key])){
          return $this->input[$key];
        }
  }

  function keyExists($key){
        if(isset($this->input[$key])){
          return true;
        }else{
          return false;
        }
  }

  function getData(){
      return $this->getArrayByKey('DATA');
  }

  function getAct(){
      return $this->getValueByKey('ACT');
  }

  function getAuth(){
      return $this->getArrayByKey('AUTH');
  }

  function getRaw(){
	  return $this->input;
  }
}

?>
