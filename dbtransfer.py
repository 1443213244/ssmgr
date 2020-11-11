# -*- encoding: utf-8 -*-

from manager import Manager
import datetime
import cymysql
import socket
import logging
import json
import config
import requests
import re
import time
import os


class Dbtransfer(object):

    instance = None

    def __init__(self):
        self.last_get_transfer = {}

    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance
    
    def __init__(self, config):
        self._config = config

    @staticmethod
    def send_command(cmd):
        data = ''
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #cli.settimeout(10)
            cli.sendto(cmd, ('%s' % (config.MANAGE_BIND_IP), config.MANAGE_PORT))
            data, addr = cli.recvfrom(500000000)
            cli.close()
            # TODO: bad way solve timed out
            time.sleep(0.05)
        except:
            logging.warn('send_command response')
        return data

    def list_port(self):
        list = Dbtransfer.send_command('list')
        return list
    
    #iP
    def getouterip(self):
        url='https://api.ip.sb/ip'
        r=requests.get(url).text
        ip=r.encode("utf-8")
	ip=ip.rstrip()
        return ip


    def getall(self):
        conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                                           passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        main_ip=self.getouterip()
        cur.execute('SELECT * FROM user where main_ip= "%s"' % main_ip)
        rows = []
        for r in cur.fetchall():
            n_time = datetime.datetime.now()
            if n_time < r[6] :
                rows.append(r)
        cur.close()
        conn.close()
        return rows


    def run(self):
        device = config.DEVICE
        os.system('iptables -t mangle -F')
        os.system('tc qdisc del dev %s root > /dev/null 2>&1' % (device))
        os.system('tc qdisc add dev %s root handle 1: htb r2q 1;' %(device))
        while True:
            try:
                users_all = []
                users = []
                alls = self.getall()
                for i in range(len(alls)):
                    user_all = []
                    user = []
                    pid =  alls[i][33]
                    bandwidth = alls[i][8]
                    port = alls[i][2]
                    password = alls[i][3]
                    user_all.extend([pid, port, password, bandwidth])
                    user.extend([port, password])
                    users.append(user)
                    users_all.append(user_all)

                
                islist = []
                lists = self.list_port()
                json_str = json.loads(lists)
                for i in range(len(json_str)):
                    lists1 = []
                    lists1.extend([long(json_str[i]['server_port']),json_str[i]['password']])
                    islist.append(lists1)

                
                for i in users_all:
                    j = []
                    pid = i[0]
                    port = i[1]
                    bandwidth = i[3]
                    j.extend([i[1], i[2]])
                    if j not in islist:
                        os.system('tc class add dev %s parent 1: classid 1:%s htb rate %s ceil %s burst %s prio 0' % (device, pid, str(bandwidth) + 'mbit', str(int(bandwidth)*2) + 'mbit', str(int(bandwidth)*2*60*10) + 'k'))
                        os.system('tc filter add dev %s parent 1: protocol ip handle %s fw flowid 1:%s' % (device, pid, pid))
                        os.system('iptables -A POSTROUTING -t mangle -p tcp --sport %d -j MARK --set-mark %s' % (port, pid))
                        Dbtransfer.send_command('add: {"server_port": %s, "password":"%s"}' % (j[0], j[1]))
                    
                for i in islist:
                    if i not in users:
                        Dbtransfer.send_command('remove: {"server_port": %s}' % (i[0]))
            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.warn('db thread except:%s' % e)
            finally:
                time.sleep(10)




