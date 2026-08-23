import requests
import time
import subprocess
import re

from system import scan_system

def getdata_inf():

    ip = "Unknown"
    country = "Unknown"
    latency = None
    ping = None

    try:
        response = requests.get("http://ip-api.com/json", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            ip = data["query"]
            country = data["country"]
        else:
            ip = "Unknown"
            country = "Unknown"
    except requests.RequestException:
        pass

    
    try:
        start = time.perf_counter()
        requests.get("https://one.one.one.one", timeout=2)
        end = time.perf_counter()
        
        latency = (end - start) * 1000

    except requests.RequestException:
        latency = None

    system = scan_system()

    if system == "Windows":
        ping_command = ["ping", "-n", "2", "-w", "2000", "8.8.8.8"]
    elif system == "Linux":
        ping_command = ["ping", "-c", "2", "-W", "2", "8.8.8.8"]
    else:
        ping_command = None

    ping = None

    if ping_command:
        try:
            encoding = "cp866" if system == "Windows" else "utf-8"
            result = subprocess.run(
                ping_command,
                capture_output=True,
                text=True,
                encoding=encoding,
                errors="ignore"
            )
            if system == "Linux":
                match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/", result.stdout)
                if match:
                    ping = float(match.group(1))
            elif system == "Windows":
                times = re.findall(r"=(\d+)\s*(?:ms|мс)", result.stdout)
                if times:
                    ping = sum(float(t) for t in times) / len(times)  
        except (subprocess.CalledProcessError, FileNotFoundError):
            ping = None

    return ip, country, latency, ping
