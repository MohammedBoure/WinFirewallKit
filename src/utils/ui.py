# utils/ui.py
import os
from firewall.rules import add_program_rule, add_port_rule, delete_rule

def input_valid_path(prompt: str) -> str | None:
    """Prompt user for a file path and validate existence (optional continue)."""
    path = input(prompt).strip('"\' ')
    if os.path.exists(path):
        return path
    print(f"Warning: File not found: {path}")
    if input("Continue anyway? (y/n): ").lower() != 'y':
        return None
    return path

def handle_add_program():
    """Interactive: Add program to firewall allow list."""
    print("\n--- Allow a Program (Inbound) ---")
    rule_name = input("Enter rule name (e.g., MyApp): ").strip()
    if not rule_name:
        print("Rule name required.")
        return

    program_path = input_valid_path("Full path to .exe (e.g., C:\\App\\app.exe): ")
    if program_path:
        add_program_rule(rule_name, program_path)

def handle_open_port():
    """Interactive: Open a port in firewall."""
    print("\n--- Open a Port (Inbound) ---")
    rule_name = input("Enter rule name (e.g., Web Server): ").strip()
    if not rule_name:
        print("Rule name required.")
        return

    port = input("Port number (e.g., 8080): ").strip()
    if not port.isdigit():
        print("Invalid port number.")
        return

    proto = input("Protocol (TCP/UDP) [default: TCP]: ").strip().upper()
    if proto not in ["TCP", "UDP"]:
        proto = "TCP"
        print("Using TCP by default.")

    add_port_rule(rule_name, port, proto)

def handle_delete_rule():
    """Interactive: Delete a firewall rule."""
    print("\n--- Delete a Firewall Rule ---")
    rule_name = input("Enter exact rule name to delete: ").strip()
    if rule_name:
        delete_rule(rule_name)