import argparse
import logging
import os
import platform
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass
from tqdm import tqdm
import xxhash

# ANSI escape codes for color output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

# Constants
class Constants:
    CHECKSUM_FILENAME = "checksums.txt"
    LOG_FILENAME = "organize_files.log"
    HASHES_FILENAME = "hashes.txt"
    CHUNK_SIZE = 8192
    DEFAULT_PARALLEL_JOBS = 4

@dataclass
class ProcessingStats:
    """Track file processing statistics"""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    total_bytes: int = 0
    start_time: float = 0.0

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time

    @property
    def transfer_rate(self) -> float:
        """Calculate transfer rate in MB/s"""
        if self.elapsed_time > 0:
            return (self.total_bytes / 1024 / 1024) / self.elapsed_time
        return 0.0

def setup_logging(log_file: Path, quiet: bool = False) -> logging.Logger:
    """Configure logging to both file and console"""
    handlers = [logging.FileHandler(log_file)]
    if not quiet:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    return logging.getLogger("file_organizer")

def get_args() -> argparse.Namespace:
    """Parse command-line arguments with enhanced options"""
    parser = argparse.ArgumentParser(
        description="Organize files by modification date and generate checksums.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--source", type=Path, help="Source directory path")
    parser.add_argument("--dest", type=Path, help="Destination directory path")
    parser.add_argument("--progress", action="store_true", help="Show progress bar")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run")
    parser.add_argument("--parallel-jobs", type=int, default=Constants.DEFAULT_PARALLEL_JOBS,
                      help="Number of parallel jobs")
    parser.add_argument("--file-type", nargs="+", help="Include specific file extensions")
    parser.add_argument("--min-size", type=int, help="Minimum file size in bytes")
    parser.add_argument("--max-size", type=int, help="Maximum file size in bytes")
    parser.add_argument("--skip-existing", action="store_true", 
                      help="Skip files that already exist in destination")
    return parser.parse_args()

def prompt_for_directory(prompt_text: str) -> Path:
    """Prompt for directory with improved path handling"""
    while True:
        try:
            dir_path = input(f"{prompt_text} (drag and drop or type path): ").strip()
            # Handle drag-and-drop paths
            dir_path = dir_path.strip('"').strip("'").encode("utf-8").decode("unicode_escape")
            path = Path(dir_path).resolve()
            if not path.exists():
                print(f"{Colors.YELLOW}Warning: Path does not exist. Create it? (y/n){Colors.RESET}")
                if input().lower() == 'y':
                    path.mkdir(parents=True)
                    return path
            elif path.is_dir():
                return path
            else:
                print(f"{Colors.RED}Path is not a directory: {path}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Invalid path: {e}{Colors.RESET}")

def compute_checksum(file_path: Path) -> str:
    """Compute xxhash3 checksum"""
    hash_func = xxhash.xxh3_64()
    with file_path.open("rb") as f:
        while chunk := f.read(Constants.CHUNK_SIZE):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_destination_path(file: Path, dest_dir: Path) -> tuple[Path, Path]:
    """Calculate destination folder and file path based on modification time"""
    mod_time = datetime.fromtimestamp(file.stat().st_mtime)
    subfolder = mod_time.strftime("%Y/%Y-%m-%d")
    dest_folder = dest_dir / subfolder
    dest_file = dest_folder / file.name
    return dest_folder, dest_file

def process_file(file: Path, dest_dir: Path, stats: ProcessingStats, config: Dict, logger: logging.Logger) -> bool:
    """Process a single file with enhanced error handling and logging"""
    try:
        dest_folder, dest_file = get_destination_path(file, dest_dir)
        if config['skip_existing'] and dest_file.exists() and dest_file.stat().st_size == file.stat().st_size:
            logger.debug(f"Skipping existing file: {file.name}")
            return True
        if not config['dry_run']:
            dest_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest_file)
            checksum = compute_checksum(dest_file)
            with open(dest_folder / Constants.CHECKSUM_FILENAME, "a") as f:
                f.write(f"{checksum}  {file.name}\n")
            with open(dest_dir / Constants.HASHES_FILENAME, "a") as hf:
                hf.write(f"{checksum}  {dest_file.relative_to(dest_dir)}\n")
            stats.total_bytes += file.stat().st_size
        stats.successful += 1
        logger.debug(f"Processed: {file.name}")
        return True
    except Exception as e:
        stats.failed += 1
        logger.error(f"Error processing {file.name}: {e}")
        return False

def process_files_with_progress(files: List[Path], dest_dir: Path, stats: ProcessingStats, config: Dict, logger: logging.Logger, show_progress: bool) -> None:
    """Process files with optional progress bar"""
    with ThreadPoolExecutor(max_workers=config['parallel_jobs']) as executor:
        futures = {executor.submit(process_file, f, dest_dir, stats, config, logger): f for f in files}
        if show_progress:
            with tqdm(total=len(files), unit='files', desc='Processing') as pbar:
                for future in as_completed(futures):
                    future.result()
                    pbar.update(1)
                    pbar.set_postfix({'rate (MB/s)': f"{stats.transfer_rate:.2f}"})
        else:
            for future in as_completed(futures):
                future.result()

def main() -> None:
    """Enhanced main function with better error handling and reporting"""
    args = get_args()
    src_dir = args.source or prompt_for_directory("Source directory")
    dest_dir = args.dest or prompt_for_directory("Destination directory")
    log_file = dest_dir / Constants.LOG_FILENAME
    logger = setup_logging(log_file, quiet=args.progress)
    stats = ProcessingStats(start_time=time.time())
    config = {
        'dry_run': args.dry_run,
        'skip_existing': args.skip_existing,
        'file_type': {ft.lower() for ft in args.file_type} if args.file_type else None,
        'min_size': args.min_size,
        'max_size': args.max_size,
        'parallel_jobs': args.parallel_jobs
    }
    try:
        if not args.dry_run:
            with open(dest_dir / Constants.HASHES_FILENAME, "w") as hf:
                hf.write("Global Hashes for All Files:\n---\n")
        logger.info("Scanning for files...")
        files = [f for f in src_dir.rglob("*") if f.is_file()]
        files = [
            f for f in files
            if (not config.get('file_type') or f.suffix.lower() in config['file_type'])
            and (not config.get('min_size') or f.stat().st_size >= config['min_size'])
            and (not config.get('max_size') or f.stat().st_size <= config['max_size'])
        ]
        stats.total_files = len(files)
        logger.info(f"Found {stats.total_files} files to process")
        process_files_with_progress(files, dest_dir, stats, config, logger, args.progress)
        logger.info("\nProcessing Summary:")
        logger.info(f"Total files: {stats.total_files}")
        logger.info(f"Successful: {stats.successful}")
        logger.info(f"Failed: {stats.failed}")
        logger.info(f"Total time: {stats.elapsed_time:.2f} seconds")
        logger.info(f"Transfer rate: {stats.transfer_rate:.2f} MB/s")
        if not args.progress:
            print(f"Total time: {stats.elapsed_time:.2f} seconds")
            print(f"Transfer rate: {stats.transfer_rate:.2f} MB/s")
    except KeyboardInterrupt:
        logger.warning("\nProcessing interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
