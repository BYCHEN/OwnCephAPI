#!/usr/bin/env python3
# coding=UTF-8
import rados
import json

def mainLIB():
    cmd = {"prefix": "status", "format": "json"}

    cluster = rados.Rados(conffile = "/etc/ceph/ceph.conf", conf = dict (keyring = "/etc/ceph/ceph.client.admin.keyring"))
    cluster.connect()

    stat, res, err = cluster.mon_command(json.dumps(cmd), "")

    if stat == 0:
        resJSON = json.loads(res.decode("UTF-8"))
        
        print("FSID : {}".format(resJSON["fsid"]))
        print("Status : {}".format(resJSON["health"]["status"]))
    else:
        print("ERROR ({}) : {}".format(stat, err))


if __name__ == '__main__':
    mainLIB()