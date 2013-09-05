<?php

require_once($_SERVER['DOCUMENT_ROOT']."/includes/aatt_config.php");

class System{

	static function addLog($msg,$level){
    	openlog(APPNAME,LOG_NDELAY,SYSLOGFACILITY);
    	syslog($level,$msg);
    	closelog();
	}
}
