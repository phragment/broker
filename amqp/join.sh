#!/bin/bash

./ctl2.sh cluster_status

./ctl2.sh stop_app
./ctl2.sh join_cluster rabbit1@localhost
./ctl2.sh start_app

./ctl2.sh cluster_status


#./ctl2.sh set_policy ha-test "^test" \ '{"ha-mode":"exactly","ha-params":2,"ha-sync-mode":"automatic"}'

./ctl2.sh set_policy ha-all "^ha" '{"ha-mode":"all"}'

