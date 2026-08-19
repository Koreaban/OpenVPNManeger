import requests
import time
import subprocess
import re

def getdata_inf():

    ip = "Unknown"
    country = "Unknown"
    latency = None
    ping = None

    try:
        data = requests.get("http://ip-api.com/json").json()
        ip = data["query"]
        country = data["country"]
    except requests.RequestException:
        pass

    
    try:
        start = time.perf_counter()
        requests.get("https://one.one.one.one", timeout=2)
        end = time.perf_counter()
        
        latency = (end - start) * 1000
    except requests.RequestException:
        latency = None

    result = subprocess.run(
        ["ping", "-c", "2","-W", "2", "8.8.8.8"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        match = re.search(
            r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/",
            result.stdout
        )

        if match:
            ping = float(match.group(1))
        else:
            ping = None

    else:
        ping = None
    return ip, country, latency, ping
