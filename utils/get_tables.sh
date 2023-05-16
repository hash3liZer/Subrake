#!/bin/bash

folder="/usr/share/cockpit/static/subtakes"

# Get the list of directories under the folder
directories=$(find "$folder" -mindepth 1 -maxdepth 1 -type d)

declare -A rtval

# Loop through each directory
for dir in $directories; do
    # Get base name of dir
    basename=$(basename "$dir")
    sessionname="${basename//.}"

    # Initialize the section dictionary
    declare -A section

    # Emptying the section
    section["name"]="$basename"
    section["datetime"]="Undefined"
    section["subdomains"]="0"
    section["status"]="Undefined"
    section["takeovers"]="0"

    # Date Collection
    if [ -e "$dir/datetime.txt" ]; then
        section["datetime"]="$(cat "$dir/datetime.txt")"
    fi

    # Subdomain Collection
    if [ -e "$dir/report.csv" ]; then
        section["subdomains"]="$(tail -n +2 "$dir/report.csv" | grep -i "$basename" | wc -l)"
    fi

    # Status Collection
    if tmux has-session -t "$sessionname" 2>/dev/null; then
        section["status"]="Running"
    else
        if [ -e "$dir/report.csv" ] && [ -e "$dir/subdomains.txt" ] && [ -e "$dir/datetime.txt" ]; then
            section["status"]="Completed"
        else
            section["status"]="Stopped"
        fi
    fi

    # Takeover Collection
    if [ -e "$dir/report.csv" ] && [ -e "$dir/subdomains.txt" ] && [ -e "$dir/datetime.txt" ]; then
        section["takeovers"]="$(tail -n +2 "$dir/report.csv" | grep -i ",Possible" | wc -l)"
    fi

    # Add the section to the rtval dictionary
    rtval["$basename"]="${section[@]}"
done

# Convert the rtval dictionary to JSON using jq
json_string=$(declare -p rtval | jq -c .)
echo "$json_string"
