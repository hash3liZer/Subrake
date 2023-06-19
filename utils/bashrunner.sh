#!/bin/bash

trap '' INT

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
MAGENTA="\e[35m"
CYAN="\e[36m"
WHITE="\e[37m"
RESET="\e[0m"

while true; do
    clear
    echo -en "${RED}[?]${RESET} Enter Domain name                                  : ${GREEN}"
    read domain

    session="${domain//.}"

    args="-d $domain -o /usr/share/cockpit/static/subtakes/$domain/subdomains.txt --csv /usr/share/cockpit/static/subtakes/$domain/report.csv --filter"

    if tmux has-session -t "$session" 2>/dev/null; then
    echo -e "${MAGENTA}[-]${RESET} A screen session with the name '$domain' already exists."
    echo -en "${YELLOW}[?]${RESET} Do you want to jump to that session or skip? (y/n) "
    read choice
        case "$choice" in
            y|Y)
                tmux attach-session -t "$session"
                continue
                ;;
            *)
                clear
                continue
                ;;
        esac
    fi

    echo -en "${RED}[?]${RESET} Do you want to run online module [Y/n]             : ${YELLOW}"
    read omodule

    echo -en "${RED}[?]${RESET} Do you want to subcast [Y/n]                       : ${YELLOW}"
    read subcast

    if [ "$subcast" != "Y" ] && [ "$subcast" != "y" ]; then
        args="$args --skip-subcast"
    # else
    #     echo -en "${RED}[?]${RESET} Run only Sublist3r (Resource Efficient) [Y/n]      : ${YELLOW}"
    #     read osublist3r
    #     if [ "$osublist3r" == "Y" ] || [ "$osublist3r" == "y" ]; then
    #         args="$args --only-sublister"
    #     fi
    fi

    echo -en "${RED}[?]${RESET} Select a Wordlist from below (you can select multiple using ,): "
    echo -e "\n"
    echo -e  "${YELLOW}[?]${RESET} 1. 5000 Entries"
    echo -e  "${YELLOW}[?]${RESET} 2. 20000 Entries"
    echo -e  "${YELLOW}[?]${RESET} 3. Knockpy >10000 Entries"
    echo -e  "${YELLOW}[?]${RESET} 4. Deepmagic Top 500 Entries"
    echo -en "\n"
    echo -en "${RED}[?]${RESET} Your Option (Leave empty for none): ${MAGENTA}"
    read wordlist

    if [ "$wordlist" != "" ]; then
        IFS=',' read -ra values <<< "$wordlist"

        nwords=""
        for value in "${values[@]}"; do
            if [ $value == "1" ]; then
                nwords+="/opt/subrake_wordlists/subdomains-top1million-5000.txt,"
            elif [ $value == "2" ]; then
                nwords+="/opt/subrake_wordlists/subdomains-top1million-20000.txt,"
            elif [ $value == "3" ]; then
                nwords+="/opt/subrake_wordlists/knockpy_wordlist.txt,"
            elif [ $value == "4" ]; then
                nwords+="/opt/subrake_wordlists/deepmagic_top500.txt,"
            else
                echo -e "${RED}[-]${RESET} Invalid Dictionary Option ..."
                read
                exit 1
            fi
        done

        # Get last character and remove it if its comma
        last_character="${nwords: -1}"
        if [[ "$last_character" == "," ]]; then
            nwords="${nwords%?}"
        fi
        args="$args --wordlists $nwords"
    fi

    echo -en "${RED}[?]${RESET} Any IPs you want to exclude [comma-separated]      : ${YELLOW}"
    read excludelist

    echo -en "${RED}[?]${RESET} Specify Ports you want to scan [Empty to leave]    : ${YELLOW}"
    read ports

    echo -en "${RED}[?]${RESET} Number of threads to generate [25]                 : ${YELLOW}"
    read threads

    if [ -z "$omodule" ] && [ -z "$subcast" ] && [ -z "$wordlist" ]; then
        exit 1
    fi

    if [ "$omodule" != "Y" ] && [ "$omodule" != "y" ]; then
        args="$args --skip-search"
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

    echo $args

    mkdir -p /usr/share/cockpit/static/subtakes/$domain
    echo "$(date)" > /usr/share/cockpit/static/subtakes/$domain/datetime.txt

    tmux new-session -d -s "$session" "tmux source-file /opt/.tmux.conf; bash -c 'subrake $args; echo; echo; echo -en \"${MAGENTA}[-]${RESET} Press any key to continue...\"; read; exit'"
    tmux attach-session -t "$session"
    # clear
done