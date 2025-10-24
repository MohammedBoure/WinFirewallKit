# firewall/admin.py
import ctypes
import sys
import os

def is_admin() -> bool:
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def relaunch_as_admin_and_wait() -> bool:
    """Relaunch the script with elevated privileges and exit the current process."""
    if is_admin():
        return True

    print("Requesting Administrator privileges (UAC)...")
    python_exe = sys.executable
    script = os.path.abspath(sys.argv[0])
    params = f'"{script}"'
    if len(sys.argv) > 1:
        params += " " + " ".join(f'"{a}"' for a in sys.argv[1:])

    try:
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, params, None, 1)
        if int(ret) <= 32:
            print("Failed to start elevated process.")
            input("Press Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"Error requesting elevation: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    print("Elevated process started. Please approve the UAC prompt.")
    sys.exit(0)