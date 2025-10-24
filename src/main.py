# main.py
import sys
from firewall.admin import is_admin, relaunch_as_admin_and_wait
from firewall.core import check_firewall_status, enable_firewall, disable_firewall
from utils.ui import handle_add_program, handle_open_port, handle_delete_rule

def main_menu():
    """Display interactive firewall control menu."""
    if sys.platform != "win32":
        print("This tool is for Windows only.")
        return

    while True:
        admin_status = " (Administrator)" if is_admin() else " (Not Administrator)"
        print(f"\n{'='*25} Firewall Control Menu {admin_status} {'='*25}")
        print("1. Check Firewall Status")
        print("2. Disable Firewall (All Profiles)")
        print("3. Enable Firewall (All Profiles)")
        print("--- Rule Management (Requires Admin) ---")
        print("5. Allow a Program (Inbound)")
        print("6. Open a Port (Inbound)")
        print("7. Delete a Rule (by name)")
        print("9. Exit")
        print("="*70)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            check_firewall_status()

        elif choice in ['2', '3', '5', '6', '7']:
            if relaunch_as_admin_and_wait():
                if choice == '2':
                    disable_firewall()
                elif choice == '3':
                    enable_firewall()
                elif choice == '5':
                    handle_add_program()
                elif choice == '6':
                    handle_open_port()
                elif choice == '7':
                    handle_delete_rule()

        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()