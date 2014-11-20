__author__ = 'youngsoul'

from RaspberryPiWifiSetup import RaspberryPiWifiSetup

import sys
import getopt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))


def _usage():
    print("createwificonfig.py [-s|--ssid <>] [-p|--pwd <>]")


def write_file(the_file, the_data):
    with open(the_file, "wt") as f:
        f.write(the_data)

if __name__ == "__main__":
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hs:p:", ["ssid=", "pwd="])
    except getopt.GetoptError:
        _usage()
        sys.exit(2)

    if len(opts) == 0:
        _usage()
        sys.exit()

    pwd = None
    for opt, arg in opts:
        print("opt: " + opt)
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
    print iface
    print supplicant

    write_file(script_dir + "/interfaces", iface)
    write_file(script_dir + "/wpa_supplicant.conf", supplicant)

    print "run: sudo cp ./interfaces /etc/network/"
    print "run: sudo cp ./wpa_supplicant.conf /etc/wpa_supplicant/"
    print "run: sudo reboot"


