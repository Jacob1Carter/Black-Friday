import subprocess

def rule_exists(rule_name):
    command = f'netsh advfirewall firewall show rule name="{rule_name}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "No rules match the specified criteria" not in result.stdout

def add_firewall_rule():
    rule_name = "Allow UDP 5011"
    protocol = "UDP"
    port = "5011"
    direction = "in"
    action = "allow"

    if rule_exists(rule_name):
        fprint(f"Firewall rule '{rule_name}' already exists.")
    else:
        command = f'netsh advfirewall firewall add rule name="{rule_name}" protocol={protocol} dir={direction} localport={port} action={action}'
        subprocess.run(command, shell=True)
        fprint(f"Firewall rule '{rule_name}' added successfully.")

if __name__ == "__main__":
    add_firewall_rule()