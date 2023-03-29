#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import netifaces
except ImportError:
    netifaces = None
import os
import platform
from subprocess import Popen, PIPE
import sys
import time
import psutil
import plugins
try:
    import distro
except ImportError:
    distro = None

def systemCommand(Command, newlines=True):
    Output = ""
    Error = ""
    try:
        proc = Popen(Command.split(), stdout=PIPE)
        Output = proc.communicate()[0]
    except Exception:
        pass

    if Output:
        if newlines is True:
            Stdout = Output.split("\n")
        else:
            Stdout = Output
    else:
        Stdout = []
    if Error:
        Stderr = Error.split("\n")
    else:
        Stderr = []

    return (Stdout, Stderr)


def ip_addresses():
    ip_list = {}
    ip_list['v4'] = {}
    ip_list['v6'] = {}
    if netifaces is None:
        return ip_list
    for interface in netifaces.interfaces():
        link = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in link:
            if interface not in ip_list['v4']:
                ip_list['v4'][interface] = []
            ip_list['v4'][interface].append(link[netifaces.AF_INET])
        if netifaces.AF_INET6 in link:
            if interface not in ip_list['v6']:
                ip_list['v6'][interface] = []
            ip_list['v6'][interface].append(link[netifaces.AF_INET6])
    return ip_list


class Plugin(plugins.BasePlugin):
    __name__ = 'system'

    def run(self, *unused):
        systeminfo = {}
        cpu = {}
        cpu['brand'] = "Unknown CPU"
        cpu['count'] = 0
        if(os.path.isfile("/proc/cpuinfo")):
            f = open('/proc/cpuinfo')
            if f:
                for line in f:
                    # Ignore the blank line separating the information between
                    # details about two processing units
                    if line.strip():
                        if "model name" == line.rstrip('\n').split(':')[0].strip():
                            cpu['brand'] = line.rstrip('\n').split(':')[1].strip()
                        if "Processor" == line.rstrip('\n').split(':')[0].strip():
                            cpu['brand'] = line.rstrip('\n').split(':')[1].strip()
                        if "processor" == line.rstrip('\n').split(':')[0].strip():
                            cpu['count'] = line.rstrip('\n').split(':')[1].strip()
        if cpu['brand'] == "Unknown CPU":
            f = os.popen('lscpu').read().split('\n')
            if f:
                for line in f:
                    # Ignore the blank line separating the information between
                    # details about two processing units
                    if line.strip():
                        if "Model name" == line.rstrip('\n').split(':')[0].strip():
                            cpu['brand'] = line.rstrip('\n').split(':')[1].strip()
                        if "Processor" == line.rstrip('\n').split(':')[0].strip():
                            cpu['brand'] = line.rstrip('\n').split(':')[1].strip()
                        if "CPU(s)" == line.rstrip('\n').split(':')[0].strip():
                            cpu['count'] = line.rstrip('\n').split(':')[1].strip()
        mem = psutil.virtual_memory()
        if sys.platform == "linux" or sys.platform == "linux2":
            if distro is None:
                systeminfo['os'] = str(' '.join(platform.linux_distribution()))
            else:
                systeminfo['os'] = str(' '.join(distro.linux_distribution(full_distribution_name=True)))
        elif sys.platform == "darwin":
            systeminfo['os'] = "Mac OS %s" % platform.mac_ver()[0]
            cpu['brand'] = str(systemCommand('sysctl machdep.cpu.brand_string', False)[0]).split(': ')[1]
            #cpu['count'] = systemCommand('sysctl hw.ncpu')
        elif sys.platform == "freebsd10" or sys.platform == "freebsd11":
            systeminfo['os'] = "FreeBSD %s" % platform.release()
            cpu['brand'] = str(systemCommand('sysctl hw.model', False)[0]).split(': ')[1]
            cpu['count'] = systemCommand('sysctl hw.ncpu')
        elif sys.platform == "win32":
            systeminfo['os'] = "{} {}".format(platform.uname()[0], platform.uname()[2])
        systeminfo['cpu'] = cpu['brand']
        systeminfo['cores'] = cpu['count']
        systeminfo['memory'] = mem.total
        systeminfo['psutil'] = '.'.join(map(str, psutil.version_info))
        systeminfo['python_version'] = sys.version
        systeminfo['platform'] = platform.platform()
        systeminfo['uptime'] = int(time.time()-psutil.boot_time())
        systeminfo['ip_addresses'] = ip_addresses()
        systeminfo['hostname'] = platform.node()

        return systeminfo


if __name__ == '__main__':
    Plugin().execute()
