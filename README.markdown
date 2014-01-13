EcoDroidLink BlueZ NAP automation/management software
=====================================================

About
-----

Use (and also freely study, modify and share) this software on GNU/Linux based computers (especially Raspberry Pis) with BlueZ to provide Bluetooth Internet (Network Access Point profile) to compatible Android phones/tablets and also other computers.

This software just simply does the 'automation' part to make sharing LAN/ethernet internet from computers to other devices via Bluetooth simpler. The real Bluetooth Internet engine is BlueZ. It also has a 'BlueZ agent' (edl_agent) to auto-accept Bluetooth pairing and connection requests - useful for a headless Raspberry Pi.

This is essentially the same software managing [EcoDroidLink Bluetooth Access Point for Android](http://www.clearevo.com/ecodroidlink) - please visit to see real usage screenshots on Android, power-consuption test results comparing Bluetooth vs WIFI internet, Android setup instructions and also ready-flashed SD-cards for Raspberry Pis and more.

Note: The new auto bridging features are quite new and experimental - please send bug reports (or patches) to  **`<`ykasidit[AT]gmail.com`>`**

HOWTO Setup and Use
-------------------

- Make sure you have git (to download this software from the development repository), python, python-dbus, python-gobject, bluez, bridge-utils packages installed. Below is an example Ubuntu/Debian/Raspbian command to install all of them:
<pre>sudo apt-get install git-core python-dbus python-gobject bluez bridge-utils</pre> 

- Download and install the latest release version:
<pre>git clone https://github.com/ykasidit/ecodroidlink.git</pre>

- After it completes, a folder named 'ecodroidlink' would be created, you can cd into it. (After this, you can 'git pull origin master' to check and get new updates...).

- If you're using a Raspberry Pi or Desktop computer, please get a compatible CSR-Based USB Bluetooth dongle (preferably Bluetooth CSR 4.0 Dongles - it had better results than older dongles we tested). If you're using a Notebook with internal Bluetooth, make sure it is turned-on and working on your GNU/Linux (Ubuntu, Debian, etc.) computer.

- Make sure you have a working ethernet/LAN internet source connected to your computer (with DHCP enabled in the router - default for most setups).

Let's test it
-------------

Ok, let's test it first: let's start the EcoDroidLink main manager - edl_main - it would make a new "bridge" and put your eth0 (ethernet) connection in it, reset DHCP on it - ready to share to new Bluetooth connections - to do all of this and more, it requires root access so a 'sudo' is required. Enter the following command: 
<pre>sudo ./edl_main</pre>

(Note: If your internet-source is not the default 'eth0' - you can specify it via the '--interface' option. So if your internet source is usb0, use a command like: sudo ./edl_main --interface usb0)

Then, it would proceed - once it shows "edl: Bluetooth Network Access Point Server (for nap) registered for bridge edl_br0" - this means it's done! Now you can proceed to connect from your Android device or other computers which have Bluetooth.

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

If all goes well, now let's connect from your android phone/tablet - for instructions and screenshots on how to setup Android phones/tablets to use your new Bluetooth Internet source - please see the "Android Bluetooth Internet Setup" topic of the [Official EcoDroidLink Page](http://www.clearevo.com/ecodroidlink) - there are also intructions/screenchots to setup and use Bluetooth Internet on Windows 7, Windows XP and Ubuntu computers in the "Computer Bluetooth interent Setup" section in that same page.

If you've got internet working from your android, let's install it for autostart in the next section below.

Make EcoDroidLink autostart-on-boot
----------------------------------

Simply run:
<pre>sudo ./install_autostart</pre>

If it shows "Successfully setup auto-start-on-boot for edl_main" then you're done - reboot your pi and test it! For example run:
<pre>sudo shutdown -r now</pre>

NOTE: The default/generated autostart script would not contain any custom parameters. Therefore, if you want to specify --interface or the recommended --use_existing_bridge part as in next section, so please edit and add your desired parameters in the file /etc/init.d/ecodroidlink (sudo nano /etc/init.d/ecodroidlink) - the line which calls edl_main in the line under "start)" - make sure the trailing & is still there.

Recommended: Manually create your own bridge for best connection reliability
--------------------------------------------

By default, the edl_main would automatically create a bridge over eth0 as already descibed above. However, this is done only once on startup, problems could arise if the ethernet cable gets temporarily disconnected and so forth - the edl_main auto-bridging doesn't check and re-bridge in such cases yet - the auto-bridging is intended for easy testing purposes but not permanet use.

It is advisable to create and use your own 'bridge' (in /etc/network/interfaces) because you can fully customize the bridge as you like (static ip for your Computer/Pi, etc). So, just create a bridge (like 'br0') containing your desired interface (like 'eth0') in this file: sudo nano /etc/network/interfaces - let's first remove the 'auto eth0' line

For example, make it: 
auto lo
iface lo inet loopback

auto br0
iface br0 inet dhcp
  bridge_ports eth0

For more detailed info, please see <http://www.hkepc.com/forum/viewthread.php?tid=1710030> - the part about "The modified /etc/network/interfaces file".

- For static ip examples please see <https://wiki.debian.org/NetworkConfiguration#Bridging> - for most computers which have eth0 only - make sure you remove the eth1 from the bridge_ports. 

- Make sure you removed do not have a line to setup dhcp for your interface (eth0) otherwise it could cause strange behavior - only set ip/dhcp for the bridge as explained in <http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge#Creating_a_bridge_device>.

- Restart your computer (sudo shutdown -r now), make sure internet works, then specify the bridge's name (like 'br0') - for example:
sudo ./edl_main --use_existing_bridge br0

License
-------

EcoDroidLink is free-software, licensed under GNU GPL, same as BlueZ. Please see the COPYING file in this same folder for full info.

Special Thanks
-------------

- Thanks to the user 'howdy' in <http://www.hkepc.com/forum/viewthread.php?tid=1710030> for posting a detailed tutorial for setting nap on bluez.

- Thanks to [BlueZ](http://www.bluez.org)

- Thanks to Raspberry Pi forum users: Basil_R, Douglas6, maxwed, and all others providing great input/suggestions in <http://www.raspberrypi.org/phpBB3/viewtopic.php?f=36&t=57529>.