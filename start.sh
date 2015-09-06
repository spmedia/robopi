#!/bin/bash

if [ "$1" != "restart" ]; then
  clear
  echo
  echo "################################################################################"
  echo "# RoboPi                                                                       #"
  echo "# @author Joshua Richard <www.joshrichard.net>                                 #"
  echo "# @license MIT                                                                 #"
  echo "################################################################################"
  echo
  echo "Starting services..."
  sudo ifconfig wlan0 192.168.87.1/24 up
  sleep 1
  sudo service isc-dhcp-server start
  sudo hostapd -B /etc/hostapd/hostapd.conf
fi

echo
echo "Starting python controller..."
cd /home/pi/robopi/python; python control.py >/dev/null 2>&1 &
sleep 3
echo "Starting video feed..."
cd /home/pi/robopi/python; python video_feed.py >/dev/null 2>&1 &
sleep 3
echo "Installing npm package..."
cd /home/pi/robopi/nodejs; npm install
sleep 5
echo "Running npm package..."
cd /home/pi/robopi/nodejs; npm start >/dev/null 2>&1 &
sleep 10
echo "Configuring system..."
sleep 5
echo "Opening screen display..."
sleep 5
DISPLAY=:0.0 chromium -kiosk http://localhost:61337/display >/dev/null 2>&1 &
sleep 8
