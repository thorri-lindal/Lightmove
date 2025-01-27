#!/bin/bash

# Prompt for source and destination directories
echo "Drag and drop the source directory or directories into this terminal:"
read -r SRC_DIR
SRC_DIR=$(echo "$SRC_DIR" | xargs) # Remove surrounding quotes if any

echo "Drag and drop the destination directory into this terminal:"
read -r DEST_DIR
DEST_DIR=$(echo "$DEST_DIR" | xargs) # Remove surrounding quotes if any

# Check if the source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Source directory does not exist. Exiting."
    exit 1
fi

# Loop through all files in the source directory
find "$SRC_DIR" -type f | while read -r file; do
    # Extract the modification date of the file
    MOD_DATE=$(date -r "$file" +"%Y/%Y-%m-%d")

    # Create the destination folder based on the date
    DEST_FOLDER="$DEST_DIR/$MOD_DATE"
    mkdir -p "$DEST_FOLDER"

    # Sync the file to the destination folder
    rsync -av --checksum "$file" "$DEST_FOLDER/"

    # Generate MD5 hash and save it in a checksum file
    MD5_HASH=$(md5sum "$file" | awk '{print $1}')
    echo "$MD5_HASH  $(basename "$file")" >> "$DEST_FOLDER/md5_checksums.txt"
done

echo "File organization and MD5 hash generation completed!"
