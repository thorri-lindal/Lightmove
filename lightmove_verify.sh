#!/bin/bash

echo "Drag and drop the directories you want to verify into this terminal, then press Enter:"
read -r INPUT_PATHS

# Convert the input string into an array, splitting by spaces while preserving paths with spaces
IFS=' ' read -r -a PATH_ARRAY <<< "$(echo "$INPUT_PATHS" | sed 's/"//g')"

# Loop through all provided paths
for DEST_DIR in "${PATH_ARRAY[@]}"; do
    # Trim and clean the directory path
    DEST_DIR=$(echo "$DEST_DIR" | xargs)

    # Check if the directory exists
    if [ ! -d "$DEST_DIR" ]; then
        echo "Error: Directory '$DEST_DIR' does not exist. Skipping."
        continue
    fi

    echo "Starting verification in $DEST_DIR..."
    # Find all md5_checksums.txt files and verify them
    find "$DEST_DIR" -type f -name "md5_checksums.txt" | while IFS= read -r checksum_file; do
        echo "Verifying files in $(dirname "$checksum_file")"
        (cd "$(dirname "$checksum_file")" && md5sum -c "$(basename "$checksum_file")")
    done
    echo "Verification completed for $DEST_DIR."
done

echo "All directories have been verified."
exit 0
