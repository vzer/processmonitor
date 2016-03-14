#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import cms_post
import os
from optparse import OptionParser
import re
import datetime
import subprocess
import socket
try:
    import fcntl
except Exception:
    print "no this model"
import struct
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#shell 命令执行
def shellCmd(cmd):
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (processStdout,processStderr) = process.communicate()
    retcode = process.poll()
    if retcode:
        return (retcode,processStderr)
    return (retcode,processStdout)

#查询进程，返回pid号
def queryProcess(cmd):
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        (status,result)=shellCmd('/usr/java/jdk1.7.0_65/bin/jps -l|grep '+cmd)
        if status==0:
            pid=re.findall('(\d+) %s'%cmd,result)
            print 'status:ok------pid:%s'%''.join(pid)
            return ''.join(pid)
        else:
            if result=='':
                print 'status: not ok------pid:NULL'
                return '0'
            else:
                return "0"
                print'command is error,Messages:%s'%result
                #print (status,result)
    except Exception,msg:
        print('commit is error.')
        print(msg)

#查询端口号
def queryport(port):
    pass

def get_hostname():
        sys = os.name
        if sys == 'nt':
                hostname = os.getenv('computername')
                return hostname

        elif sys == 'posix':
                host = os.popen('echo $HOSTNAME')
                try:
                        hostname = host.read()
                        return hostname
                finally:
                        host.close()
        else:
                return 'Unkwon hostname'

#获取本机ip
def get_ip(ifname):
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

if __name__=="__main__":
    parser=OptionParser()
    parser.add_option("-n","--name",action="store",type="string",dest="programname",help="进程名称：1-后台，2-前台，3-zookeeper")
    (options,args)=parser.parse_args()
    if options.programname:
        QueryCmd=options.programname
    else:
        QueryCmd="1"
    if QueryCmd=="1":
        QueryCmd="com.alibaba.dubbo.container.Main"
        modelname="Service"
    elif QueryCmd=="2":
        QueryCmd="/usr/jetty/start.jar"
        modelname="Web"
    elif QueryCmd=="3":
        QueryCmd="org.apache.zookeeper.server.quorum.QuorumPeerMain"
        modelname="Zookeeper"
    print '--------------------------PID Monitor-----------------------------'
    if QueryCmd=="com.alibaba.dubbo.container.Main":
        metric_name="XiniuServicePid"
    elif QueryCmd=="/usr/jetty/start.jar":
        metric_name="XiniuWebPid"
    elif QueryCmd=="org.apache.zookeeper.server.quorum.QuorumPeerMain":
        metric_name="XiniuZookeeperPid"
    ip=get_ip("eth0")
    hostname=get_hostname()
    pid=queryProcess(QueryCmd)
    cms_post.post(ali_uid="1489610834336193",metric_name=metric_name,metric_value=pid,unit=None,fields="model=%s,hostname=%s,ip=%s"%(modelname,hostname,ip))

