import os
from os import sys
import socket
import platform
from uptime import uptime
import subprocess

ostype = sys.platform[:3]
if ostype == 'win':
    import psutil

def pack(key, args):
    if isinstance(args, str):
            message = "{%s: '%s'}" % (key, args)
    else:
        message = "{%s: %s}" % (key, args)
    return str.encode(message)

def getMachineName():
    return socket.gethostname()

def getCurrentUsername():
    return os.environ.get('USERNAME')

def getOperatingSystemVersion():
    return platform.platform()

def getUptime():
    return uptime()

def getCPUUsage():
    if ostype == 'win':
        return psutil.cpu_percent()
    else:
        usage = subprocess.check_output('free | grep Mem | awk \'{print $3/$2 * 100.0}\'', shell=True, encoding='utf-8')
        usage = usage.rstrip('\n')
        return str(usage)

def getMemoryUsage():
    if ostype == 'win':
        memory =str(psutil.virtual_memory())
        memory = memory.split(',')[2]
        memory = memory.lstrip(' percent=')
        return memory
    else:
        memory = subprocess.check_output('grep \'cpu \' /proc/stat | awk \'{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}\'', shell=True, encoding='utf-8')
        memory = memory.rstrip("%\n")
        return memory

def getLocalIP():
    return socket.gethostbyname(socket.gethostname())

def getCurrentWindowTitle():
    if ostype == 'lin':
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]
    elif ostype == 'win':
        import win32gui
        w = win32gui
        return w.GetWindowText(w.GetForegroundWindow())