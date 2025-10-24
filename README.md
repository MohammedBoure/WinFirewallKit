# WinFirewallKit – Windows Firewall Control Library

A **powerful, modular Python library** and **interactive CLI tool** for managing **Windows Defender Firewall** with full automation support.

---

## Features

- Enable / Disable firewall (all profiles)
- Check real-time firewall status (Domain, Private, Public)
- Allow programs through firewall
- Open/close TCP/UDP ports
- Delete firewall rules by name
- **Auto UAC elevation** – no manual admin needed
- Clean, reusable API for scripting

---

## Project Structure

```
winfirewallkit/
│
├── main.py                  # Interactive CLI entry point
├── firewall/
│   ├── __init__.py          # Exports core API
│   ├── admin.py             # Admin check & elevation
│   ├── core.py              # Enable/disable/status
│   └── rules.py             # Program & port rules
├── utils/
│   ├── __init__.py          # Exports UI handlers
│   └── ui.py                # Interactive prompts
└── README.md                # This file
```

> **`utils/__init__.py`** cleanly exports interactive handlers:  
> `handle_add_program`, `handle_open_port`, `handle_delete_rule`

---

## Requirements

| Requirement | Details |
|-----------|--------|
| **OS** | Windows 10 / 11 |
| **Python** | 3.6+ |
| **Permissions** | **Admin rights required** for rule changes |
| **netsh** | Built-in on Windows |

---

## How to Run (Interactive Mode)

```bash
python main.py
```

> If not admin, the script will **automatically relaunch with UAC prompt**.

---

## Interactive Menu

```
========================= Firewall Control Menu (Administrator) =========================
1. Check Firewall Status
2. Disable Firewall (All Profiles)
3. Enable Firewall (All Profiles)
--- Rule Management (Requires Admin) ---
5. Allow a Program (Inbound)
6. Open a Port (Inbound)
7. Delete a Rule (by name)
9. Exit
======================================================================
```

---

## Library Usage (Programmatic)

### Import Core Functions

```python
from firewall import (
    is_admin, relaunch_as_admin_and_wait,
    enable_firewall, disable_firewall, check_firewall_status,
    add_program_rule, add_port_rule, delete_rule
)
```

### Import UI Handlers (Interactive)

```python
from utils import handle_add_program, handle_open_port, handle_delete_rule
```

---

### Example: Auto-Setup Script

```python
# setup_server.py
from firewall import is_admin, relaunch_as_admin_and_wait, enable_firewall
from firewall.rules import add_program_rule, add_port_rule

if not is_admin():
    relaunch_as_admin_and_wait()
    exit()

enable_firewall()
add_program_rule("WebApp", r"C:\Apps\WebApp.exe")
add_port_rule("HTTP", "80", "TCP")
add_port_rule("HTTPS", "443", "TCP")

print("Firewall configured!")
```

---

## Build Standalone `.exe`

```bash
pip install pyinstaller
pyinstaller --onefile --name "FirewallSetup" main.py
```

Output: `dist/FirewallSetup.exe` – **No Python needed**

---

## API Reference

| Function | Description |
|--------|-----------|
| `check_firewall_status()` | Print status per profile |
| `enable_firewall()` | Turn on all profiles |
| `disable_firewall()` | Turn off all profiles |
| `add_program_rule(name, path, ...)` | Allow/block program |
| `add_port_rule(name, port, protocol, ...)` | Open/close port |
| `delete_rule(name)` | Remove rule |
| `is_admin()` | Check elevation |
| `relaunch_as_admin_and_wait()` | Auto-relaunch with UAC |

---

## Security Notes

- Disabling firewall reduces security
- Use only on trusted systems
- Always re-enable firewall after testing

---

## Project Name: **`WinFirewallKit`**

> **Recommended package name:** `winfirewallkit`  
> **PyPI:** `pip install winfirewallkit`

---

**Automate Windows Firewall like a pro.**