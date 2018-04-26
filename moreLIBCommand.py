#!/usr/bin/env python3
# coding=UTF-8
"""
Ceph Command的集合，要來給rados.mon_command 使用
reference by : https://github.com/ceph/ceph/tree/master/src/mon

"""

def poolList():
    """ List all ceph osd pool names."""
    return {"prefix": "osd pool ls", "format": "json"}

def poolGetQuota(PoolId):
    """ Get maximum storage size of the specific pool. """
    return {"prefix": "osd pool get-quota", "pool": PoolId, "format": "json"}

def poolSetQuota(PoolId, size_bytes):
    """ Set maximum storage size of the specific pool. """
    return {"prefix": "osd pool set-quota", "field": "max_bytes", "val": str(size_bytes), "pool": PoolId}

def poolGetReplicated(PoolId):
    """ Get size of repicating the specific pool. """
    return {"prefix": "osd pool get", "pool": PoolId, "var": "size", "format": "json"}

def poolSetReplicated(PoolId, size):
    """ Set size of repicating the specific pool. """
    return {"prefix": "osd pool set", "pool": PoolId, "var": "size", "val": size}

def poolSetECOverwrite(PoolId, sw):
    """ Whether enable overwrites on the specific pool. 
    reference by : https://ceph.com/community/new-luminous-erasure-coding-rbd-cephfs/
    """
    return {"prefix": "osd pool set", "pool": PoolId, "var": "allow_ec_overwrites", "val": sw}

def poolGetECProfile(PoolId):
    """ Whether enable overwrites on the specific pool. 
    reference by : https://ceph.com/community/new-luminous-erasure-coding-rbd-cephfs/
    """
    return {"prefix": "osd pool get", "pool": PoolId, "var": "erasure_code_profile", "format": "json"}    

def poolDelete(PoolId):
    """ Delete pool should set mon_allow_pool_delete config option to true. """
    return {"prefix": "osd pool rm", "pool": PoolId, "pool2": PoolId, "sure": "--yes-i-really-really-mean-it"}

def poolCreate(PoolId, PG_NUM, PGP_NUM, ProtectType):
    """ Create pool based on pg_num, pgp_num, and pool_type. 
    
    In deault, pg_num = pgp_num, pool_type = replicated. """
    return {"prefix": "osd pool create", "pool": PoolId, "pg_num": PG_NUM, "pgp_num": PGP_NUM, "pool_type": ProtectType}

def cephPGStat():
    """ Get ceph PG state. 
    
    In deault, to check whether num_pgs exceed maximum pg num per osd. """
    return {"prefix": "pg stat", "format": "json"}

def cephEnableApp(PoolId, App):
    """ Create RBD pool shoud enable use of RBD application on specific pool.

    Here shows the general command for enabling use of cephfs/rbd/rbd/rgw application.
    
    The original command is::

        ceph osd pool application enable {poolname} {app-name}

    """
    return {"prefix": "osd pool application enable", "pool": PoolId, "app": App}

def cephDF():
    """ List all ceph used pools info. It shows maximum available and used storage size. """
    return {"prefix": "df", "format": "json"}

def fsRemovePool(FSName, PoolId):
    """ 刪除該 Pool 中 Filesystem service 的 data. """
    return {"prefix": "fs rm_data_pool", "fs_name": FSName, "pool": PoolId}

def fsAddPool(FSName, PoolId):
    """ 將 Filesystem service 的 data 加到該 Pool 中. """
    return {"prefix": "fs add_data_pool", "fs_name": FSName, "pool": PoolId}

def monDump():
    """ List monitor map of cluster. """
    return {"prefix": "mon dump", "format": "json"}

# Capacity's String Array should by ODD.
def clusterStatus():
    """ 取得 cluster現在的健康狀態與細節資訊 """
    return {"prefix": "status", "format": "json"}

def authCreate(CephUserId, PoolId):
    """ 創建 PoolId 的 client Keyring"""
    client = "client.{}".format(CephUserId)
    osdCaps = "allow rw pool={}".format(PoolId)
    return {"prefix": "auth get-or-create-key","entity": client, "caps": ["mon", "allow r", "osd", osdCaps], "format": "json"}

def authCreateForRBDPool(CephUserId, PoolId):
    """ 創建 PoolId 的 client Keyring"""
    client = "client.{}".format(CephUserId)
    osdCaps = "profile rbd pool={}".format(PoolId)
    return {"prefix": "auth get-or-create-key","entity": client, "caps": ["mon", "profile rbd", "osd", osdCaps], "format": "json"}

def authCreateForRBDECPool(CephUserId, PoolId, MDPoolId):
    """ 創建 ECRBDImg 的 client Keyring"""
    client = "client.{}".format(CephUserId)
    osdCaps = "profile rbd pool={}, profile rbd pool={}".format(PoolId, MDPoolId)
    return {"prefix": "auth get-or-create-key","entity": client, "caps": ["mon", "profile rbd", "osd", osdCaps], "format": "json"}

def authCreateForFSPool(CephUserId, FSPoolId, FSGroupPath):
    """ 創建 FSPoolId 的 client Keyring"""
    client = "client.{}".format(CephUserId)
    osdCaps = "allow rw pool={}".format(FSPoolId)
    mdsCaps = "allow r, allow rw path={}".format(FSGroupPath)
    return {"prefix": "auth get-or-create-key","entity": client, "caps": ["mon", "allow r", "osd", osdCaps, "mds", mdsCaps], "format": "json"}

def authCreateForFSSvc(CephUserId, FSSvcId, FSSvcPath):
    """ 創建 FSSvcId 的 client Keyring"""
    client = "client.{}".format(CephUserId)
    osdCaps = "allow rw pool={}".format(FSSvcId)
    mdsCaps = "allow r, allow rw path={}".format(FSSvcPath)
    return {"prefix": "auth get-or-create-key","entity": client, "caps": ["mon", "allow r", "osd", osdCaps, "mds", mdsCaps], "format": "json"}

def authDelete(CephUserId):
    """ 刪除 client Keyring"""
    client = "client.{}".format(CephUserId)
    return {"prefix": "auth del", "entity": client, "format": "json"}

def authIsExist(CephUserId):
    """ 判斷是否存在此 client Keyring"""
    client = "client.{}".format(CephUserId)
    return {"prefix": "auth print-key", "entity": client, "format": "json"}

