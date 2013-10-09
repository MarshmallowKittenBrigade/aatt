#!/usr/bin/python

import json, sys, MySQLdb, hashlib
from lib import System

class Processor:

	def __init__(self,sent):
		self.raw = json.loads(sent)
		self.data = {}
		self.auth = {}
		self.response = {}
		self.act = ""
		self.records = {}
		self.checks = {}
		self.changes = {}
		self.updates = {}

		config = System.Config('/opt/aatt/etc/config.ini')
		cfg = config.getConfig()

		self.aattlog = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])

		self.db = MySQLdb.connect(host=cfg['dbhost'],user=cfg['dbuser'],passwd=cfg['dbpass'],db=cfg['dbname'])
		self.checker = Validator(sent)
		try:
			self.checker.validJson()
		except:
			self.response["STATUS"] = "FAIL"
			self.response["RESPONSE"] = "BADJSON"
			self.aattlog.log("WARNING: STATUS %s RESPONSE %s" % (self.response["STATUS"],self.response["RESPONSE"]))

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
			except Exception as e:
				self.response["STATUS"] = "FAIL"
				self.response["RESPONSE"] = "KEYNOTEXIST"
				self.aattlog.log("WARNING: STATUS %s RESPONSE %s" % (self.response["STATUS"],self.response["RESPONSE"]))
	
	def record(self,deviceId,endpointId,value):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "INSERT INTO endpoint_data (device_id,endpoint_id,value) VALUES(%s,%s,%s)" % (deviceId,endpointId,value)
		try:
			c.execute(sql)
			self.aattlog.log("INFO: Added data for endpoint %s" % (endpointId))
		except Exception, e:
			self.aattlog.log("ERROR: %s " % (e))
			self.db.rollback()
			c.close()
			return False
		self.db.commit()
		c.close()
		return True

	def check(self,attributeId):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT new FROM state WHERE attribute_id=%s" %(attributeId)
		c.execute(sql)
		results = c.fetchall()
		for value in results:
			return value
		c.close()

	def set(self,attributeId,state):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "INSERT INTO state (attribute_id,new) VALUES (%s,%s) ON DUPLICATE KEY UPDATE new=%s" % (attributeId,state,state)
		try:
			c.execute(sql)
			self.aattlog.log("INFO: Added new state request for attribute %s" % (attributeId))
		except Exception, e:
			self.aattlog.log("ERROR: %s " % (e))
			self.db.rollback()
			c.close()
			return False
		self.db.commit()
		c.close()
		return True

	def update(self,attributeId,state):
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "INSERT INTO state (attribute_id,current) VALUES (%s,%s) ON DUPLICATE KEY UPDATE current=%s" % (attributeId,state,state)
		try:
			c.execute(sql)
			self.aattlog.log("INFO: Updated current state for attribute %s" % (attributeId))
		except Exception, e:
			self.aattlog.log("ERROR: %s " % (e))
			self.db.rollback()
			c.close()
			return False
		self.db.commit()
		c.close()
		return True

	def process(self):
		self.parse()
		foo = Auth(self.auth)
		if foo.login():
			self.checker.getAssets(foo.getId())
			rowcount = 0
			self.aattlog.log("ACT: %s" % self.act)
			if self.act == "RECORD":
				self.records = self.data["RECORDS"]
				for endpoint in self.records:
					if self.checker.validEndpoint(endpoint):
						self.record(self.device,endpoint,self.records[endpoint])
						rowcount += 1
					else:
						self.aattlog.log("ERROR: BAD RECORD - ENDPOINT %s NOT ON ACCT" % (endpoint))
				self.response = {"STATUS":"SUCCESS","RESPONSE":{"RECORDED":rowcount}}
				self.aattlog.log("INFO: Successfully recorded %d items" % (rowcount))
			elif self.act == "CHECK":
				state = {}
				self.checks = self.data["CHECKS"]
				for endpoint in self.checks:
					if self.checker.validEndpoint(endpoint):
						state[endpoint] = {}
						for attribute in endpoint:
							if self.checker.validAttribute(attribute):
								checkResult = self.check(attribute)
								if checkResult:
									state[endpoint][attribute] = checkResult
								else:
									state[endpoint][attribute] = "ATTNOTEXIST"
					self.aattlog.log("ERROR: BAD CHECK - ENDPOINT %s NOT ON ACCT" % (endpoint))
				if not state:
					self.response = {"STATUS":"FAIL","RESPONSE":"EPNOTEXIST"}
					self.aattlog.log("WARNING: Endpoint does not exist")
				else:
					self.response = {"STATUS":"SUCCESS","RESPONSE":state}
					self.aattlog.log("INFO: Successfully returned results of check")
			elif self.act == "SET":
				self.changes = self.data["CHANGES"]
				for attribute in self.changes:
					self.set(attribute,self.changes[attribute])
					rowcount += 1
				self.response = {"STATUS":"SUCCESS","RESPONSE":{"SET":rowcount}}
				self.aattlog.log("INFO: Successfull set %d items" % (rowcount))
			elif self.act == "UPDATE":
				self.updates = self.data["UPDATES"]
				for attribute in self.updates:
					self.update(attribute,self.updates[attribute])
					rowcount += 1
				self.response = {"STATUS":"SUCCESS","RESPONSE":{"UPDATED":rowcount}}
				self.aattlog.log("INFO: Successfull updated %d items" % (rowcount))

		elif not foo.login():
			self.response = {"STATUS":"FAIL","RESPONSE":"AUTHFAIL"}
		return json.dumps(self.response)

