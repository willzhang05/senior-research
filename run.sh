#!/bin/sh
sudo ip tuntap add tun0 mode tun
sudo ip addr add 10.0.0.2/24 dev tun0
sudo nohup ~/mcproxy/mcproxy -dsvv -f ~/mcproxy/mcproxy.conf &
sudo nohup ~/senior-research/amt/gateway/amtgwd -a 198.38.23.145 -c tun0
