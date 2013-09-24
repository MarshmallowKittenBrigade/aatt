#!/usr/bin/python

from lib import Aatt, System
import sys, getopt, socket, time


def main(argv):
	config = System.Config('/opt/aatt/etc/config.ini')
	cfg = config.getConfig()
	
	meh = System.Log(cfg['syslogHost'],cfg['syslogFacility'],cfg['syslogName'])

	host = ''
	port = cfg['port']
	backlog = 256
	size = 1024
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((host,port))
	sock.listen(backlog)

	try:
		opts, args = getopt.getopt(argv, "p:",["port=","debug"])
	except getopt.GetoptError:
		print './server.py -p <port> [--debug]'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-p","--port"):
			port = arg
		if opt is "--debug":
			debug = True
	
	meh.log("Starting server on port " + str(cfg['port']))
	
	while 1:
		client, address = sock.accept()
		start = int(round(time.time() * 1000))
		meh.log("Connection from %s" % (str(address)))
		data = client.recv(size)
		if data:
			aatt = Aatt.Processor(data)
			client.send(aatt.process())
			client.close()
			duration = (int(round(time.time() * 1000))) - start
			meh.log("STATS: Process Time - %i ms" % (duration))

if __name__ == "__main__":
	main(sys.argv[1:])
