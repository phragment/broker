#!/bin/bash

export D="$(dirname $0)"

export RABBITMQ_NODENAME=rabbit1@localhost
export RABBITMQ_NODE_PORT=5672
export RABBITMQ_CONFIG_FILE="$D/rabbit1/config"
export RABBITMQ_MNESIA_BASE="$D/rabbit1/mnesia"
export RABBITMQ_LOG_BASE="$D/rabbit1/log"
export RABBITMQ_ENABLED_PLUGINS_FILE="$D/rabbit1/enabled_plugins"

/usr/lib/rabbitmq/bin/rabbitmq-server

