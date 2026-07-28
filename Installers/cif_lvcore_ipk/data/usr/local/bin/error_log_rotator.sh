#!/bin/sh
MAX_SIZE=1048576 # 1MB in bytes
LOG_FILE="/var/local/cif/logs/cif_error.log"

while IFS= read -r line; do
    # Append full line cleanly
    echo "$line" >> "$LOG_FILE"

    # Check file size after the write operation
    FILE_SIZE=$(wc -c < "$LOG_FILE")
    if [ "$FILE_SIZE" -ge "$MAX_SIZE" ]; then
        # Perform clean rotation up to 3 files
        rm -f /var/local/cif/logs/cif_error.log.2
        mv /var/local/cif/logs/cif_error.log.1 /var/local/cif/logs/cif_error.log.2 2>/dev/null
        mv /var/local/cif/logs/cif_error.log /var/local/cif/logs/cif_error.log.1 2>/dev/null
        touch "$LOG_FILE"
    fi
done