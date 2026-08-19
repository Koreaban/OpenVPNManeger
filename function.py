import json
from concurrent.futures import ThreadPoolExecutor
from getdata import getdata_inf
from connect import connect_vpn, closevpn
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
[0] Exit
"""  
    while True:            
        print(wellcome)
        try:
            option = int(input("Enter number: "))

            if option not in (0, 1, 2, 3, 4):
                print("Invalid option. Choose 0, 1, 2, 3 or 4.")
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
                latency = round(latency, 2)
                ping = round(ping, 2)
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

            elif option ==0:
                print("Bye!")
                break
        except KeyboardInterrupt:
            print("Bye!")
            break
            
        except ValueError:
            print("Please try again")
