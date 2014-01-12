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
from optparse import OptionParser, make_option

import logging
import logging.handlers

logger = logging.getLogger('edl_main')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

def printlog(s):
    logger.info(s)
    print(s)

####################3
src_interface = "eth0"
##### override this like 'sudo ./edl_main --interface eth1' (for usb tethering sources it would be usb0)

#TODO - extact the current setting from the current interface and use that automatically - if it's static then use its current ip
############### default is dhcp - to use static provide command-line options like 'sudo ./edl_main --ip 192.168.1.33 --mask 255.255.255.0'
src_interface_ip_mode_dhcp = True
src_interface_ifconfig_ip = ""
src_interface_ifconfig_subnet_mask = ""

option_list = [
		make_option("--interface", action="store",
				type="string", dest="interface"),
		make_option("--ip", action="store",
				type="string", dest="ip"),
		make_option("--mask", action="store",
				type="string", dest="mask"),
		]

parser = OptionParser(option_list=option_list)

(options, args) = parser.parse_args()

if (options.interface is not None):
    printlog("edl: using network interface "+options.interface)
    src_interface = options.interface
else:
    printlog("edl: using default interface eth0 - you can customize like 'sudo ./edl_main --interface eth1' or usb0 or whatever is your internet souce")

if (options.ip is not None):
    src_interface_ifconfig_ip = options.ip
    src_interface_ifconfig_subnet_mask = options.mask
    if (options.mask is None):
        printlog("edl: ip supplied but mask not support - please supply --mask option")
        exit(1)
    printlog("edl: using static ip for bridge: "+options.ip+" subnet_mask: "+options.mask)
    src_interface_ip_mode_dhcp = False
    #TODO - try implementing static ip in the future - for now support only dhcp...
    printlog("edl: static ip is NOT supported yet... you can try directly edit this python source code do to ifconfig instead of dhclient... and dont supply these ip params")
    exit(2)
else:
    printlog("edl: using dhcp")

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

    ret = edl_call("hciconfig -a hci0 class 0x020300", "edl_init")
    if (ret != 0):
        return ret;

    ret = edl_call("hciconfig -a hci0 sspmode 1", "edl_init")
    if (ret != 0):
        printlog("edl: NOTE - The local (USB) Bluetooth device on this computer doesn't support simple-pairing-mode - you'd need to enter 0000 to pair...")

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
            printlog("edl: init adapter failed - either not run as ROOT or a compatible usb bluetooth adapter probably not inserted or turned-on... wait 10 secs and try again...")
            time.sleep(10)
            continue

        printlog ("edl: bluetooth adapter ready")

        ########### prepare new bridge between eth0 (or other interface as specified in option like 'sudo ./edl_main --interface eth1'

        ret = edl_call("sudo ifconfig "+src_interface,"edl_bridge_init");
        if (ret != 0):
            printlog("edl: CRITICAL source interface probably doesn't exist: "+src_interface+" - failed to get initial info of interface...")
            break;

        edl_call("sudo ifconfig "+src_interface+" 0.0.0.0 0.0.0.0","edl_bridge_init");
        edl_call("sudo ifconfig edl_br0 down","edl_bridge_init")
        edl_call("sudo brctl delbr edl_br0","edl_bridge_init")

        ret = edl_call("sudo brctl addbr edl_br0","edl_bridge_init")        
        if (ret != 0):
            printlog("edl: CRITICAL create bridge edl_br0 failed!")
            break;

        ret = edl_call("sudo brctl addif edl_br0 "+src_interface,"edl_bridge_init")        
        if (ret != 0):
            printlog("edl: CRITICAL create bridge edl_br0 failed!")
            break;

        edl_call("sudo ifconfig edl_br0 0.0.0.0 0.0.0.0","edl_bridge_init")

        ret = edl_call("sudo dhclient edl_br0","edl_bridge_init")
        if (ret != 0):
            printlog("edl: CRITICAL set DHCP for newly created bridge failed!")
            break;

        #get path to local module - since edl_nap and edl_agent are in the same folder        
        encoding = sys.getfilesystemencoding()
        this_path = os.path.dirname(unicode(__file__, encoding))

        #start new NAP process - start this before the agent so the sdp profile would be there before users come to pair and discover services...

        printlog('edl: path_to_execute agent and nap: '+this_path)
        nap_process = subprocess.Popen(this_path+'/edl_nap edl_br0', shell=True)

        time.sleep(5)

        #start new auto accept agent
        agent_process = subprocess.Popen(this_path+'/edl_agent', shell=True)
        #printlog ("precheck edl_agent_status: " + str(agent_process.poll()))
        
        watch_agent_and_nap_process(agent_process,nap_process)
        
        printlog("agent or nap has now exit - handle by reset the bt adapter and restart those processes in 5 seconds")
        time.sleep(5)
        #end of while

    #end of main_loop def

