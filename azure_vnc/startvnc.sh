#!/bin/sh
CERT_FILE=/etc/ssl/dincloud.com.crt
CERT_KEY=/etc/ssl/dincloud.com.key
DIN_TIMEOUT=500

/usr/share/novnc/websockify/run -D -v --web /usr/share/novnc --timeout $DIN_TIMEOUT --cert $CERT_FILE --key $CERT_KEY --token-plugin ReadOnlyString --token-source "$1: $2:5901" $3
