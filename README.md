
# Lightmove

## Lightroom style by date photo organization with MD5 file verification

This script organizes files into a structured folder hierarchy, the same one used by Adobe Lightroom (`YYYY/YYYY-MM-DD`), based on their modification date and generates MD5 hashes for integrity verification. It also logs all actions performed during the process.

## Features
- Automatically organizes files by date into a nested folder structure.
- Generates `md5_checksums.txt` for each folder to verify file integrity.
- Saves a detailed log file with actions and errors.
- Supports drag-and-drop input for source and destination directories.

---

## Requirements
- **Operating System**: Linux, macOS, or Windows with WSL.
- **Utilities**: `rsync`, `md5sum`, and `find` (installed by default on most Unix-based systems).

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/thorri-lindal/Lightmove.git
cd Lightmove
```

### 2. Make the Script Executable
```bash
chmod +x lightmove.sh
```

### 3. Run the Script
```bash
./lightmove.sh
```

### 4. Drag and Drop Folders
- When prompted, drag and drop the **source directory** (where your files are) into the terminal.
- Drag and drop the **destination directory** (where organized files should be saved).

---

## Output
1. **Organized Files**:
   - Files are moved into a folder structure: `YYYY/YYYY-MM-DD`.
2. **MD5 Checksums**:
   - Each folder contains a `md5_checksums.txt` file with hashes of all files in that folder.
3. **Log File**:
   - A log file (`organization_log_YYYYMMDD_HHMMSS.log`) is saved in the destination directory.

---

## Verifying Files

### Verify Files in a Single Folder
Run this command in a folder containing the `md5_checksums.txt` file:
```bash
md5sum -c md5_checksums.txt
```

### Verify Files Across All Folders
Use the provided script below to verify all files in the destination directory:
```bash
#!/bin/bash
DEST_DIR="/path/to/destination"
find "$DEST_DIR" -name "md5_checksums.txt" | while read -r checksum_file; do
    echo "Verifying files in $(dirname "$checksum_file")"
    md5sum -c "$checksum_file"
done
```

Save this script as `verify_md5.sh`, make it executable, and run:
```bash
chmod +x verify_md5.sh
./verify_md5.sh
```

---

## Example Workflow

1. Drag and drop `/home/user/photos` (source) into the terminal.
2. Drag and drop `/home/user/organized_photos` (destination) into the terminal.
3. The script organizes files by date:
   ```
   /home/user/organized_photos/
   ├── 2023/
   │   ├── 2023-05-01/
   │   │   ├── photo1.jpg
   │   │   ├── photo2.png
   │   │   └── md5_checksums.txt
   │   └── 2023-12-25/
   └── 2024/
   ```
4. Use `md5sum -c` to verify files’ integrity.

---

## License
This project is licensed under the [MIT License](LICENSE).
