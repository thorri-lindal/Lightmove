#!/bin/bash

# Default flags
SHOW_PROGRESS=false
DRY_RUN=false

# Parse flags
while [[ "$1" =~ ^- ]]; do
    case "$1" in
        --progress) SHOW_PROGRESS=true ;;
        --dry) DRY_RUN=true ;;
        *) echo "Unknown option: $1" ;;
    esac
    shift
done

# Prompt for source and destination directories
echo "Drag and drop the source directory or directories into this terminal:"
read -r SRC_DIR
SRC_DIR=$(echo "$SRC_DIR" | xargs) # Remove surrounding quotes if any

echo "Drag and drop the destination directory into this terminal:"
read -r DEST_DIR
DEST_DIR=$(echo "$DEST_DIR" | xargs) # Remove surrounding quotes if any

# Validate source directory
if [ ! -d "$SRC_DIR" ]; then
    echo "Error: Source directory '$SRC_DIR' does not exist. Exiting."
    exit 1
fi

# Validate or create destination directory
if [ ! -d "$DEST_DIR" ]; then
    echo "Destination directory '$DEST_DIR' does not exist. Creating it..."
    mkdir -p "$DEST_DIR"
fi

# Loop through all files in the source directory
find "$SRC_DIR" -type f | while read -r file; do
    # Extract the modification date of the file
    MOD_DATE=$(date -r "$file" +"%Y/%Y-%m-%d")

    # Create the destination folder based on the date
    DEST_FOLDER="$DEST_DIR/$MOD_DATE"
    mkdir -p "$DEST_FOLDER"

    # Set rsync flags
    RSYNC_FLAGS="-a --checksum"
    [[ "$DRY_RUN" == true ]] && RSYNC_FLAGS="$RSYNC_FLAGS --dry-run"

    # Sync the file to the destination folder
    if [[ "$SHOW_PROGRESS" == true ]]; then
        echo "Syncing: $file -> $DEST_FOLDER/"
        rsync $RSYNC_FLAGS --progress "$file" "$DEST_FOLDER/"
    else
        rsync $RSYNC_FLAGS "$file" "$DEST_FOLDER/" > /dev/null 2>&1
    fi

    # Only generate MD5 hashes if not in dry-run mode
    if [[ "$DRY_RUN" == false ]]; then
        DEST_FILE="$DEST_FOLDER/$(basename "$file")"
        MD5_HASH=$(md5sum "$DEST_FILE" | awk '{print $1}')
        echo "$MD5_HASH  $(basename "$file")" >> "$DEST_FOLDER/md5_checksums.txt"
    fi
done

# Final message
if [[ "$DRY_RUN" == true ]]; then
    echo
    echo "----------------------------------------"
    echo "Dry run completed. No files were copied or modified."
    echo "----------------------------------------"
else
    echo
    echo "----------------------------------------"
    echo "File organization and MD5 hash generation completed!"
    echo "----------------------------------------"
fi
