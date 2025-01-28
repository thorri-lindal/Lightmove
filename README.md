# Lightmove
![Alt text](https://raw.githubusercontent.com/thorri-lindal/Lightmove/refs/heads/main/lightmove.png "lightmove")

## Photo Organization with xxHash and Verification

This project provides tools to organize files into a structured folder hierarchy (`YYYY/YYYY-MM-DD`) based on their modification date, with xxHash-based integrity verification. It also logs all actions performed during the process.

---

## Requirements
- **Operating System**: Linux, macOS, or Windows with WSL.
- **Utilities**: `rsync`, `md5sum`, and `find` (installed by default on most Unix-based systems).

---

## Features

1. **File Organization**:
   - Automatically organizes files into a nested folder structure based.
   - Supports filtering by file type, size, and skipping existing files.
2. **Drag-and-drop support**:
	-Supports drag-and-drop input for source and destination directories.
   
4. **Integrity Verification**:
   - Generates `checksums.txt` with xxHash for each folder.
   - Logs verification results and identifies missing or modified files.

4. **Enhanced Logging**:
   - Detailed logs are saved to track operations and errors.

5. **Parallel Processing**:
   - Multi-threaded for faster performance.

6. **Customization Options**:
   - Supports dry-run mode, progress bars, and user-defined filters.

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/thorri-lindal/Lightmove.git
cd Lightmove
```

### 2. Activate the Virtual Environment
Activate your pre-configured virtual environment to ensure all dependencies are correctly set up.

For Bash or Zsh
```
source venv/bin/activate
```
For Fish
```
source venv/bin/activate.fish
```
For PowerShell
```
.\venv\Scripts\Activate.ps1
```
For Command Prompt
```
venv\Scripts\activate.bat
```
### 3. Organize Files
Run the script:
```bash
python lightmove.py --progress --parallel-jobs-8 --dry
Source directory (drag and drop or type path): '/home/user/photos' 
Destination directory (drag and drop or type path): '/home/user/sorted-photos'
```

#### Optional Arguments:
- `--file-type`: Specify file extensions (e.g., `--file-type .jpg .png`).
- `--min-size` and `--max-size`: Filter by file size in bytes.
- `--skip-existing`: Skip already organized files.
- `--dry-run`: Preview actions without making changes.
- `--progress`: Display a progress bar.

#### Example:
```bash
python lightmove.py
Source directory (drag and drop or type path): '/home/user/pics' 
Destination directory (drag and drop or type path): '/home/user/pics-sorted'
```

---

### 4. Verify Files
Run the verification script:
```bash
python verify.py --progress
```

Follow the prompts to specify the directory containing `checksums.txt`.

#### Example Output:
```plaintext
Starting checksum verification in '/path/to/organized_files'...
MATCH: photo1.jpg
MISMATCH: photo2.png (expected: <hash>, actual: <hash>)
MISSING: photo3.jpg
Verification completed with mismatches or missing files.
```
---

## Example Output

- **Organized Files**:
  ```
  /destination/
  ├── 2023/
  │   ├── 2023-05-01/
  │   │   ├── photo1.jpg
  │   │   └── checksums.txt
  └── 2023-12-25/
      ├── photo2.png
      └── checksums.txt
  ```

- **Logs**:
  ```
  organize_files.log
  xxhash3_verification.log
  ```

---

## Future Updates

- [X] Rewrite in Python3
- [ ] Advanced file type and metadata filtering.
- [ ] Integrate more hashing algorithms for flexibility.
- [X] Replace MD5 with xxHash for performance gains.

---

## License
This project is licensed under the [MIT License](LICENSE).
