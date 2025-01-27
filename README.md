
# Lightmove
![Alt text](https://raw.githubusercontent.com/thorri-lindal/Lightmove/refs/heads/main/lightmove.png "lightmove")

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
- When prompted, drag and drop the **source directory** (where your photos are) into the terminal.
- Drag and drop the **destination directory** (where organized photos should be saved).

---

## Output
1. **Organized Files**:
   - photos are moved into a folder structure: `YYYY/YYYY-MM-DD`.
2. **MD5 Checksums**:
   - Each folder contains a `md5_checksums.txt` file with hashes of all photos in that folder.
3. **Log File**:
   - A log file (`organization_log_YYYYMMDD_HHMMSS.log`) is saved in the destination directory.

---

### 2. Verify Files

Use the `verify_md5.sh` script to verify files against their `md5_checksums.txt`.

#### Steps:
1. Run the script:
   ```bash
   ./verify_md5.sh
   ```
2. Drag and drop one or more directories into the terminal (e.g., `/home/user/organized_photos/2023`).
3. Press **Enter** to start the verification.

#### Example:
- Input:
  ```
  Drag and drop the directories you want to verify: 
  '/home/user/organized_photos/2023/2023-05-01' '/home/user/organized_photos/2023/2023-12-25'
  ```
- Output:
  ```
  Starting verification in /home/user/organized_photos/2023/2023-05-01...
  Verifying files in /home/user/organized_photos/2023/2023-05-01
  photo1.jpg: OK
  Verification completed for /home/user/organized_photos/2023/2023-05-01.

  Starting verification in /home/user/organized_photos/2023/2023-12-25...
  Verifying files in /home/user/organized_photos/2023/2023-12-25
  photo2.png: OK
  Verification completed for /home/user/organized_photos/2023/2023-12-25.

  All directories have been verified.
  ```

---

## Scripts in This Project

1. **organize_files_with_log.sh**:
   - Organizes photos into `YYYY/YYYY-MM-DD` folders based on modification dates.
   - Generates `md5_checksums.txt` for each folder.
   - Saves a log of all actions performed.

2. **verify_md5.sh**:
   - Verifies files using the `md5_checksums.txt` files.
   - Supports drag-and-drop for multiple directories.
## Scripts in This Project

1. **organize_files_with_log.sh**:
   - Organizes photos into `YYYY/YYYY-MM-DD` folders based on modification dates.
   - Generates `md5_checksums.txt` for each folder.
   - Saves a log of all actions performed.

2. **verify_md5.sh**:
   - Verifies files using the `md5_checksums.txt` files.
   - Supports drag-and-drop for multiple directories.

---

## License
This project is licensed under the [MIT License](LICENSE).
