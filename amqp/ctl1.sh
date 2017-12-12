#!/bin/bash

export D="$(dirname $0)"

export RABBITMQ_NODENAME=rabbit1@localhost
export RABBITMQ_LOG_BASE="$D/rabbit1/log"

/usr/lib/rabbitmq/bin/rabbitmqctl "$@"

