import socket
import json
import time
import os

class Manager(object):


    def __init__(self, config):
        self._config = config
        self._cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._cli.bind(('0.0.0.0',6002))  # address of the client 
       


    def send_data(self):
        cli.send(b'add: {"server_port":'+ str(port + i)+', "password":"7cd308cc059"}')
        print(cli.recv(1506)+"\n")  # You'll receive 'ok'
       

    def start_port(self):

        self._cli.connect(('127.0.0.1',6001))  # address of Shadowsocks manager
        port = 8080

        for i in range(1, 200):
            print(i)
            self._cli.send(b'add: {"server_port":'+ str(port + i)+', "password":"7cd308cc059"}')
            print(self._cli.recv(1506)+"\n")  # You'll receive 'ok'

        # while True:
        #     #cli.send(b'list')
        #     cli.send(b'ping') 
        #     print(cli.recv(999999999)) # when data is transferred on Shadowsocks, you'll receive stat info every 10 seconds
        #     time.sleep(10)

    def add_port(self):
        print("add port")
        self._cli.send(b'add: {"server_port":9000, "password":"7cd308cc059"}')
        print(self._cli.recv(1506)+"\n")  # You'll receive 'ok'
        
    def run(self):
        #print(config['method'])
        os.system('ss-manager -m '+self._config['method']+' -u --manager-address 127.0.0.1:6001')
        self.start_port()
       
        

