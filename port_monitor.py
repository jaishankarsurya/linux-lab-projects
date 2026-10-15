import socket
import sys

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3389: "RDP",
    5432: "PostgreSQL"
}

def check_port(host, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False

def run_port_scan(target_host):
    print(f"[*] Scanning target: {target_host}\n")
    print(f"{'Port':<8} | {'Service':<15} | {'Status':<10}")
    print("-" * 40)

    for port, service in COMMON_PORTS.items():
        is_open = check_port(target_host, port)
        status = "[OPEN]" if is_open else "[CLOSED]"
        print(f"{port:<8} | {service:<15} | {status}")

if __name__ == "__main__":
    # Default to localhost if no argument is passed
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    run_port_scan(target)
