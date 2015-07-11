#EcoDroidLink - edl_util - provides bt nap startup, prepares bt dongle, auto pairs, auto accept bt nap connections and periodic checks for running for Bluetooth Network Access Point

__author__ = "Kasidit Yusuf"
__copyright__ = "EcoDroidLink Copyright (c) 2013 Kasidit Yusuf"
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0.3"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"

#header format from http://stackoverflow.com/questions/1523427/python-what-is-the-common-header-format

import sys
import time
import dbus
from subprocess import call
import subprocess

import logging
import logging.handlers

logger = logging.getLogger('edl_main')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

def printlog(s):
    logger.info(s)
    print(s)

def edl_call(cmd,dbg_header):
    ret = call(cmd, shell=True)
    printlog(dbg_header+": "+cmd+" *RESULT:* "+str(ret))
    return ret

def edl_call_no_log(cmd,dbg_header):
    ret = call(cmd, shell=True)
    return ret

def edl_init_adapter():
    ret = edl_call("hciconfig -a hci0 up", "edl_init")
    if (ret != 0):
        return ret;

    #now set computer name in /etc/hostname instead
    #ret = edl_call("hciconfig -a hci0 name EcoDroidLink", "edl_init")
    #if (ret != 0):
    #    return ret;

    ret = edl_call("hciconfig -a hci0 class 0x020300", "edl_init")
    if (ret != 0):
        return ret;

    ret = edl_call("hciconfig -a hci0 sspmode 1", "edl_init")
    if (ret != 0):
        return ret;

    ret = edl_call("hciconfig -a hci0 piscan", "edl_init")
    if (ret != 0):
        return ret;

    return 0;

def edl_deinit():
    ret = edl_call("killall edl_agent", "edl_deinit")

    ret = edl_call("killall edl_nap", "edl_deinit")    
    
    #ret = edl_call("netctl stop edl_bridge", "edl_deinit")
    
    ret = edl_call("hciconfig -a hci0 down", "edl_deinit")

    
def watch_agent_and_nap_process(agent_process,nap_process):
        while (1):
            #check agent_process - make sure it's running
            agent_process_status = agent_process.poll()
            #printlog ("check edl_agent_status: " + str(agent_process_status))
            if (agent_process_status is not None): #means it has exit
                printlog("edl_agent_status: process exit! break from observer loop now and restart into main process")
                return -1

            #check nap process - make sure it's running
            nap_process_status = nap_process.poll()
            #printlog ("check edl_nap_status: " + str(nap_process_status))
            if (nap_process_status is not None): #means it has exit
                printlog("edl_nap_status: process exit! break from observer loop now and restart into main process")
                return -2
            
            time.sleep(5);
            #end of while loop

        printlog("CONTROL SHOULD NEVER REACH HERE!")
        return -3
        #end of watcher def

def main_loop():
    while (1):
        printlog ("edl: EcoDroidLink initialzing/cleaning processes and adapter state...")
        edl_deinit()

        #printlog ("edl: preparing eth0 bridge")
        #if (0 != edl_init_eth0_bridge()):
        #    printlog("edl: init eth0 bridge failed - ethernet not plugged-in/ready... wait 10 secs and try again...")
        #    time.sleep(10)
        #    continue

        printlog ("edl: preparing bluetooth adapter..")
        
        if (0 != edl_init_adapter()):
            printlog("edl: init adapter failed - compatible usb bluetooth adapter probably not inserted... wait 10 secs and try again...")
            time.sleep(10)
            continue

        printlog ("edl: bluetooth adapter ready")
       
        #start new auto accept agent
        agent_process = subprocess.Popen('/home/ecodroidlink/edl_agent', shell=True)
        #printlog ("precheck edl_agent_status: " + str(agent_process.poll()))
            

        time.sleep(5)

        #start new NAP process
        nap_process = subprocess.Popen('/home/ecodroidlink/edl_nap br0', shell=True)
        
        watch_agent_and_nap_process(agent_process,nap_process)
        
        printlog("agent or nap has now exit - handle by reset the bt adapter and restart those processes in 5 seconds")
        time.sleep(5)
        #end of while

    #end of main_loop def

