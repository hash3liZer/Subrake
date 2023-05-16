#!/bin/bash
find /usr/share/cockpit/static/subtakes -type f -name "*.csv" -exec tail -n +2 {} + | grep -c ',Possible'