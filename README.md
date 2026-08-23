# VPN Manager

VPN Manager is a VPN connection manager based on **OpenVPN**. It uses OpenVPN configuration files from **Proton VPN** and allows users to easily connect to available VPN servers, check connection speed, and manage the connection from a simple console menu.

> **Platform:** Supports both **Windows** and **Linux**.

## Features

* Connect to Proton VPN OpenVPN servers.
* Choose a country and a specific server manually.
* Find the **fastest available server** in a country by testing all of them.
* Check which VPN server was used for the **last connection** (with status and timestamp).
* Check the current **public IP address**, country, HTTP latency, and ping.
* Stop an active VPN connection at any time from the main menu.
* Automatically save connection history to `history.json`.

## Requirements

Before using VPN Manager, make sure you have:

* Windows or Linux
* Python 3
* [`requests`](https://pypi.org/project/requests/) Python package
* **OpenVPN installed** on your system
* A Proton VPN account
* Proton VPN OpenVPN configuration files
* Proton VPN OpenVPN credentials

### Installing OpenVPN

**Linux (Debian/Ubuntu-based):**

```bash
sudo apt update
sudo apt install openvpn
```

Verify the installation with:

```bash
openvpn --version
```

**Windows:**

Download and install OpenVPN from the [official website](https://openvpn.net/community-downloads/). The application expects OpenVPN to be installed at the default path:

```
C:\Program Files\OpenVPN\bin\openvpn.exe
```

### Installing Python dependencies

```bash
pip install requests
```

## Getting Started

Before using VPN Manager, you need a **Proton VPN account**.

1. Create an account on Proton VPN.
2. Log in to your Proton VPN account.
3. Obtain your **OpenVPN username and password** from your Proton VPN account (Account → OpenVPN / IKEv2 credentials).
4. Download the required Proton VPN **OpenVPN configuration files** (`.ovpn`).
5. Place the configuration files in a folder named `Vpn base/` in the project directory (e.g. `Vpn base/nl1.ovpn`).
6. Create an `openvpnkey.txt` file in the project directory with your OpenVPN credentials (see format below).

> **Important:** The OpenVPN username and password are **not** the same as your regular Proton account login. Use the dedicated **OpenVPN / IKEv2 credentials** provided by Proton VPN.

## OpenVPN Credentials

The application requires an `openvpnkey.txt` file in the project directory, containing your OpenVPN username and password on separate lines:

```text
your_openvpn_username
your_openvpn_password
```

> **Security warning:** `openvpnkey.txt` contains authentication credentials and must **never** be uploaded to a public repository. This file (along with `Vpn base/`, `history.json`, and `last_server.json`) is already excluded via `.gitignore`.

## Running the Manager

Open a terminal and navigate to the project directory:

```bash
cd /path/to/VPN-Manager
```

**Linux:** OpenVPN requires root privileges, so run the script with `sudo`:

```bash
sudo python3 init.py
```

**Windows:** OpenVPN requires administrator privileges to create the TAP network adapter. Open a terminal (PowerShell or CMD) **as Administrator**, then run:

```powershell
python3 init.py
```

## Menu Options

```
[1] Connect VPN            - Choose a country and server, then connect
[2] Last connected server  - View details of your most recent connection
[3] Fastest server         - Test all servers in a country and find the fastest one
[4] Check public IP        - View your current public IP, country, latency, and ping
[5] End VPN connection     - Stop the currently active VPN connection
[0] Exit                   - Quit the application
```

## How It Works

1. The manager loads the available OpenVPN configuration files from `Vpn base/`.
2. The user selects a country or a specific server from the menu.
3. The manager builds the appropriate OpenVPN command for your operating system.
4. Authentication credentials are loaded from `openvpnkey.txt`.
5. The application establishes the VPN connection through the locally installed OpenVPN client.
6. The manager can check the current public IP, measure latency/ping, and save connection history to `history.json` and `last_server.json`.
7. The connection can be stopped at any time via option `[5]`, which safely terminates the OpenVPN process.

## Known Limitations

* Ping/latency measurement on Windows depends on the system's locale for parsing `ping` output; this is handled automatically but may vary slightly across Windows language editions.
* Option `[5]` stops **all** running OpenVPN processes on the system by name — if you have other OpenVPN connections running outside this app, they will also be stopped.

## Roadmap

* [x] Linux support
* [x] Windows support
* [ ] Additional improvements and features (e.g. per-connection process tracking, config auto-detection)
