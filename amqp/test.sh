#!/bin/bash

D="$(dirname $0)"

xfce4-terminal --default-working-directory="$D" -e './rabbit1.sh' &
sleep 1

xfce4-terminal --default-working-directory="$D" -e './rabbit2.sh' &
sleep 3


xfce4-terminal --default-working-directory="$D" -e './client/sub.py' &
sleep 1

xfce4-terminal --default-working-directory="$D" -e './client/pub.py' &
sleep 1

#while true; do sleep 1; done

