EcoDroidLink BlueZ NAP automation/management software
=====================================================

About
-----

Use (and also freely study, modify and share) this software on GNU/Linux based computers (especially Raspberry Pis) with BlueZ to provide Bluetooth Internet (Network Access Point profile) to compatible Android phones/tablets and also other computers.

This software just simply does the 'automation' part to make sharing LAN/ethernet internet from computers to other devices via Bluetooth simpler. The real Bluetooth Internet engine is BlueZ.

This is essentially the same software managing [EcoDroidLink Bluetooth Access Point for Android](http://www.clearevo.com/ecodroidlink) - please visit to see real usage screenshots on Android, power-consuption test results comparing Bluetooth vs WIFI internet, Android setup instructions and also ready-flashed SD-cards for Raspberry Pis and more.

Note: The new auto bridging features are quite new and experimental - please send bug reports (or patches) to  **`<`ykasidit[AT]gmail.com`>`**

HOWTO Setup and Use
-------------------

- Make sure you have git (to download this software from the development repository), python, python-dbus, python-gobject, bluez, bridge-utils packages installed. Below is an example Ubuntu/Debian/Raspbian command to install all of them:
<pre>sudo apt-get install git-core python-dbus python-gobject bluez bridge-utils</pre> 

- Download and install the latest release version:
<pre>git clone https://github.com/ykasidit/ecodroidlink.git</pre>

- After it completes, a folder named 'ecodroidlink' would be created, you can cd into it. (After this, you can 'git pull' to check and get new updates...).

- If you're using a Raspberry Pi or Desktop computer, please get a compatible CSR-Based USB Bluetooth dongle (preferably Bluetooth CSR 4.0 Dongles - it had better results than older dongles we tested). If you're using a Notebook with internal Bluetooth, make sure it is turned-on and working on your GNU/Linux (Ubuntu, Debian, etc.) computer.

- Make sure you have a working ethernet/LAN internet source connected to your computer (with DHCP enabled in the router - default for most setups).

- Ok, let's start the EcoDroidLink main manager - edl_main - it would make a new "bridge" and put your eth0 (ethernet) connection in it, reset DHCP on it - ready to share to new Bluetooth connections - to do all of this and more, it requires root access so a 'sudo' is required. Enter the following command: 
<pre>sudo ./edl_main</pre>

(Note: If your internet-source is not the default 'eth0' - you can specify it via the '--interface' option. So if your internet source is usb0, use a command like: sudo ./edl_main --interface usb0)

Then, it would proceed - once it shows "edl: Bluetooth Network Access Point Server (for nap) registered for bridge edl_br0" - this means it's done! Now you can proceed to connect from your Android device or other computers which have Bluetooth.

- For instructions and screenshots on how to setup Android phones/tablets to use your Bluetooth Internet - please see the "Android Setup" part of the [Official EcoDroidLink Page](http://www.clearevo.com/ecodroidlink).

- Below is an example output EcoDroidLink running on Ubuntu 12.04:

(I'm using usb0 here since I don't have LAN internet right now, so using 'USB Tethering' from my phone as the internet source... if your're using the normal eth0 ethernet/LAN then don't specify "--interface usb0"! Just use "sudo ./edl_main")

<pre>kasidit@kasidit-computer:~/ecodroidlink$ sudo ./edl_main --interface usb0
edl: using network interface usb0
edl: using dhcp
edl: EcoDroidLink initialzing/cleaning processes and adapter state...
edl_deinit: Attempt call: killall edl_agent
edl_agent: no process found
edl_deinit: Call completed: killall edl_agent *RESULT:* 1
edl_deinit: Attempt call: killall edl_nap
edl_nap: no process found
edl_deinit: Call completed: killall edl_nap *RESULT:* 1
edl_deinit: Attempt call: hciconfig -a hci0 down
edl_deinit: Call completed: hciconfig -a hci0 down *RESULT:* 0
edl: preparing bluetooth adapter..
edl_init: Attempt call: hciconfig -a hci0 up
edl_init: Call completed: hciconfig -a hci0 up *RESULT:* 0
edl_init: Attempt call: hciconfig -a hci0 class 0x020300
edl_init: Call completed: hciconfig -a hci0 class 0x020300 *RESULT:* 0
edl_init: Attempt call: hciconfig -a hci0 sspmode 1
edl_init: Call completed: hciconfig -a hci0 sspmode 1 *RESULT:* 0
edl_init: Attempt call: hciconfig -a hci0 piscan
edl_init: Call completed: hciconfig -a hci0 piscan *RESULT:* 0
edl: bluetooth adapter ready
edl_bridge_init: Attempt call: sudo ifconfig usb0
usb0      Link encap:Ethernet  HWaddr ea:9b:d4:36:11:47  
          inet6 addr: fe80::e89b:d4ff:fe36:1147/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1949 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1692 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:2135942 (2.1 MB)  TX bytes:270351 (270.3 KB)

edl_bridge_init: Call completed: sudo ifconfig usb0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig usb0 0.0.0.0 0.0.0.0
edl_bridge_init: Call completed: sudo ifconfig usb0 0.0.0.0 0.0.0.0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig edl_br0 down
edl_bridge_init: Call completed: sudo ifconfig edl_br0 down *RESULT:* 0
edl_bridge_init: Attempt call: sudo brctl delbr edl_br0
edl_bridge_init: Call completed: sudo brctl delbr edl_br0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo brctl addbr edl_br0
edl_bridge_init: Call completed: sudo brctl addbr edl_br0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo brctl addif edl_br0 usb0
edl_bridge_init: Call completed: sudo brctl addif edl_br0 usb0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig edl_br0 0.0.0.0 0.0.0.0
edl_bridge_init: Call completed: sudo ifconfig edl_br0 0.0.0.0 0.0.0.0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo dhclient edl_br0
edl_bridge_init: Call completed: sudo dhclient edl_br0 *RESULT:* 0
edl: Bluetooth Network Access Point Server (for nap) registered for bridge edl_br0
edl: agent starting
edl: this is probably an older bluez version - trying old compat code...
edl: auto-pair/accept agent registered with older bluez method
</pre>