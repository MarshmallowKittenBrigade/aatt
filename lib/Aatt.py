#!/usr/bin/python

import json, sys, MySQLdb, hashlib
from lib import System

class Processor:

	def __init__(self,sent):
		self.raw = {}
		self.data = {}
		self.auth = {}
		self.response = {}
		self.act = ""
		self.records = {}
		self.checks = {}

		config = System.Config('/opt/aatt/etc/config.ini')
		cfg = config.getConfig()

		self.meh = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])

		self.db = MySQLdb.connect(host=cfg['dbhost'],user=cfg['dbuser'],passwd=cfg['dbpass'],db=cfg['dbname'])
		try:
			self.raw = json.loads(sent)
		except:
			self.response["STATUS"] = "FAIL"
			self.response["RESPONSE"] = "BADJSON"
			self.meh.log(json.dumps(self.response))

	def getRaw(self):
		return json.dumps(self.raw).encode("utf-8")

	def getData(self):
		return json.dumps(self.data).encode("utf-8")

	def getAct(self):
		return self.act.encode("utf-8")

	def getAuth(self):
		return json.dumps(self.auth).encode("utf-8")

	def getChecks(self):
		return json.dumps(self.data["CHECKS"]).encode("utf-8")

	def parse(self):
		if(self.response == {}):
			try:
				self.act	= self.raw["ACT"]
				self.data	= self.raw["DATA"]
				self.device	= self.raw["DATA"]["DEVICE"]
				self.auth	= self.raw["AUTH"]
			except:
				self.response["STATUS"] = "FAIL"
				self.response["RESPONSE"] = "KEYNOTEXIST"
				self.meh.log(json.dumps(self.response))
	
	def add(self,deviceId,endpointId,value):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "INSERT INTO endpoint_data (device_id,endpoint_id,value) VALUES('"+deviceId+"','"+endpointId+"','"+value+"')"
		try:
			c.execute(sql)
		except:
			self.db.rollback()
			c.close()
			return False
		self.db.commit()
		c.close()
		return True

	def check(self,attributeId):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT current,previous FROM state WHERE attribute_id='%s'" %(attributeId)
		c.execute(sql)
		results = c.fetchall()
		for value in results:
			return value
		c.close()

	def process(self):
		self.parse()
		foo = Auth(self.auth)
		if(foo.login() == True):
			rowcount = 0
			self.meh.log("ACT: %s" % self.act)
			if self.act == "RECORD":
				self.records = self.data["RECORDS"]
				for endpoint in self.records:
					self.add(self.device,endpoint,self.records[endpoint])
					rowcount += 1
				self.response = {"STATUS":"SUCCESS","RESPONSE":{"RECORDED":rowcount}}
			elif self.act == "CHECK":
				state = {}
				self.checks = self.data["CHECKS"]
				for endpoint in self.checks:
					state[endpoint] = {}
					for attribute in endpoint:
						checkResult = self.check(attribute)
						if checkResult:
							state[endpoint][attribute] = checkResult
						else:
							state[endpoint][attribute] = "ATTNOTEXIST"
				if not state:
					self.response = {"STATUS":"FAIL","RESPONSE":"EPNOTEXIST"}
				else:
					self.response = {"STATUS":"SUCCESS","RESPONSE":state}
		elif(foo.login() == False):
			self.response = {"STATUS":"FAIL","RESPONSE":"AUTHFAIL"}
		return json.dumps(self.response)

class Auth:

	def __init__(self,auth):
		self.response = {}
		self.app = ""
		self.account = ""
		self.key = ""

		try:
			self.app		= auth['APP']
			self.account	= auth['ACCOUNT']
			self.key		= auth['KEY']
		except:
			self.response['STATUS'] = 'FAIL'
			self.response['RESPONSE'] = 'NOAUTH'

		config = System.Config('/opt/aatt/etc/config.ini')
		cfg = config.getConfig()

		self.meh = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])

		self.db = MySQLdb.connect(host=cfg['dbhost'],user=cfg['dbuser'],passwd=cfg['dbpass'],db=cfg['dbname'])

	def login(self):

		pw = hashlib.md5(self.key + "phoolsalt").hexdigest()
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT COUNT(*) as foo FROM account WHERE account_code='%s' AND account_key='%s'" % (self.account,pw)
		try:
			c.execute(sql)
			accts = c.fetchone()
			c.close()
		except:
			self.meh.log("Authentication query failed: ")
			return False
		if(int(accts['foo']) > 0):
			self.meh.log("Login Sucessful")
			return True
		else:
			return False
