#EcoDroidLink - edl_util - provides bt nap startup, prepares bt dongle, auto pairs, auto accept bt nap connections and periodic checks for running for Bluetooth Network Access Point

__author__ = "Kasidit Yusuf"
__copyright__ = "EcoDroidLink Copyright (c) 2013 Kasidit Yusuf"
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"

#header format from http://stackoverflow.com/questions/1523427/python-what-is-the-common-header-format

import sys
import time
import dbus
from subprocess import call
import subprocess
import os

import logging
import logging.handlers

logger = logging.getLogger('edl_main')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

def printlog(s):
    logger.info(s)
    print(s)

####################

def edl_call(cmd,dbg_header):
    printlog(dbg_header+": Attempt call: "+cmd);
    ret = call(cmd, shell=True)
    printlog(dbg_header+": Call completed: "+cmd+" *RESULT:* "+str(ret))
    return ret

def edl_call_no_log(cmd,dbg_header):
    ret = call(cmd, shell=True)
    return ret

def edl_init_adapter():
    ret = edl_call("hciconfig -a hci0 up", "edl_init")
    if (ret != 0):
        return ret;

    #now use default bt name - which is taken from computer name in /etc/hostname instead
    #ret = edl_call("hciconfig -a hci0 name EcoDroidLink", "edl_init")
    #if (ret != 0):
    #    return ret;

    time.sleep(1);

    ret = edl_call("hciconfig -a hci0 class 0x020300", "edl_init")
    if (ret != 0):
        return ret;

    ret = edl_call("hciconfig -a hci0 sspmode 1", "edl_init")
    if (ret != 0):
        printlog("edl: NOTE - The local (USB) Bluetooth device on this computer doesn't support simple-pairing-mode - you'd need to enter 0000 to pair...")

    ret = edl_call("hciconfig -a hci0 piscan", "edl_init")
    if (ret != 0):
        return ret;

    #set again as some devices the class set above donest seem to work
    ret = edl_call("hciconfig -a hci0 class 0x020300", "edl_init")
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

def main_loop(use_existing_bridge,src_interface):
    # dont enable ip-forwarding since it somehow causes problems with my nexus5 - so comment out this code - edl_call("sudo echo 1 > /proc/sys/net/ipv4/ip_forward","edl") # Theoretically this is 'ip forwarding' might not be required since the bridge works at the lower layer so it should already forwards all ip packets (http://www.linuxjournal.com/article/8172 or http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge - "Since forwarding is done at Layer 2, all protocols can go transparently through a bridge."), and I've tested that the bluetooth-nap works without this ip-forward
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
            printlog("edl: init adapter failed - either not run as ROOT or a compatible usb bluetooth adapter probably not inserted or turned-on... wait 10 secs and try again...")
            time.sleep(10)
            continue

        printlog ("edl: bluetooth adapter ready")

        bridge_to_use = 'edl_br0'

        # if use_existing_bridge was not specified then make our own bridge... ########### prepare new bridge between eth0 (or other interface as specified in option)            
        if use_existing_bridge is None:
            printlog("edl: creating a bridge with DHCP over "+src_interface)
            ret = edl_call("sudo ifconfig "+src_interface,"edl_bridge_init");
            if (ret != 0):
                printlog("edl: CRITICAL source interface probably doesn't exist: "+src_interface+" - failed to get initial info of interface...")
                break;
            edl_call("sudo ifconfig "+src_interface+" 0.0.0.0","edl_bridge_init");
            edl_call("sudo ifconfig edl_br0 down","edl_bridge_init")
            edl_call("sudo brctl delbr edl_br0","edl_bridge_init")
            ret = edl_call("sudo brctl addbr edl_br0","edl_bridge_init")        
            if (ret != 0):
                printlog("edl: CRITICAL create bridge edl_br0 failed!")
                break;
            # this stp makes the internet fail to work entierely in my tests - comment it out - edl_call("sudo brctl stp edl_br0 on ","edl_bridge_init")
            # this forward-delay causes slow down in setting and and dhcp in my tests - comment it out - edl_call("sudo brctl setfd edl_br0 5","edl_bridge_init")
            ret = edl_call("sudo brctl addif edl_br0 "+src_interface,"edl_bridge_init")        
            if (ret != 0):
                printlog("edl: CRITICAL create bridge edl_br0 failed!")
                break;
            edl_call("sudo ifconfig edl_br0 0.0.0.0","edl_bridge_init")
            ret = edl_call("sudo dhclient edl_br0 ","edl_bridge_init")
            if (ret != 0):
                printlog("edl: CRITICAL set DHCP for newly created bridge failed!")
                break;
        else:
            bridge_to_use = use_existing_bridge

        #get path to local module - since edl_nap and edl_agent are in the same folder        
        encoding = sys.getfilesystemencoding()
        this_path = ""
        try:
            this_path = os.path.dirname(unicode(__file__, encoding))
        except Exception as e:
            this_path = os.path.dirname(str(__file__))
            
        #start new NAP process - start this before the agent so the sdp profile would be there before users come to pair and discover services...

        printlog('edl: path_to_execute agent and nap on bridge: '+this_path)
        nap_process = subprocess.Popen(this_path+'/edl_nap '+bridge_to_use, shell=True)

        time.sleep(5)

        #start new auto accept agent
        agent_process = subprocess.Popen(this_path+'/edl_agent', shell=True)
        #printlog ("precheck edl_agent_status: " + str(agent_process.poll()))
        
        watch_agent_and_nap_process(agent_process,nap_process)
        
        printlog("agent or nap has now exit - handle by reset the bt adapter and restart those processes in 5 seconds")
        time.sleep(5)
        #end of while

    #end of main_loop def

