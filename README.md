# Who is home ?
<img src="https://www.ut.ee/sites/default/files/logod/04.%20Arvutiteaduse%20instituut/arvutiteaduse%20instituut_eng_sinine.png" width=300px></img><img src="https://media.voog.com/0000/0034/3577/photos/IT%20Akadeemia%20logo%20RGB%201000%20px.png" width=300></img>

This code was developed for Computer Programming course at Tartu University.

Upon completion of this application we decided to add it to the "IT Student Project Contest" organized by Tartu University.

It is intended to be installed on a device (running linux) that is connected to home or office network. Preferably raspberry pi that is connected to audio system and runs 24/7. Initially we intended it to be CLI only but later decided to add simple GUI also.

## What does this application do ?

It will be running every couple minutes (via crontab) (if you decide to use it like that). Each time it will scan home/work network several times for connected devices. It stores scan results and checks wether any device in spied devices list have connected or disconnected since last scan. If it sees change in spied devices list, it informs the owner via email. If someone in spied devices list comes home (connects to network), it plays welcoming audio file. Additionally owner can request a latest scan report via email by sending trigger phrase(by default trigger phrase is "who is there". It can be changed in emailconf.py). Devices are identified according to their mac addresses. User should replace 3rd column (text after mac address) of "spied devices" and "all devices/known devices" with appropriate device names for easy identification (this is in the instructions). Unknown devices that connect to network get stored in unknown devices list. During first connection of an unknown device, owner gets an email notification. Later owner can identify that device and add it to known devices and spied devices list if desired.

## Prerequisites/instructions

Seperate CLI and GUI instructions explain in detail what needs to be done. You can choose any of them and work according to it. Some instructions are same both in GUI and CLI as this application depends on some tools (arp-scan) and python modules (pygame) being installed on your system together with some modifications to sudoers list.

**1. install arp-scan on raspberry pi or on your linux device.**

```sudo apt install arp-scan```

**2. Find out path to arp-scan**

```sudo which arp-scan```

Will tell you where arp-scan was installed. For me it was:/usr/sbin/arp-scan

**3. Edit sudoers list**

```sudo visudo``` if you know how to work with vim or ```sudo nano /etc/sudoers``` to work with nano.

Add following line to the end:

```hsynli ALL = (ALL) NOPASSWD: /usr/sbin/arp-scan```

Replace "hsynli" with your username and "/usr/sbin/arp-scan" with the location from command in step 2.
arp-scan requires sudo privileges to run. This will allow "sudo arp-scan" command to be run without typing password from your current user. This is the safest option as it doesn't require our code to be run as sudo or sudo password to be hardcoded into code. Also it uses full path to arp-scan which reduces the risk of running malicious code instead of arp-scan.

**4. Install pygame module from current regular user (not sudo).**

Pygame should be installed by default, if it is not, install python pygame module from your current user:

```pip3 install pygame```

**5. Connect all of your devices from**

Ensure all of your devices are on and connected to your home network.

**6. Make areyouthere.py and gui.py executable.**

Inside application directory

```sudo chmod +x areyouthere.py```
```sudo chmod +x gui.py```

**7. Continue from instructions files**

Decide on CLI or GUI and read its instructions.

Do not continue before reading selected instruction files. Otherwise application will fail.

If you have decided on using GUI, and done previous steps, you can open GUI with ```./gui.py``` inside application directory and continue reading instructions / making changes from there. 

## Contents

emailconf.py - stores configuration variables.

areyouthere.py - core code. This one is intended to be executed periodically via crontab. 

mailingsystem.py - handles everything related to email.

gui.py - Graphical user interface.

.txt - Various txt files created by this app for it's normal operation.

## Authors

* **Azar Huseynli**
* **Andris Maennik**

## License

This project is licensed under GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

Have a nice day.
