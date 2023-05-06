#!/bin/bash

echo -n "Enter Domain name: "
read domain

echo -n "Do you want to run online module [Y/n]: "
read omodule

echo -n "Do you want to subcast [Y/n]: "
read subcast

echo -n "Want to provide any wordlist [default/empty for no]: "
read wordlist

echo -n "Any IPs you want to exclude [comma-separated]: "
read excludelist

args="-d '$domain'"

if [ "$omodule" != "Y" && "$omodule" != "y" ]; then
    args="$args --skip-search"
fi

if [ "$subcast" != "Y" && "$subcast" != "y" ]; then
    args="$args --skip-subcast"
else
    args="$args --skip-sublister"
fi

if [ "$wordlist" != "" ]; then
    if [ "$wordlist" == "default" ]; then
    args="$args --wordlists '/opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt'"
fi

if [ "$excludelist" != "" ]; then
    args="$args --exclude-ips '$excludelist'"
fi

subrake $args
exit