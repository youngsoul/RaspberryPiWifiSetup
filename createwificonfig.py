__author__ = 'youngsoul'

#from RaspberryPiWifiSetup import RaspberryPiWifiSetup

import sys
import getopt
import os
import string
import platform

script_dir = os.path.dirname(os.path.abspath(__file__))


interfaces_template = """

auto lo
iface lo inet loopback
allow-hotplug eth0
iface eth0 inet dhcp

allow-hotplug wlan0
auto wlan0
iface wlan0 inet dhcp
\tpre-up wpa_supplicant -Dwext -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -B
iface default inet dhcp

 """

wpa_supplicant_template2 = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
ap_scan=2
network={
     ssid="$network_ssid"
     scan_ssid=1
     proto=RSN
     pairwise=CCMP
     key_mgmt=WPA-PSK
     psk="$network_password"
}
"""

wpa_supplicant_template = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
     ssid="$network_ssid"
     psk="$network_password"
}
"""

open_wpa_supplicant_template = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
ap_scan=2
eapol_version=1
network={
     ssid="$network_ssid"
     scan_ssid=1
     key_mgmt=NONE
}
"""


class RaspberryPiWifiSetup:

    @classmethod
    def create_wifi_configurations(cls, network_ssid, network_password=None):
        '''
        Create the interfaces file content and wpa_supplicant file content
        given an network ssid and password.  For a password protected network
        the SSID can be hidden.
        :param network_ssid: required parameter.  SSID of the wifi network
        :param network_password: optional parameter.  If not specified,
                                 then it is assumed to be an open network.
                                 If it is specified, it is assumed to be the
                                 network password
        :return:
        '''
        intefaces_content = interfaces_template
        if not network_password:
            supplicant_content = string.Template(open_wpa_supplicant_template).substitute({"network_ssid": network_ssid})
        else:
            supplicant_content = string.Template(wpa_supplicant_template).substitute({"network_ssid": network_ssid, "network_password": network_password})

        return intefaces_content, supplicant_content


def _usage():
    print("createwificonfig.py [-s|--ssid <>] [-p|--pwd <>]")


def write_file(the_file, the_data):
    with open(the_file, "wt") as f:
        f.write(the_data)

if __name__ == "__main__":
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "h", ["ssid=", "pwd="])
    except getopt.GetoptError:
        _usage()
        sys.exit(2)

    if len(opts) == 0:
        _usage()
        sys.exit()

    pwd = None
    for opt, arg in opts:
        #print("opt: " + opt)
        if opt == '-h':
            _usage()
            sys.exit()
        elif opt in ("-s", "--ssid"):
            ssid = arg
        elif opt in ("-p", "--pwd"):
            pwd = arg


    print("ssid: " + str(ssid))
    print("pwd: " + str(pwd))

    (iface, supplicant ) = RaspberryPiWifiSetup.create_wifi_configurations(ssid,pwd)
    #print(iface)
    #print(supplicant)

    write_file(script_dir + "/interfaces", iface)
    write_file(script_dir + "/wpa_supplicant.conf", supplicant)

    print("Execute the following commands to setup WIFI configuration....")
    print("sudo rm /var/run/wpa_supplicant/wlan0")
    print("sudo pkill -f wpa_supplicant.conf")
    print("sudo cp ./interfaces /etc/network/")
    print("sudo cp ./wpa_supplicant.conf /etc/wpa_supplicant/")
    print("sudo reboot")

    # if we are on the raspberry pi, ask if we should execute the commands now
    if platform.system() == "Linux":
        prompt = "Would you like to execute the above commands now? y/N"
        ans_response = raw_input(prompt).strip()
        if ans_response == "y" or ans_response == "Y":
            os.system("sudo rm /var/run/wpa_supplicant/wlan0")
            os.system("sudo pkill -f wpa_supplicant.conf")
            os.system("sudo cp ./interfaces /etc/network/")
            os.system("sudo cp ./wpa_supplicant.conf /etc/wpa_supplicant/")
            os.system("sudo rm -f ./interfaces")
            os.system("sudo rm -f ./wpa_supplicant.conf")
            os.system("sudo reboot")


