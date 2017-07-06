import socket, thread, time, logging
from time import sleep
from time import gmtime, strftime


class Heartbeat(object):
    addr = ""
    port = 0
    client = {}
    disconn = False
    interval = 5
    beat_data = "HB"
    log_file = "log.txt"
    logger = logging.getLogger("heartbeat")
    timeout = 15
    countdown = timeout

    def __init__(self, addr, port):
        fh = logging.FileHandler(self.log_file)
        self.logger.setLevel(logging.DEBUG)
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter("", datefmt)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.addr = addr
        self.port = port
        self.connect()
        thread.start_new(self.beat,())
        thread.start_new(self.receive,())
        thread.start_new(self.echobeat,())
        pass

    def connect(self):
        if self.disconn == True:
            return
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.client.connect((self.addr, self.port))
        except Exception, msg:
            self.err(msg)
            sleep(1)

    def beat(self):
        while self.disconn == False:
            try:
                sleep(self.interval)
                self.client.send(self.beat_data)
            except socket.error, msg:
                self.err(msg)
                self.connect()
                
    def echobeat(self):
	while self.disconn == False:
	    self.countdown = self.countdown - 1
	    sleep(1)
	    if self.countdown < 0:
		print "an error occured, server is no answer."

    def receive(self):
	while True:
	    flag = self.client.recv(8192)
	    if flag == self.beat_data:
                print "beat echo."
		self.countdown = self.timeout
				
    def close(self):
        self.disconn = true
        return

    def err(self, msg):
        print msg
        self.logger.error(msg)
        pass
