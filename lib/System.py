#!/usr/bin/python

import syslog, ConfigParser

class Log:
	def __init__(self,host,facility,name):
		self.host = host
		self.facility = facility
		self.name = name

	def log(self,msg):
		syslog.openlog(self.name,syslog.LOG_PID,syslog.LOG_LOCAL0)
		syslog.syslog(msg)
		syslog.closelog()

class Config:
	global configs
	def __init__(self,file):
		self.configs = {}
		config = ConfigParser.ConfigParser()
		config.read(file)

		self.configs['port']			= config.getint("main","port")
		self.configs['debug']			= config.get("main","debug")
		self.configs['syslogHost']		= config.get("syslog","host")
		self.configs['syslogFacility']	= config.get("syslog","facility")
		self.configs['syslogName']		= config.get("syslog","name")
		self.configs['dbhost']			= config.get("db","host")
		self.configs['dbuser']			= config.get("db","user")
		self.configs['dbpass']			= config.get("db","password")
		self.configs['dbname']			= config.get("db","name")

	def getConfig(self):
		return self.configs
