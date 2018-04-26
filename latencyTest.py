#!/usr/bin/env python3
# coding=UTF-8

import rados
import shlex
import json
from time import time, sleep
from subprocess import Popen, PIPE



def mainLIB(times=10):
    start = time()
    cmd = {"prefix": "status", "format": "json"}

    cluster = rados.Rados(conffile = "/etc/ceph/ceph.conf", conf = dict (keyring = "/etc/ceph/ceph.client.admin.keyring"))
    cluster.connect()

    for x in range(1,times):
        
        stat, res, err = cluster.mon_command(json.dumps(cmd), "")

        if stat == 0:
            resJSON = json.loads(res.decode("UTF-8"))
            
        else:
            print("ERROR ({}) : {}".format(stat, err))
            break;
    stop = time()
    print("{} s".format(round(stop-start, 3)))


def mainCLI(times=10):
    start = time()
    cmd = "ceph status -f json"

    for x in range(1,times):
        p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)

        stdout_data, stderr_data = p.communicate()

        if p.returncode == 0:
            resJSON = json.loads(stdout_data.decode("UTF-8"))

        else:
            print("ERROR ({}) : {}".format(p.returncode, stderr_data.decode("UTF-8")))
            break;

    stop = time()
    print("{} s".format(round(stop-start, 3)))

if __name__ == '__main__':
    print("starting Latency Test")

    print("Test LIB ...")
    mainLIB(100)
    print("Test LIB Finished")
    print("sleep 5s")
    sleep(5)

    print("First Test CLI")
    mainCLI(100)
    print("Test CLI Finished")