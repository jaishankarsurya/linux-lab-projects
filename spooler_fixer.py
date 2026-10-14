import platform
import subprocess
import os
import shutil

def clear_windows_spooler():
    print("[*] Stopping Print Spooler service...")
    subprocess.run(["net", "stop", "spooler"], capture_output=True, text=True)

    spool_dir = r"C:\Windows\System32\spool\PRINTERS"
    if os.path.exists(spool_dir):
        print(f"[*] Clearing stuck jobs from {spool_dir}...")
        count = 0
        for item in os.listdir(spool_dir):
            item_path = os.path.join(spool_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    count += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    count += 1
            except Exception as e:
                print(f"    [!] Could not delete {item}: {e}")
        print(f"[*] Cleared {count} item(s) from print queue.")

    print("[*] Starting Print Spooler service...")
    subprocess.run(["net", "start", "spooler"], capture_output=True, text=True)
    print("[+] Windows Print Spooler reset complete.")

def clear_linux_cups():
    print("[*] Restarting CUPS print service...")
    result = subprocess.run(["sudo", "systemctl", "restart", "cups"], capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] Linux CUPS service restarted successfully.")
    else:
        print(f"[-] Failed to restart CUPS. Ensure you have sudo privileges.\nStderr: {result.stderr}")

if __name__ == "__main__":
    current_os = platform.system()
    if current_os == "Windows":
        clear_windows_spooler()
    elif current_os == "Linux":
        clear_linux_cups()
    else:
        print(f"[-] Unsupported OS for print service recovery: {current_os}")
