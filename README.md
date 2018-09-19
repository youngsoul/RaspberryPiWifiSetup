
Raspberry Pi Wifi Setup
========================

Project to help create the interfaces and wpa_supplicant.conf files
necessary to setup wifi on a Raspberry pi.

After spending many frustrating hours trying to get the right magic incantation
necessary to make this work - after I finally got what I believe to be a
repeatable process - I thought I would script it so I can generate the files at will.

This has worked for me on a model B Raspberry Pi.

There are 2 files:

RaspberryPiWifiSetup.py

This class has a single static method that takes a ssid and an optional password,
and produces strings for the interface and wpa_supplicant files.  It assumes WPA
security, at the moment, but the ssid can be either broadcast or hidden.  If no
password is given, it assume you are trying to connect to an open wifi network.

createwificonfig.py

This is a script that takes command line arguments for the ssid and pwd and then
generates actual files.

Usage:

python createwificonfig.py --ssid="my ssid" --pwd="my password"

I hope you find it useful.

