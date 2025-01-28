import os
import time
import xxhash
from pathlib import Path

RED = "\033[0;31m"
GREEN = "\033[0;32m"
RESET = "\033[0m"

HAS_ERRORS = False

def compute_checksum(file_path: Path) -> str:
    """
    Compute the xxhash3 checksum for a given file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        str: The hexadecimal checksum.
    """
    hash_func = xxhash.xxh3_64()
    with file_path.open("rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_checksums_in_file(checksum_file: Path, log_file: Path, show_progress: bool):
    """
    Verify all files listed in a checksum file.

    Args:
        checksum_file (Path): Path to the checksum file.
        log_file (Path): Path to the log file.
        show_progress (bool): Whether to display progress line by line in the terminal.
    """
    global HAS_ERRORS
    folder = checksum_file.parent

    with checksum_file.open("r") as f, log_file.open("a") as log:
        for line in f:
            try:
                expected_hash, file_name = line.strip().split(maxsplit=1)
            except ValueError:
                log.write(f"INVALID LINE: {line.strip()} in {checksum_file}\n")
                print(f"{RED}INVALID LINE: {line.strip()} in {checksum_file}{RESET}")
                HAS_ERRORS = True
                continue

            full_path = folder / file_name

            if not full_path.exists():
                message = f"MISSING: {file_name} (expected hash: {expected_hash})"
                log.write(message + "\n")
                if show_progress:
                    print(f"{RED}{message}{RESET}")
                HAS_ERRORS = True
                continue

            actual_hash = compute_checksum(full_path)
            if actual_hash == expected_hash:
                message = f"MATCH: {file_name}"
                log.write(message + "\n")
                if show_progress:
                    print(f"{GREEN}{message}{RESET}")
            else:
                message = f"MISMATCH: {file_name} (expected: {expected_hash}, actual: {actual_hash})"
                log.write(message + "\n")
                if show_progress:
                    print(f"{RED}{message}{RESET}")
                HAS_ERRORS = True

def main():
    """
    Main function to verify checksums recursively.
    """
    global HAS_ERRORS

    # Ask for the directory to verify
    print("Please enter or drag-and-drop the destination directory to verify:")
    verify_dir = input().strip().strip("'").strip('"')
    verify_dir_path = Path(verify_dir)

    if not verify_dir_path.is_dir():
        print(f"{RED}Error: Directory '{verify_dir_path}' does not exist. Exiting.{RESET}")
        return

    # Log file path in the destination directory
    log_file_path = verify_dir_path / "xxhash3_verification.log"
    log_file_path.write_text("")  # Clear the log file

    start_time = time.time()
    print(f"Starting checksum verification in '{verify_dir_path}'...")
    print(f"Verification log: {log_file_path}")

    # Find all `checksums.txt` files recursively
    checksum_files = list(verify_dir_path.rglob("checksums.txt"))

    if not checksum_files:
        print(f"{RED}No 'checksums.txt' files found in '{verify_dir_path}'. Exiting.{RESET}")
        return

    for checksum_file in checksum_files:
        print(f"Verifying checksums in: {checksum_file.parent}")
        verify_checksums_in_file(checksum_file, log_file_path, "--progress" in os.sys.argv)

    elapsed_time = time.time() - start_time

    # Final summary
    with log_file_path.open("a") as log:
        if HAS_ERRORS:
            log.write("ERROR: Verification completed with mismatches or missing files.\n")
            print(f"{RED}ERROR: Verification completed with mismatches or missing files.{RESET}")
        else:
            log.write("SUCCESS: All files verified successfully!\n")
            print(f"{GREEN}SUCCESS: All files verified successfully!{RESET}")
        log.write(f"Total time taken: {elapsed_time:.2f} seconds.\n")

    print(f"Total time taken: {elapsed_time:.2f} seconds.")
    print(f"Verification results saved in: {log_file_path}")

if __name__ == "__main__":
    main()
