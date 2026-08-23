import os
import platform

def scan_system():
    return platform.system()
    

def get_vpn(config_file, auth_file):
    system = scan_system()
    
    if system == "Linux":
        vpn_command = [
            "sudo",
            "openvpn",
            "--config", config_file,
            "--auth-user-pass", auth_file
        ]
    elif system == "Windows":
        openvpn = r"C:\Program Files\OpenVPN\bin\openvpn.exe"
        if not os.path.exists(openvpn):
            print("OpenVPN executable not found. Please install OpenVPN and ensure the path is correct.")
            return None
        vpn_command = [
            openvpn,
            "--config", config_file,
            "--auth-user-pass", auth_file
        ]
    else:
        print("Unsupported operating system.")
        return None
    return vpn_command