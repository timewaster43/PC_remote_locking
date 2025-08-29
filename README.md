# This script only works when two devices are in the same LAN
In the script I set the port 7834
Before your first use, you should set your trust MAC address (sender's MAC address) and your secret token, these two values should be assigned at the beginning of the script, you can see the relavent variables respectively
Sender Device will send a UDP package two the whole LAN (255.255.255.255:7834) with a message of your secret token
If you are using your mobile phone, you may try **HTTP Shortcuts** -> **Create Shortcut** -> **Scripting Shortcut** -> the script can be "sendUDPPacket(TOKEN_MESSAGE, "255.255.255.255", 7834);"
# PLEASE NOTICE THAT THIS PYTHON SCRIPT MAY REQUIRE ADMIN PRIORITY FROM THE SYSTEM
