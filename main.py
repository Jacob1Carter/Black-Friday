import time
import launcher
import subprocess
import sys
from tools import fprint
fprint("main.py")

def main():
    launch_settings = launcher.main()
    if not launch_settings:
        exit("Launch settings not provided.")
    
    python_executable = sys.executable  # Get the current Python interpreter

    if launch_settings["mode"] == "join":
        subprocess.run([python_executable, "client.py", launch_settings["username"], launch_settings["ip"]])
    elif launch_settings["mode"] == "host":
        # subprocess.run(["firewall_rule.bat"])

        subprocess.run([python_executable, "server.py"])
    elif launch_settings["mode"] == "host_join":
        # subprocess.run(["firewall_rule.bat"])

        subprocess.Popen([python_executable, "server.py"])
        time.sleep(1)
        subprocess.run([python_executable, "client.py", launch_settings["username"], "localhost"])
    else:
        exit("Invalid data provided:\n" + str(launch_settings))

if __name__ == "__main__":
    main()


#
# a valuable contribution from the cat:
#
# ijg87uuuuuuuuuuuuuuuuuuuuu ybu-063wh
# ????????????????????????????????????????
# v cccccccccccccccccccccccccccccccccccccccccccccccccc
#
# well done cat, well done
#