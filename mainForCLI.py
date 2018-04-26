#!/usr/bin/env python3
# coding=UTF-8
import shlex
import json
from subprocess import Popen, PIPE

def mainCLI():
    cmd = "ceph status -f json"
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)

    stdout_data, stderr_data = p.communicate()

    if p.returncode == 0:
        resJSON = json.loads(stdout_data.decode("UTF-8"))

        print("FSID : {}".format(resJSON["fsid"]))
        print("Status : {}".format(resJSON["health"]["status"]))
    else:
        print("ERROR ({}) : {}".format(p.returncode, stderr_data.decode("UTF-8")))

if __name__ == '__main__':
    mainCLI()