class Auth:

	def __init__(self,auth):
		self.response = {}
		self.app = ""
		self.account = ""
		self.key = ""
		self.id = ""

		try:
			self.app		= auth['APP']
			self.account	= auth['ACCOUNT']
			self.key		= auth['KEY']
		except Exception as e:
			self.response['STATUS'] = 'FAIL'
			self.response['RESPONSE'] = 'NOAUTH'

		config = System.Config('/opt/aatt/etc/config.ini')
		cfg = config.getConfig()

		self.aattlog = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])

		self.db = MySQLdb.connect(host=cfg['dbhost'],user=cfg['dbuser'],passwd=cfg['dbpass'],db=cfg['dbname'])

	def login(self):

		pw = hashlib.md5(self.key + "phoolsalt").hexdigest()
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT * FROM account WHERE account_code='%s' AND account_key='%s'" % (self.account,pw)
		try:
			c.execute(sql)
			accts = c.fetchone()
			self.id = accts['id']
			c.close()
		except Exception as e:
			self.aattlog.log("WARNING: Authentication query failed.")
			return False
		if(int(self.id)):
			self.aattlog.log("INFO: Login Sucessful")
			return True
		else:
			return False

	def getId(self):
		return self.id


class Validator:

	def __init__(self,json):
		self.json = json
		self.assets = {}
		self.assets['devices'] = []
		self.assets['endpoints'] = []
		self.assets['attributes'] = []

		config = System.Config('/opt/aatt/etc/config.ini')
		cfg = config.getConfig()
		self.aattlog = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])
		self.db = MySQLdb.connect(host=cfg['dbhost'],user=cfg['dbuser'],passwd=cfg['dbpass'],db=cfg['dbname'])

	def validJson(self):
		try:
			json.loads(self.json)
			return True
		except Exception, e:
			return False

	def validDevice(self,deviceId):
		return deviceId in self.assets['devices']

	def validEndpoint(self,endpointId):
		return endpointId in self.assets['endpoints']

	def validAttribute(self,attributeId):
		return attributeId in self.assets['attributes']

	def getAssets(self,id):
		sql = "select d.id as device, ep.id as endpoint, a.id as attribute from device d left join endpoint ep on (d.id=device_id) left join attribute a on (ep.id=a.endpoint_id) where account_id=%s" % (id)
		c = self.db.cursor(MySQLdb.cursors.DictCursor)
		try:
			c.execute(sql)
		except Exception, e:
			self.aattlog.log("ERROR: %s" % (e))

		rows = c.fetchall()
		for row in rows:
			self.assets['devices'].append(row['device'])
			self.assets['endpoints'].append(row['endpoint'])
			self.assets['attributes'].append(row['attribute'])

		#self.aattlog.log("DEVICES: " + str(self.assets['devices']).strip('[]'))
		#self.aattlog.log("ENPOINTS: " + str(self.assets['endpoints']).strip('[]'))
		#self.aattlog.log("ATTRIBUTES: " + str(self.assets['attributes']).strip('[]'))
