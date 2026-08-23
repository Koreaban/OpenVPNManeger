import os
import sys
import json
import time
import subprocess
from getdata import getdata_inf
import threading
from system import get_vpn, scan_system

system = scan_system()

servers = {
    "ca": ["ca1", "ca2", "ca3"],
    "ch": ["ch1", "ch2", "ch3"],
    "jp": ["jp1", "jp2", "jp3", "jp4", "jp5", "jp6", "jp7", "jp8"],
    "mx": ["mx1", "mx2", "mx3"],
    "nl": ["nl1", "nl2", "nl3"],
    "no": ["no1", "no2"],
    "sg": ["sg1", "sg2", "sg3"],
    "us": ["us1", "us2", "us3"]
}

def read_vpn_output(process,connected):
    for line in process.stdout:
        if "Initialization Sequence Completed" in line:
            connected.set()
            return

def closevpn(process):
    process.terminate()
    process.wait()
    print("Connection is close")

def connect_vpn():

    print("""
Available country
Enter one of the following country codes:

ca   - Canada
ch   - Switzerland
jp   - Japan
mx   - Mexico
nl  - Netherlands
no   - Norway
sg   - Singapore
us   - United States

Example: nl
""")

    while True:
        try:
            country = input("Choose country: ").strip().lower()
            
            if country in servers:
                break
            else:
                print("This country does not exist. Try again!")
                
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()
            
    while True:
        try:
            print(f"Available servers in {country}:")
            print(servers[country])
            
            server = input("Choose server: ").strip().lower()
        
            if server in servers[country]:
                break
            else:
                print("This server does not exist. Try again!")
                
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()        
                
    config_file = f"Vpn base/{server}.ovpn"
    auth_file = "openvpnkey.txt"

    vpn_command = get_vpn(config_file, auth_file)
    if vpn_command is None:
        print("Unsupported operating system.")
        return

    creationflags = subprocess.CREATE_NO_WINDOW if system == "Windows" else 0      

    process = subprocess.Popen(
        vpn_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=creationflags
    )
    
    connected = threading.Event()
    
    conn_for_json = None
    
    thread = threading.Thread(
        target=read_vpn_output,
        args=(process, connected)
    )
    
    thread.start()
    
    if connected.wait(timeout=30):
        conn_for_json = "Success"
        print("Your connection is successful!")
        time.sleep(2)  # Wait for a moment to ensure the connection is stable

        while True:
            print("To check the connection you can view your IP, just enter '4' ")
            try:
                check = input("Enter the '0' for stop or '4' for check: ").strip()

                if check == "4":
                    ip, country, latency, ping = getdata_inf()
                    latency = round(latency, 2) if latency else 0
                    ping = round(ping, 2) if ping is not None else 0
                    print(f"""

====================================================
          Your IP, Country and Ping now
====================================================
Your IP: {ip}
Your Country: {country}
HTTP Latency: {latency}
Ping: {ping}ms
""")
                elif check == "0":
                    closevpn(process)
                    break
            except ValueError:
                print("Pls just '4' or '0'") 
    else:
        conn_for_json = "Failed"
        print("VPN connection failed!")
        closevpn(process)

    last_server = {
           "Server": server,
           "Time": time.strftime("%Y-%m-%d %H:%M:%S"),
           "Status": conn_for_json,
    }
        
    with open("last_server.json", "w") as file:
        json.dump(last_server, file, indent=4)

    if os.path.exists("history.json"):
        try:
            with open("history.json", "r") as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
    else:
        history = []

    history.append({
           "Server": server,
           "Time": time.strftime("%Y-%m-%d %H:%M:%S"),
           "Status": conn_for_json,
    })



    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)


    return last_server, process
