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

echo -n "Specify Ports you want to scan [Empty to leave]: "
read ports

echo -n "Number of threads to generate [25]: "
read threads

args="-d $domain -o /opt/subtakes/$domain/subdomains.txt --csv /opt/subtakes/$domain/report.csv --filter"

if [ "$omodule" != "Y" ] && [ "$omodule" != "y" ]; then
    args="$args --skip-search"
fi

if [ "$subcast" != "Y" ] && [ "$subcast" != "y" ]; then
    args="$args --skip-subcast"
else
    args="$args --only-sublister"
fi

if [ "$wordlist" != "" ]; then
    if [ "$wordlist" == "default" ]; then
    args="$args --wordlists /opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt"
    fi
fi

if [ "$excludelist" != "" ]; then
    args="$args --exclude-ips '$excludelist'"
fi

if [ "$ports" != "" ]; then
    args="$args --ports '$ports'"
fi

if [ "$threads" != "" ]; then
    args="$args --threads $threads"
fi

mkdir /opt/subtakes/$domain

subrake $args
exit