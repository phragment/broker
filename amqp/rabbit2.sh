#!/bin/bash

export D="$(dirname $0)"

export RABBITMQ_NODENAME=rabbit2@localhost
export RABBITMQ_NODE_PORT=5673
export RABBITMQ_CONFIG_FILE="$D/rabbit2/config"
export RABBITMQ_MNESIA_BASE="$D/rabbit2/mnesia"
export RABBITMQ_LOG_BASE="$D/rabbit2/log"
export RABBITMQ_ENABLED_PLUGINS_FILE="$D/rabbit2/enabled_plugins"

/usr/lib/rabbitmq/bin/rabbitmq-server

