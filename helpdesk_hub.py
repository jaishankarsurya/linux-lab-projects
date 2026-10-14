import sqlite3
import sys

def init_db():
    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            category TEXT,
            priority TEXT,
            resolution TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def show_kb():
    kb = {
        "printer": "1. Check physical connections.\n2. Restart Print Spooler service.\n3. Clear print queue in C:\\Windows\\System32\\spool\\printers.\n4. Re-add network driver.",
        "vpn": "1. Verify internet connection.\n2. Check credentials / MFA prompt.\n3. Flush DNS (ipconfig /flushdns).\n4. Reinstall VPN client tunnel adapter."
    }
    print("\n--- KNOWLEDGE BASE ---")
    for key, steps in kb.items():
        print(f"\n[Issue: {key.upper()}]\n{steps}")

def create_ticket():
    print("\n--- LOG NEW TICKET ---")
    user = input("User email/ID: ")
    category = input("Category (Printer/VPN/Hardware/Software): ")
    priority = input("Priority (Low/Medium/High/Urgent): ")
    resolution = input("Resolution steps taken: ")

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (user, category, priority, resolution) VALUES (?, ?, ?, ?)",
                   (user, category, priority, resolution))
    conn.commit()
    conn.close()
    print("Ticket successfully logged to database!")

if __name__ == "__main__":
    init_db()
    while True:
        print("\n1. View Knowledge Base\n2. Log Support Ticket\n3. Exit")
        choice = input("Select an option (1-3): ")
        if choice == "1":
            show_kb()
        elif choice == "2":
            create_ticket()
        elif choice == "3":
            sys.exit()
        else:
            print("Invalid choice. Try again.")
