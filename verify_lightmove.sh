#!/bin/bash

echo "Drag and drop the directories you want to verify into this terminal, then press Enter:"
read -r INPUT_PATHS
INPUT_PATHS=$(echo "$INPUT_PATHS" | xargs) # Remove surrounding quotes and extra spaces

# Start the timer
START_TIME=$(date +%s)

# Split the input into an array of directories
IFS=' ' read -r -a DIR_ARRAY <<< "$INPUT_PATHS"

# Loop through each provided directory
for DIR in "${DIR_ARRAY[@]}"; do
    # Check if the directory exists
    if [ ! -d "$DIR" ]; then
        echo "Error: Directory '$DIR' does not exist. Skipping."
        continue
    fi

    echo "Starting verification in '$DIR'..."
    # Find all xxhash_checksums.txt files in the directory
    find "$DIR" -type f -name "xxhash_checksums.txt" | while read -r checksum_file; do
        CHECKSUM_DIR=$(dirname "$checksum_file")
        echo "Verifying files in '$CHECKSUM_DIR'..."

        # Read the checksum file and verify each file
        while IFS= read -r line; do
            EXPECTED_HASH=$(echo "$line" | awk '{print $1}')
            FILE_NAME=$(echo "$line" | awk '{print $2}')
            FILE_PATH="$CHECKSUM_DIR/$FILE_NAME"

            # Check if the file exists
            if [ ! -f "$FILE_PATH" ]; then
                echo "MISSING: $FILE_NAME (expected hash: $EXPECTED_HASH)"
                continue
            fi

            # Compute the XXHash for the file
            ACTUAL_HASH=$(xxhsum "$FILE_PATH" | awk '{print $1}')

            # Compare the actual hash with the expected hash
            if [[ "$ACTUAL_HASH" == "$EXPECTED_HASH" ]]; then
                echo "OK: $FILE_NAME"
            else
                echo "FAILED: $FILE_NAME (expected: $EXPECTED_HASH, actual: $ACTUAL_HASH)"
            fi
        done < "$checksum_file"
    done
    echo "Verification completed for '$DIR'."
done

# End the timer
END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))

echo
echo "----------------------------------------"
echo "All directories have been verified."
echo "Total time taken: $ELAPSED_TIME seconds."
echo "----------------------------------------"
