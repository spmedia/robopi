#!/bin/bash
clear

echo
echo "################################################################################"
echo "# RoboPi v.1.1.1                                                               #"
echo "# @author Joshua Richard <www.joshrichard.net>                                 #"
echo "# @license MIT                                                                 #"
echo "################################################################################"

wget http://node-arm.herokuapp.com/node_latest_armhf.deb
sudo dpkg -i node_latest_armhf.deb
sudo rm -f node_latest_armhf.deb

sudo apt-get -y install isc-dhcp-server python-pip nodejs libnl-dev libssl-dev chromium  python-virtualenv python-opencv

sudo ip link set up dev wlan0

sudo ip addr add 192.168.87.1/24 dev wlan0

sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak
sudo touch /etc/dhcp/dhcpd.conf
sudo cp ./system/dhcpd.conf /etc/dhcp/dhcpd.conf

sudo mv /etc/default/isc-dhcp-server /etc/default/isc-dhcp-server.bak
sudo touch /etc/default/isc-dhcp-server
sudo cp ./system/isc-dhcp-server /etc/default/isc-dhcp-server

sudo ifdown wlan0
sudo ifconfig wlan0 192.168.87.1

sudo mkdir /root/src

sudo cd /root/src; sudo wget http://w1.fi/releases/hostapd-2.4.tar.gz
sudo tar -xf /root/src/hostapd-2.4.tar.gz

sudo cd /root/src/hostapd-2.4/hostapd; sudo cp defconfig .config
sudo make
sudo make install

sudo mkdir /etc/hostapd
sudo cp ./system/hostapd.conf /etc/hostapd/hostapd.conf

pip install pyserial
sudo pip install flask
sudo pip install cv2
