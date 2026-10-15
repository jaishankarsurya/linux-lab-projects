import re
import collections 
import csv
import os 

SAMPLE_LOG_DATA = """
Oct 15 06:12:01 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54321 ssh2
Oct 15 06:12:03 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54322 ssh2
Oct 15 06:12:05 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54323 ssh2
Oct 15 06:12:07 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54324 ssh2
Oct 15 06:12:09 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54325 ssh2
Oct 15 06:12:11 server sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54326 ssh2
Oct 15 06:15:20 server sshd[1289]: Accepted password for root from 10.0.0.5 port 12345 ssh2
Oct 15 06:18:01 server sshd[1350]: Failed password for root from 203.0.113.42 port 43211 ssh2
Oct 15 06:18:04 server sshd[1350]: Failed password for root from 203.0.113.42 port 43212 ssh2
"""

def create_sample_log():
    if not os.path.exists("auth.log"):
        with open("auth.log", "w") as f:
        	f.write(SAMPLE_LOG_DATA.strip())

def analyze_logs(log_file="auth.log", threshold=3):
    create_sample_log()
    ip_pattern = re.compile(r'from\s+(\d{1,3}(?:\.\d{1,3}){3})')
    failed_attempts = collections.Counter()

    print(f"[*] Parsing log file: {log_file}")
    with open(log_file, "r") as f:
        for line in f:
            if "Failed password" in line or "Failed login" in line:
                match = ip_pattern.search(line)
                if match:
                    ip = match.group(1)
                    failed_attempts[ip] += 1

    print("\n--- AUTHENTICATION FAILURE REPORT ---")
    print(f"{'Source IP':<18} | {'Failed Attempts':<15} | {'Status':<15}")
    print("-" * 54)

    alerts = []
    for ip, count in failed_attempts.items():
        status = "SUSPICIOUS (Brute-Force)" if count >= threshold else "Normal"
        if count >= threshold:
            alerts.append((ip, count))
        print(f"{ip:<18} | {count:<15} | {status}")

    # Export report
    with open("security_audit_report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP Address", "Failed Count", "Flagged Status"])
        for ip, count in failed_attempts.items():
            status = "Flagged" if count >= threshold else "OK"
            writer.writerow([ip, count, status])

    print(f"\n[+] Audit complete. Flagged {len(alerts)} potential threat source(s). Report saved.")

if __name__ == "__main__":
    analyze_logs(threshold=3)
