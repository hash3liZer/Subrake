#!/bin/bash

find /usr/share/cockpit/static/subtakes -type f -name "*.csv" -exec tail -n +2 {} + | wc -l | awk '{print $1}'