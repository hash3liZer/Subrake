#!/bin/bash
echo $(( $(find /usr/share/cockpit/static/subtakes -maxdepth 1 -type d | wc -l) - 1 ))