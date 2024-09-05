The program is used to monitor devices connected to the LAN network. The program displays devices from a dropdown list based on their types. The user can choose from:

* Computers
* Printers
* IoT Devices
* Server Devices
* All devices connected to the network

The program checks the response of the devices to pings, and depending on the response, it displays the device's status as Online or Offline. If the device responds, the time of the last ping and the latency value in milliseconds are provided. The program checks availability every 10 seconds and updates the displayed messages. After clicking on a specific device, its information will be displayed in a pop-up window. The user can view details such as the device name, IP address, MAC address, the room where it is located, and the connection type.

The list of devices is loaded from an external file and saved in JSON format. In the future, functionality will be added to allow users to add new devices and enable remote computer startup using WOL (Wake-on-LAN), as well as remotely connect to the computer via a previously configured RDP (Remote Desktop Protocol) port.

![MonitorowanieSieci](https://github.com/user-attachments/assets/dae915d7-b5eb-443c-a772-5661c3e14cfc)
