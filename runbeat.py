from heartbeat import Heartbeat
from time import sleep


a = Heartbeat("192.168.1.40", 5432)

while True:
    sleep(1)
