import subprocess
import platform
import socket

def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except Exception:
        return False

def check_dns(domain="google.com"):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def run_diagnostics():
    print("Running IT Help Desk Network Diagnostics...\n")

    # 1. Check DNS
    dns_status = check_dns()
    print(f"[*] DNS Resolution (google.com): {'[PASS]' if dns_status else '[FAIL - Check DNS settings]'}")

    # 2. Check External Gateway / Public IP reachable (Google DNS)
    ext_status = ping_host("8.8.8.8")
    print(f"[*] Public Internet Ping (8.8.8.8): {'[PASS]' if ext_status else '[FAIL - Check local adapter/gateway]'}")

    # 3. Check Local Loopback
    loop_status = ping_host("127.0.0.1")
    print(f"[*] Network Stack (Loopback): {'[PASS]' if loop_status else '[FAIL - TCP/IP stack issue]'}")

    print("\nDiagnostics complete.")

if __name__ == "__main__":
    run_diagnostics()
