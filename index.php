<?php

require_once($_SERVER['DOCUMENT_ROOT']."/includes/class.db.php");
echo '<h3>AATT</h3>';

$db = new DB();
if($db){
	echo "Database connection successful!<br />";
}else{
	echo "Database connection failed!<br />";
}
?>
