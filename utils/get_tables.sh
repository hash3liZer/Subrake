#!/bin/bash

folder="/usr/share/cockpit/static/subtakes"

# Get the list of directories under the folder
directories=$(find "$folder" -mindepth 1 -maxdepth 1 -type d)

# Initialize the rtval associative array
declare -A rtval

# Loop through each directory
for dir in $directories; do
    # Get base name of dir
    basename=$(basename "$dir")
    sessionname="${basename//.}"

    # Initialize the section associative array
    declare -A section

    # Emptying the section
    section["name"]="$basename"
    section["datetime"]="Undefined"
    section["subdomains"]="0"
    section["status"]="Undefined"
    section["takeovers"]="0"

    # Date Collection
    if [ -e "$dir/datetime.txt" ]; then
        data=$(cat "$dir/datetime.txt")
        data=${data// /_}
        section["datetime"]="$data"
    fi

    # Subdomain Collection
    if [ -e "$dir/report.csv" ]; then
        section["subdomains"]=$(tail -n +2 "$dir/report.csv" | grep -i "$basename" | wc -l)
    fi

    # Status Collection
    if tmux has-session -t "$sessionname" 2>/dev/null; then
        section["status"]="Running"
    else
        if [ -e "$dir/report.csv" ] && [ -e "$dir/subdomains.txt" ] && [ -e "$dir/datetime.txt" ]; then
            section["status"]="Completed"
        else
            section["status"]="Killed"
        fi
    fi

    # Takeover Collection
    if [ -e "$dir/report.csv" ] && [ -e "$dir/subdomains.txt" ] && [ -e "$dir/datetime.txt" ]; then
        section["takeovers"]=$(tail -n +2 "$dir/report.csv" | grep -i ",Possible" | wc -l)
    fi

    # Add the section to the rtval array
    rtval["$basename"]="${section[@]}"
done

# Construct the JSON string manually
json_string="{"
for key in "${!rtval[@]}"; do
    json_string+="\"$key\": ["
    section_values="${rtval[$key]}"
    IFS=" " read -r -a values_array <<< "$section_values"
    for value in "${values_array[@]}"; do
        json_string+="\"$value\","
    done
    json_string="${json_string%,}"  # Remove the trailing comma
    json_string+="],"
done
json_string="${json_string%,}"  # Remove the trailing comma
json_string+="}"

echo "$json_string"
