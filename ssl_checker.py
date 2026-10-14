import ssl
import socket
import datetime
import csv
import os

DOMAINS_TO_CHECK = [
    "google.com",
    "github.com",
    "stackoverflow.com",
    "expired.badssl.com"  # Useful for testing warning/expired states
]

def get_certificate_expiry(domain, port=443):
    context = ssl.create_default_context()
    conn = socket.create_connection((domain, port), timeout=5)
    try:
        with context.wrap_socket(conn, server_hostname=domain) as s:
            cert = s.getpeercert()
            # 'notAfter' format: 'May 17 23:59:59 2027 GMT'
            date_str = cert.get('notAfter')
            expiry_date = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
            days_remaining = (expiry_date - datetime.datetime.utcnow()).days
            return expiry_date, days_remaining, "Valid"
    except Exception as e:
        return None, 0, f"Error: {str(e)}"

def run_ssl_audit():
    report_file = "ssl_audit_report.csv"
    print(f"{'Domain':<25} | {'Days Remaining':<15} | {'Status':<10}")
    print("-" * 60)

    with open(report_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "Expiry Date (UTC)", "Days Remaining", "Status"])

        for domain in DOMAINS_TO_CHECK:
            expiry, days, status = get_certificate_expiry(domain)
            if "Error" in status:
                print(f"{domain:<25} | {'N/A':<15} | {status}")
                writer.writerow([domain, "N/A", 0, status])
            else:
                warning_label = "OK"
                if days < 14:
                    warning_label = "CRITICAL"
                elif days < 30:
                    warning_label = "WARNING"

                print(f"{domain:<25} | {days:<15} | {warning_label}")
                writer.writerow([domain, expiry.strftime("%Y-%m-%d"), days, warning_label])

    print(f"\nAudit complete. Report saved to {report_file}")

if __name__ == "__main__":
    run_ssl_audit()
