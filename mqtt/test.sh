#!/bin/bash

D="$(dirname $0)"

xfce4-terminal --default-working-directory="$D" -e 'mosquitto -c mosq1.conf' &
sleep 1

xfce4-terminal --default-working-directory="$D" -e 'mosquitto -c mosq2.conf' &
sleep 1


xfce4-terminal --default-working-directory="$D" -e './client/sub.py' &
sleep 1

xfce4-terminal --default-working-directory="$D" -e './client/pub.py' &
sleep 1

#mosquitto_sub -h 127.0.0.1 -p 1337 -q 0 -t foo/bar
#mosquitto_pub -h 127.0.0.1 -p 1338 -q 0 -m test -t foo/bar

#while true; do sleep 1; done

