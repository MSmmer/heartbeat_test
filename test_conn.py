# -*- coding: utf-8 -*-
import socket, thread
from Queue import Queue
from time import sleep, time
from ConfigParser import ConfigParser
from time import gmtime, strftime

client = {}

def connect():
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.connect(("192.168.1.40", 5432))
        print "connected."
        
def heartbeat():
	global client
	while True:
                try:
                        sleep(5)
                        sent = client.send(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                        if sent == 0:
                                print "connection broken"
                        else:
                                print "status ok"
                except socket.error, msg:  # time out
                        print "error : %s" % msg
                        connect()


connect()
client.send("hello world")
thread.start_new(heartbeat,())
while True:
	sleep(1)
	pass
