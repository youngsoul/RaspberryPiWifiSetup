__author__ = 'youngsoul'
import string

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

if __name__ == '__main__':
    (i,w) = RaspberryPiWifiSetup.create_wifi_configurations("foo","bar")
    print i
    print w

    (a,b) = RaspberryPiWifiSetup.create_wifi_configurations("baz")
    print a
    print b