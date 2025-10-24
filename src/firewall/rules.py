# firewall/rules.py
from typing import Literal
from .core import run_netsh_command, NETSH_CMD

Direction = Literal["in", "out"]
Action = Literal["allow", "block"]
Protocol = Literal["TCP", "UDP"]

def add_program_rule(rule_name: str, program_path: str, direction: Direction = "in", action: Action = "allow") -> bool:
    """Add a firewall rule to allow/block a program."""
    command = [
        NETSH_CMD, "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}",
        f"dir={direction}",
        f"action={action}",
        f'program="{program_path}"',
        "enable=yes"
    ]
    return run_netsh_command(command, f"Rule '{rule_name}' added")

def add_port_rule(rule_name: str, port: str, protocol: Protocol = "TCP", direction: Direction = "in", action: Action = "allow") -> bool:
    """Add a firewall rule to open/close a port."""
    command = [
        NETSH_CMD, "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}",
        f"dir={direction}",
        f"action={action}",
        f"protocol={protocol}",
        f"localport={port}",
        "enable=yes"
    ]
    return run_netsh_command(command, f"Port rule '{rule_name}' added")

def delete_rule(rule_name: str) -> bool:
    """Delete a firewall rule by name."""
    command = [
        NETSH_CMD, "advfirewall", "firewall", "delete", "rule",
        f"name={rule_name}"
    ]
    return run_netsh_command(command, f"Rule '{rule_name}' deleted")