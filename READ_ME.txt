This application was developed by Azar Huseynli and Andris Maennik for Python Programming course at Tartu University.

Upon completion of this application we decided to add it to the "IT Student Project Contest" organized by Tartu University.

It is intended to be installed on a device (running linux) that is connected to home or office network. Preferably raspberry pi that is connected to audio system and runs 24/7. Initially we intended it to be CLI only but later decided to add simple GUI also.

What does this application do ?

It will be running every couple minutes (via crontab). Each time it will scan home/work network for connected devices. It stores scan results and checks wether any device in spied devices list have connected or disconnected since last scan. If it sees change in spied devices list, it informs the owner via email. If someone in spied devices list comes home, it plays welcoming audio file. Additionally owner can request a latest scan report via email by sending trigger phrase. Devices are identified according to their mac addresses. User should replace 3rd column (text after mac address) of "spied devices" and "all devices/known devices" with appropriate device names for easy identification (this is in the instructions). Unknown devices that connect to network get stored in unknown devices list. During first connection of an unknown device, owner gets an email notification. Later owner can identify that device and add it to known devices and spied devices list if desired.

emailconf.py - stores configuration variables.
areyouthere.py - core code. This one is intended to be executed periodically via crontab. 
mailingsystem.py - handles everything related to email.
gui.py - Graphical user interface.

Decide on CLI or GUI read its instructions.
Do not continue before reading selected instruction files. Otherwise application will fail.

Have a nice day.
License: GNU General Public License v3.0 (https://choosealicense.com/licenses/gpl-3.0/)
