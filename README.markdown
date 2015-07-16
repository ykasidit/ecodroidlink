EcoDroidLink BlueZ NAP automation/management software
=====================================================

*IMPORTANT: This branch is designed for advanced users. For Archlinux-ARM. If you're using Raspbian or Ubuntu - please use the master branch instead. The default behaviour in this branch requires a pre-configured bridge - not auto-bridge creation as in master branch.*

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

(I'm trying to make this easy for beginners of GNU/Linux and Raspberry Pi to follow - my apology to advanced readers if you find that there's too much explanation on the obvious basic commands.)

Note: To change the Bluetooth display name of your new Pi Bluetooth Access Point - please edit the /etc/hostname file - the default would be 'raspberrypi-0'.

Ok, let's test it first: let's start the EcoDroidLink main manager - edl_main --auto_mode - it would make a new "bridge" and put your eth0 (ethernet) connection in it, reset DHCP on it - ready to share to new Bluetooth connections - to do all of this and more, it requires root access so a 'sudo' is required. Enter the following command: 
<pre>cd ecodroidlink</pre>
<pre>sudo ./edl_main --auto_mode</pre>

(Note: If your internet-source is not the default 'eth0' - you can specify it via the '--interface' option. So if your internet source is usb0, use a command like: sudo ./edl_main --auto_mode --interface usb0)

Then, it would proceed - once it shows "edl: Bluetooth Network Access Point Server (for nap) registered for bridge edl_br0" - this means it's done! Now you can proceed to connect from your Android device or other computers which have Bluetooth.

- Below is an example output of installing and running EcoDroidLink Raspbian Wheezy:

<pre>
pi@raspberrypi:~$ git clone https://github.com/ykasidit/ecodroidlink.git
Cloning into 'ecodroidlink'...
remote: Reusing existing pack: 69, done.
remote: Total 69 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (69/69), done.
pi@raspberrypi:~$ cd ecodroidlink/
pi@raspberrypi:~/ecodroidlink$ ls
bluezutils.py  edl_main  edl_stop     install_autostart  singleton.py
edl_agent      edl_nap   edl_util.py  README.markdown    TODO
pi@raspberrypi:~/ecodroidlink$ sudo ./edl_main --auto_mode
edl: auto-create bridge (dhcp) over default interface eth0 - you can customize like 'sudo ./edl_main --interface eth1' or usb0 or whatever is your internet souce. NOTE: It is recommended to create your own bridge in /etc/network/interfaces and specify like 'sudo ./edl_main --use_existing_bridge br0' for real deployment in auto-start-on-boot mode. Please see README.markdown for full info.
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
edl: creating a bridge with DHCP over eth0
edl_bridge_init: Attempt call: sudo ifconfig eth0
eth0      Link encap:Ethernet  HWaddr b8:27:eb:38:76:19  
          inet addr:192.168.1.42  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:14014 errors:0 dropped:0 overruns:0 frame:0
          TX packets:5985 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:9946459 (9.4 MiB)  TX bytes:490751 (479.2 KiB)

