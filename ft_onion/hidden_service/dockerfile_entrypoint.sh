#!/bin/sh
# sleep 1000000
tor -f /hidden_service/tor/torrc &
mkdir -p /run/openrc
touch /run/openrc/softlevel
rc-service sshd start
nginx -g "daemon off;"
