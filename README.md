# Windows Firewall Control Library – Usage Guide

This is a **powerful, reusable Python library** for controlling **Windows Defender Firewall** programmatically. It allows you to manage firewall status, add/remove rules, and automate network security configurations — **without manual GUI interaction**.

---

## What Is This Library For?

| Feature | Benefit |
|-------|--------|
| **Enable/Disable Firewall** | Turn on/off firewall for all profiles (Domain, Private, Public) |
| **Check Firewall Status** | Get real-time status of each profile |
| **Allow Programs** | Automatically allow `.exe` files through the firewall |
| **Open Ports (TCP/UDP)** | Open specific ports for servers or apps |
| **Delete Rules** | Remove outdated or conflicting rules |
| **Admin Elevation** | Auto-relaunch script with UAC if needed |

**Use Cases:**
- Automate server setup scripts
- Configure firewalls during software installation
- Create deployment tools for IT teams
- Build custom security dashboards

---

## Folder Structure (Required)

```
your-project/
├── main.py
├── firewall/
│   ├── __init__.py
│   ├── admin.py
│   ├── core.py
│   └── rules.py
└── utils/
    └── ui.py
```

> All files must be in this exact structure for imports to work.

---

## How to Use the Library (Code Examples)

### 1. Import the Library

```python
from firewall import (
    is_admin, relaunch_as_admin_and_wait,
    enable_firewall, disable_firewall, check_firewall_status,
    add_program_rule, add_port_rule, delete_rule
)
```

---

### 2. Check Firewall Status

```python
check_firewall_status()
```

**Output Example:**
```
--- Firewall Status ---
- Domain Profile: Enabled
- Private Profile: Disabled
- Public Profile: Enabled
--------------------------
```

---

### 3. Enable or Disable Firewall

```python
# Enable all profiles
enable_firewall()

# Disable all profiles
disable_firewall()
```

---

### 4. Allow a Program (Inbound)

```python
success = add_program_rule(
    rule_name="MyGame",
    program_path=r"C:\Games\MyGame.exe",
    direction="in",
    action="allow"
)

if success:
    print("Game allowed through firewall!")
```

---

### 5. Open a Port (TCP or UDP)

```python
# Open port 8080 TCP
add_port_rule("WebServer", "8080", protocol="TCP")

# Open port 5000 UDP
add_port_rule("GameServer", "5000", protocol="UDP", action="allow")
```

---

### 6. Delete a Rule by Name

```python
delete_rule("OldRuleName")
```

---

### 7. Auto-Relaunch as Admin (Critical!)

Always wrap admin actions with this:

```python
if not is_admin():
    print("Need admin rights...")
    relaunch_as_admin_and_wait()  # Exits current process, relaunches elevated
    exit()

# Now safe to modify firewall
enable_firewall()
```

---

## Full Example Script (Standalone)

```python
# auto_firewall_setup.py
from firewall import (
    is_admin, relaunch_as_admin_and_wait,
    enable_firewall, add_program_rule, add_port_rule
)

def setup_web_server():
    if not is_admin():
        print("Requesting admin privileges...")
        relaunch_as_admin_and_wait()
        return  # Script will restart

    print("Enabling firewall...")
    enable_firewall()

    print("Allowing web server...")
    add_program_rule("Apache", r"C:\Apache\bin\httpd.exe")

    print("Opening port 80...")
    add_port_rule("HTTP", "80", "TCP")

    print("Setup complete!")

if __name__ == "__main__":
    setup_web_server()
```

Run with:
```bash
python auto_firewall_setup.py
```

---

## Convert to `.exe` (No Python Needed)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build Executable
```bash
pyinstaller --onefile --name "FirewallSetup" auto_firewall_setup.py
```

### Output:
```
dist/FirewallSetup.exe
```

> Double-click to run — **no Python required!**

---

## Important Notes

| Warning | Details |
|-------|--------|
| **Admin Required** | Most functions need elevated privileges |
| **Windows Only** | Uses `netsh` — not available on Linux/macOS |
| **Rule Names Must Be Unique** | Duplicate names will fail |
| **Paths Must Be Exact** | Use full path like `C:\App\app.exe` |

---

## Error Handling (Built-in)

All functions return `True` / `False` and print clear messages:

```python
if not add_port_rule("Test", "9999"):
    print("Failed to open port!")
```

---

## Library Functions Summary

| Function | Description |
|--------|-----------|
| `is_admin()` | Check if running as admin |
| `relaunch_as_admin_and_wait()` | Restart script with UAC prompt |
| `check_firewall_status()` | Print status of all profiles |
| `enable_firewall()` | Turn on firewall |
| `disable_firewall()` | Turn off firewall |
| `add_program_rule(name, path, ...)` | Allow/block program |
| `add_port_rule(name, port, ...)` | Open/close port |
| `delete_rule(name)` | Remove rule by name |

---

## Pro Tip: Use in Installers

Include this in your app installer:

```python
# After installing your app
add_program_rule("MyApp", r"C:\MyApp\MyApp.exe")
add_port_rule("MyApp Server", "5000", "TCP")
```

Automate firewall setup — zero user clicks!

---

**You're now a Windows Firewall automation expert!**