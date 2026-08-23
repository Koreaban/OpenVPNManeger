import subprocess
import time
import sys
import threading

from system import scan_system, get_vpn
from getdata import getdata_inf

servers = {
    "ca": ["ca1", "ca2", "ca3", "ca4", "ca5", "ca6"],
    "ch": ["ch1", "ch2"],
    "jp": ["jp1", "jp2", "jp3", "jp4", "jp5", "jp6", "jp7", "jp8"],
    "mx": ["mx1", "mx2", "mx3", "mx4"],
    "nl": ["nl1", "nl2", "nl3", "nl4", "nl5", "nl6"],
    "no": ["no1", "no2"],
    "sg": ["sg1", "sg2", "sg3", "sg4", "sg5", "sg6"],
    "us": ["us1", "us2", "us3", "us4", "us5", "us6"]
}

system = scan_system()

def closevpn(process):
    process.terminate()
    process.wait()
    print("Connection is close")

def read_vpn_output(process,connected):
    for line in process.stdout:
        if "Initialization Sequence Completed" in line:
            connected.set()
            return
        
def fastping():
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
    ping = None
    while True:
        try:
            country = input("Enter: ").strip().lower()  

            if country in servers:
                break
            else:
                print("This country does not exist. Try again!")
                
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()
        
    ping_results = {}

    print(f"All servers from this country will be checked")
    for server in servers[country]:
        print(f"Checking {server}...")

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
        thread = threading.Thread(
                target=read_vpn_output,
                args=(process, connected)
            )
        
        thread.start()

        if connected.wait(timeout=30):
            print(f"{server} is connected!")
            time.sleep(2)  # Wait for a moment to ensure the connection is stable
            ip, country, latency, ping = getdata_inf()

            ping_results[server] = ping

            print(f"{server}: {ping}ms")
        else:
            print(f"{server} is failed")
            ping_results[server] = None
            closevpn(process)

        process.terminate()
        process.wait()

    valid_vpn = {
        server: ping
        for server, ping in ping_results.items()
        if ping is not None
    }

    if valid_vpn:
        fastest_vpn = min(valid_vpn, key=valid_vpn.get)

        print(f"""
====================================================
              Fastest Server
====================================================

Server: {fastest_vpn}
Ping:   {valid_vpn[fastest_vpn]:.2f} ms

====================================================
""")
    else:
         print("No servers available.")
