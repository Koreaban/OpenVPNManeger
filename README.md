# VPN Manager

VPN Manager is a VPN connection manager based on **OpenVPN**. It uses OpenVPN configuration files from **Proton VPN** and allows users to easily connect to available VPN servers.

> **Platform:** The current version is available for **Linux only**. A **Windows version is planned** and will be added in the future.

## Features

* Connect to Proton VPN OpenVPN servers.
* Choose a VPN server manually.
* Select a country and find the **fastest available server** in that country.
* Check which VPN server was used for the **last connection**.
* Check the current **public IP address**.
* Manage and use OpenVPN configuration files.

## OpenVPN Credentials

To connect to Proton VPN servers, the application requires **OpenVPN credentials**.

The credentials should be stored in an `openvpn.key` file located in the folder containing the OpenVPN configuration files.

Example:

```text
USERNAME=your_openvpn_username
PASSWORD=your_openvpn_password
```

> **Security warning:** `openvpn.key` contains authentication credentials and must **never** be uploaded to a public repository.

For GitHub, use a template file containing placeholder values instead of real credentials, and add the actual `openvpn.key` file to `.gitignore`.

## How It Works

1. The manager loads the available OpenVPN configuration files.
2. The user selects a country or a specific server.
3. The manager uses the corresponding OpenVPN configuration.
4. Authentication credentials are loaded from `openvpn.key`.
5. The application establishes the VPN connection.
6. The manager can check the current public IP and save information about the last connected server.

## Requirements

* Linux
* OpenVPN
* Proton VPN OpenVPN configuration files
* Proton VPN OpenVPN credentials
* Python dependencies required by the project

## Roadmap

* [x] Linux support
* [ ] Windows support
* [ ] Additional improvements and features
