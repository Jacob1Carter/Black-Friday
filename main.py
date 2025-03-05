from tools import backup_project
import launcher
import server
import client

def main():
    launch_settings = launcher.main()
    if not launch_settings:
        exit("Launch settings not provided.")
    
    if launch_settings["mode"] == "join":
        client.main(launch_settings["username"], launch_settings["ip"], launch_settings["port"])
    elif launch_settings["mode"] == "host":
        server.main(int(launch_settings["port"]))
    elif launch_settings["mode"] == "all":
        server.main(int(launch_settings["port"]))
        client.main(launch_settings["username"], launch_settings["ip"], launch_settings["port"])
    else:
        exit("Invalid data provided:\n" + str(launch_settings))


if __name__ == "__main__":
    backup_project()
    main()
