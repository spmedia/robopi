#!/bin/bash
clear

echo
echo "################################################################################"
echo "# RoboPi                                                                       #"
echo "# @author Joshua Richard <www.joshrichard.net>                                 #"
echo "# @license MIT                                                                 #"
echo "################################################################################"

echo
echo "Killing any running services..."
echo

killall node
killall python
killall chromium

echo
echo "Updating code..."
echo

cd /home/pi/robopi; git pull

sh ./start.sh restart

#sudo reboot
