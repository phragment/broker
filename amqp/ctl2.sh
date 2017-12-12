#!/bin/bash

export D="$(dirname $0)"

export RABBITMQ_NODENAME=rabbit2@localhost
export RABBITMQ_LOG_BASE="$D/rabbit2/log"

/usr/lib/rabbitmq/bin/rabbitmqctl "$@"

