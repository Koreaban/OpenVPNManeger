import json
import subprocess
import platform

from getdata import getdata_inf
from connect import connect_vpn
from fast_ping import fastping

countries = {
    "ca": "Canada",
    "ch": "Switzerland",
    "jp": "Japan",
    "mx": "Mexico",
    "nl": "Netherlands",
    "no": "Norway",
    "sg": "Singapore",
    "us": "United States"
}

def choice():
    wellcome = f"""
====================================================
              OpenVPN Manager v1.0
====================================================

[1] Connect VPN
[2] Last connected server
[3] Fastest server
[4] Check public IP
[5] End VPN connection
[0] Exit
"""  
    while True:            
        print(wellcome)
        try:
            option = int(input("Enter number: "))

            if option not in (0, 1, 2, 3, 4, 5):
                print("Invalid option. Choose 0, 1, 2, 3, 4 or 5.")
                continue

            if option == 1:
                connect_vpn()
                continue
                
            elif option  == 2:
                try:
                    with open("last_server.json", "r") as file:
                        data = json.load(file)
                        server = data["Server"]
                        
                        country_code = server[:2]
                        country = countries.get(country_code, "Unknown")
                     
                    print(f"""
====================================================
             Last Connected Server
====================================================

    Server : {server}
    Country: {country}
    Time   : {data["Time"]}
    Status : {data["Status"]}

====================================================
""")   
                except FileNotFoundError:
                    print("No connection history yet.")
                    continue

            elif option == 3:
                fastping()
                continue
            elif option == 4:
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
                continue

            elif option == 5:
                system = platform.system()
                try:
                    if system == "Windows":
                        check = subprocess.run(
                            ["tasklist", "/F", "/IM", "openvpn.exe"],
                            text=True,
                            capture_output=True
                        )
                        is_running = "openvpn.exe" in check.stdout
                    elif system == "Linux":
                        check = subprocess.run(
                            ["pgrep", "openvpn"],
                            text=True,
                            capture_output=True
                        )
                        is_running = check.returncode == 0
                    else:
                        is_running = False
                    if not is_running:
                        print("No VPN connection found.")
                    else:
                        if system == "Windows":
                            subprocess.run(
                                ["taskkill", "/F", "/IM", "openvpn.exe"],
                                capture_output=True
                            )
                            print("VPN connection ended.")
                        elif system == "Linux":
                            subprocess.run(
                                ["sudo", "pkill", "openvpn"],
                                capture_output=True
                            )
                            print("VPN connection ended.")
                except Exception as e:
                    print(f"Could not stop VPN: {e}")
                continue
            elif option ==0:
                print("Bye!")
                break
        except KeyboardInterrupt:
            print("Bye!")
            break
            
        except ValueError:
            print("Please try again")
