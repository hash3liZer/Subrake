#!/bin/bash

find /usr/share/cockpit/static/subtakes -type f -name "subdomains.txt" -exec tail -n +1 {} + | wc -l | awk '{print $1}'