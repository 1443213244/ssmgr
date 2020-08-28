#!/usr/bin/python
from manager import Manager
from dbtransfer import Dbtransfer
import multiprocessing
import config
import time
import os


if __name__ == '__main__':
    config = {
        'method': '%s' % config.SS_METHOD,
        'manager_address': '%s:%s' % (config.MANAGE_BIND_IP, config.MANAGE_PORT),
        'timeout': 185, # some protocol keepalive packet 3 min Eg bt
        'fast_open': False,
        'verbose': 1
    }

    manager = Manager(config)
    db = Dbtransfer(config)
    p1 = multiprocessing.Process(target = manager.run)
    p2 = multiprocessing.Process(target = db.run)
    p1.start()
    time.sleep(0.2)
    p2.start()
