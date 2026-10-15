import os
import time
import platform
from pathlib import Path

def get_target_directory():
    system = platform.system()
    if system == "Windows":
        # Target standard Windows user temp
        temp_path = os.environ.get("TEMP", r"C:\Windows\Temp")
    elif system == "Linux":
        temp_path = "/tmp"
    else:
        temp_path = "./mock_temp" # Fallback sandbox
        os.makedirs(temp_path, exist_ok=True)
    return Path(temp_path)

def clean_temp_files(days_old=30):
    target_dir = get_target_directory()
    print(f"[*] Scanning temporary directory: {target_dir}")
    
    now = time.time()
    cutoff_seconds = days_old * 86400  # seconds in a day
    
    total_bytes_freed = 0
    files_deleted = 0
    files_skipped = 0

    if not target_dir.exists():
        print(f"[-] Directory not found: {target_dir}")
        return

    for item in target_dir.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                file_age = now - item.stat().st_mtime
                if file_age > cutoff_seconds:
                    file_size = item.stat().st_size
                    item.unlink()
                    total_bytes_freed += file_size
                    files_deleted += 1
                else:
                    files_skipped += 1
            elif item.is_dir():
                # Skip subdirectories for safety unless specifically needed
                files_skipped += 1
        except PermissionError:
            # File is likely locked by an active process
            files_skipped += 1
        except Exception as e:
            files_skipped += 1

    mb_freed = total_bytes_freed / (1024 * 1024)
    print("\n--- CLEANUP SUMMARY ---")
    print(f"Files Deleted: {files_deleted}")
    print(f"Files Skipped/Locked: {files_skipped}")
    print(f"Total Space Recovered: {mb_freed:.2f} MB")

if __name__ == "__main__":
    # Set to clean files older than 30 days
    clean_temp_files(days_old=30)
