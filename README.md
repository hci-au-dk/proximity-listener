proximity-listener
==================

This python script allows for listening for the signal strengths of all devices connected wirelessly to a given SSID and post it to a given URL.

Installation
============

Requirements:
-------------

 * http://www.aircrack-ng.org compiled from source
 * Python libraries watchdog (0.6.0) and requests (2.0.0)
   + Install e.g. with pip install -r requirements.txt

Getting the code:
-----------------

 * git clone https://github.com/hci-au-dk/proximity-listener.git
 
Howto run
=========

Start by doing a

    sudo airmon-ng

Then in the proximity-listener dir do

    sudo airodump-ng mon0 --output-format csv -w proximity
  
Now you can start the listener e.g. by

    python proximity_listener.py "1" MySSID proximity-01.csv http://localhost:3000


 
  