edl_bridge_init: Call completed: sudo ifconfig eth0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig eth0 0.0.0.0
edl_bridge_init: Call completed: sudo ifconfig eth0 0.0.0.0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig edl_br0 down
edl_br0: ERROR while getting interface flags: No such device
edl_bridge_init: Call completed: sudo ifconfig edl_br0 down *RESULT:* 255
edl_bridge_init: Attempt call: sudo brctl delbr edl_br0
bridge edl_br0 doesn't exist; can't delete it
edl_bridge_init: Call completed: sudo brctl delbr edl_br0 *RESULT:* 1
edl_bridge_init: Attempt call: sudo brctl addbr edl_br0
edl_bridge_init: Call completed: sudo brctl addbr edl_br0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo brctl addif edl_br0 eth0
edl_bridge_init: Call completed: sudo brctl addif edl_br0 eth0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo ifconfig edl_br0 0.0.0.0
edl_bridge_init: Call completed: sudo ifconfig edl_br0 0.0.0.0 *RESULT:* 0
edl_bridge_init: Attempt call: sudo dhclient edl_br0 
mv: cannot stat `/etc/samba/dhcp.conf.new': No such file or directory
edl_bridge_init: Call completed: sudo dhclient edl_br0  *RESULT:* 0
edl: path_to_execute agent and nap on bridge: /home/pi/ecodroidlink
edl: Bluetooth Network Access Point Server (for nap) registered for bridge edl_br0
edl: agent starting
edl: this is probably an older bluez version - trying old compat code...
edl: auto-pair/accept agent registered with older bluez method
</pre>

If all goes well, now let's connect from your Android phone/tablet, or your PC or other Raspberry Pis:

  - **Using Bluetooth Internet on Android**: Please see the screenshots and steps at the section [Android Bluetooth Internet Setup](http://www.clearevo.com/ecodroidlink/#setup_android) in the official EcoDroidLink page. Note: Bluetooth internet from Android Kitkat (4.4) devices are not so stable at the moment - probably because of the new/young Bluedroid stack.

  - **Using Bluetooth Internet from other Raspberry Pis**: Please see the simple steps at the section [Raspberry Pi Bluetooth Internet Setup](http://www.clearevo.com/ecodroidlink/#setup_raspberry_pi) in the official EcoDroidLink page.

  - **Using Bluetooth Internet from Computers/Laptops**: Please see the screenshots and steps for your OS (Windows 7, Windows XP or Ubuntu) at the section [Computer Bluetooth Internet Setup](http://www.clearevo.com/ecodroidlink/#setup_computer) in the official EcoDroidLink page.


If you've got internet working from your Android or Raspberry Pi or Computer as desired, let's install it for autostart in the next section below.

Make EcoDroidLink autostart-on-boot
----------------------------------

Simply run:
<pre>sudo ./install_autostart</pre>

If it shows "Successfully setup auto-start-on-boot for edl_main" then you're done - reboot your pi and test it! For example run:
<pre>sudo shutdown -r now</pre>

NOTE: The default/generated autostart script would not contain any custom parameters. Therefore, if you want to specify --interface or the recommended --use_existing_bridge part as in next section, so please edit and add your desired parameters in the file /etc/init.d/ecodroidlink (sudo nano /etc/init.d/ecodroidlink) - the line which calls edl_main in the line under "start)" - make sure the trailing & is still there.

NOTE:
- To test if your edit has correct syntax and works correctly, you can do the below to stop and start the installed ecodroidlink service:
<pre>sudo service ecodroidlink stop</pre>
- Then:
<pre>sudo service ecodroidlink start</pre>
After the start, you'd see the normal output but since there was a trailing '&', it would not block. Just press 'enter' to get back to your shell prompt or stop the service to end it.


Recommended: Manually create your own bridge for best connection reliability
--------------------------------------------

By default, the edl_main would automatically create a bridge over eth0 as already descibed above. However, this is done only once on startup, problems could arise if the ethernet cable gets temporarily disconnected and so forth - the edl_main auto-bridging doesn't check and re-bridge in such cases yet - the auto-bridging is intended for easy testing purposes but might not be suitable for long-term use.

It is advisable to create and use your own 'bridge' (in /etc/network/interfaces) because you can fully customize the bridge as you like (static ip for your Computer/Pi, etc).

Then, we'd use the option '--use_existing_bridge' to specify the bridge you've created.

- Please create a bridge (like 'br0') containing your desired interface (like 'eth0'). This is done by editing /etc/network/interfaces file - please make a copy/backup of the original file if you're unsure. For more detailed info, please see <http://www.hkepc.com/forum/viewthread.php?tid=1710030> - the part about "The modified /etc/network/interfaces file".

- Make sure you remove the dhcp setup line for your interface (which looks like 'iface eth0 inet dhcp') otherwise it could cause strange behavior - only set ip/dhcp for the bridge as explained in <http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge#Creating_a_bridge_device>.

- For example, you might make it look something like: 

<pre>
auto lo
iface lo inet loopback

auto br0
iface br0 inet dhcp
      bridge_ports eth0
</pre>

- If you want static ip instead of dhcp - please see <https://wiki.debian.org/NetworkConfiguration#Bridging> - for most computers which have eth0 only - make sure you remove the eth1 from the bridge_ports. 

- Restart your computer (sudo shutdown -r now), make sure internet works, for example try: <pre>ping www.google.com</pre>

- Finally, use --use_existing_bridge to specify the bridge's name (like 'br0') to edl_main - for example:
<pre>sudo ./edl_main --use_existing_bridge br0</pre>

- If you're using the auto-start-on-boot feature. Remember to edit the startup-script:  <pre>sudo nano /etc/init.d/ecodroidlink</pre> to make the edl_main line look like 'edl_main --use_existing_bridge br0 &' too.

License
-------

EcoDroidLink is free-software, licensed under GNU GPL, same as BlueZ. Please see the COPYING file in this same folder for full info.

Special Thanks
-------------

- Thanks to the user 'howdy' in <http://www.hkepc.com/forum/viewthread.php?tid=1710030> for posting a detailed tutorial for setting nap on bluez.

- Thanks to [BlueZ](http://www.bluez.org)

- Thanks to Raspberry Pi forum users: Basil_R, Douglas6, maxwed, and all others providing great input/suggestions in <http://www.raspberrypi.org/phpBB3/viewtopic.php?f=36&t=57529>.