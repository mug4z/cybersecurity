#!/bin/sh
# sleep 1000000
tor -f /hidden_service/tor/torrc &
nginx -g "daemon off;"
