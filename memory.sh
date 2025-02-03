#!/bin/bash
command_to_run="free -m"

output_file="Memory.txt"

while true; do
    $command_to_run >> $output_file
    sleep 60
done