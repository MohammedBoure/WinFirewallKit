# firewall/core.py
import subprocess
import sys
from typing import List
from .admin import is_admin

NETSH_CMD = "netsh"
DISABLE_COMMAND = [NETSH_CMD, "advfirewall", "set", "allprofiles", "state", "off"]
ENABLE_COMMAND = [NETSH_CMD, "advfirewall", "set", "allprofiles", "state", "on"]
STATUS_COMMAND = [NETSH_CMD, "advfirewall", "show", "allprofiles", "state"]

def run_netsh_command(command: List[str], action_name: str, require_admin: bool = True) -> bool:
    """Execute a netsh command with error handling and admin check."""
    if require_admin and not is_admin():
        print(f"\nFailed: '{action_name}' requires Administrator privileges.")
        return False

    print(f"\nExecuting: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding='utf8'
        )

        if result.returncode == 0:
            print(f"Success: {action_name}.")
            return True
        else:
            error = result.stderr.strip() or f"Exit code: {result.returncode}"
            print(f"Failed: {action_name}\n   {error}")
            return False
    except FileNotFoundError:
        print("netsh utility not found.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def enable_firewall() -> bool:
    """Enable Windows Defender Firewall for all profiles."""
    return run_netsh_command(ENABLE_COMMAND, "Firewall enabled")

def disable_firewall() -> bool:
    """Disable Windows Defender Firewall for all profiles."""
    return run_netsh_command(DISABLE_COMMAND, "Firewall disabled")

def check_firewall_status() -> None:
    """Display current firewall status for all profiles with correct profile names."""
    if sys.platform != "win32":
        print("This tool is for Windows only.")
        return

    print("Checking Windows Defender Firewall status...")
    try:
        result = subprocess.run(
            STATUS_COMMAND,
            capture_output=True,
            text=True,
            encoding='utf8',
            check=False
        )
    except FileNotFoundError:
        print("netsh.exe not found.")
        return

    if result.returncode != 0 and "No rules match" not in result.stderr:
        print("Could not retrieve firewall status. Try running as Administrator.")
        return

    output = result.stdout
    print("\n--- Firewall Status ---")

    current_profile = None
    profiles_found = 0

    for line in output.splitlines():
        line = line.strip()

        # Detect profile header
        if "Profile Settings:" in line:
            if "Domain" in line:
                current_profile = "Domain Profile"
            elif "Private" in line:
                current_profile = "Private Profile"
            elif "Public" in line:
                current_profile = "Public Profile"
            else:
                current_profile = line.split(" Settings:")[0] + " Profile"

        # Detect state line
        elif line.startswith("State") and current_profile:
            state_text = line.split("State")[1].strip()
            status = "Enabled" if state_text.upper() == "ON" else "Disabled" if state_text.upper() == "OFF" else "Unknown"
            print(f"- {current_profile}: {status}")
            profiles_found += 1
            current_profile = None  # Reset after printing

    if profiles_found == 0:
        print("No firewall profile status detected.")
    else:
        print("--------------------------")