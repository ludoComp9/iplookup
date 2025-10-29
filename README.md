# IP Lookup

A small Python script to retrieve information from IP address(es) given in parameter.

# Purpose

Purpose of this very simple tool is to:
- get a reverse DNS lookup
- get IP information such as ASN, Organisation name, Network name, Country
- search FQDN from SubjectAlternativeName / Common Name values defined in TLS certificate from opened ports identified by nmap

Note: IP Lookup uses [pwhois](https://pwhois.org/) server to get information.

# Note

This tool has been successfully tested on:
- macOS 15.6/Python 3.9.6 with 255 IP requests
- macOS 26.0.1/Python 3.12.11 with Nmap 7.98

IP information like Longitude, Latitude, City and Region could be incorrect.

Inspired by [pwhois](https://github.com/dagonis/pwhois) Python library.

# Requirements

`nmap` Network MAPper

- **Debian / Linux**
```shell
sudo apt update && sudo apt install git nmap -y
```

- **macOS**
```shell
brew update
brew install git
brew install nmap
```

# Installation

```shell
git clone https://github.com/ludoComp9/iplookup.git
cd iplookup
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
chmod a+x iplookup.py
```

# Usage

```plaintext
usage: iplookup.py [-h] [-V] [-d] [--nmap] [--nmap-port <port> [<port> ...]] [-i <ip address>] [--file <filename>] [-s <separator_character>]
                   [--field <separator_field>] [--format {json,csv}] [-o <filename>] [--proxy <proxy_host>:<proxy_port>] [--noproxy]

--== IP lookup v0.06 ==--

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -d, --debug           enable debug mode
  --nmap                get FQDN from TLS certificate(s) retrieved from ports identified by nmap
  --nmap-port <port> [<port> ...]
                        get FQDN from TLS certificate(s) retrieved from ports given in argument
  -i <ip address>       IP to check
  --file <filename>     IPs to check
  -s <separator_character>, --separator <separator_character>
                        specify the separator used in input CSV file
  --field <separator_field>, --field <separator_field>
                        select field includes IP address
  --format {json,csv}   specify output format (default: csv)
  -o <filename>, --output <filename>
                        specify the output filename
  --proxy <proxy_host>:<proxy_port>
                        specify HTTP proxy with port. Example: "localhost:3128"
  --noproxy             Ignore system proxy (if defined)
```

# Example

## Get IP information for an IPv4 address given in input and check TLS certificates for opened ports found using nmap tool

```shell                                                 
./iplookup.sh --nmap -i 8.8.8.8 
[2025-10-29 16:15:17,611][INFO][iplookup] 1 lookup(s) successfully performed for 1 IP address(s) given.
[
  {
    "IP": "8.8.8.8",
    "Primary FQDN": "dns.google",
    "FQDN Certificates": [
      "dns.google:443"
    ],
    "PTR": "8.8.8.8.in-addr.arpa",
    "Origin AS": "15169",
    "Prefix": "8.8.8.0/24",
    "AS path": "8220 15169",
    "AS Org Name": "Google LLC",
    "Org Name": "Google LLC",
    "Net Name": "GOGL",
    "Cache Date": "Oct 29 2025 05:56:26",
    "Latitude": "37.405992",
    "Longitude": "-122.078515",
    "City": "Mountain View",
    "Region": "California",
    "Country": "United States of America",
    "CC": "US"
  }
]
```

## Get IP information for a list of IPv4 addresses recorded in a CSV file and save result to result.csv CSV file

- Content of `ip_to_check.csv` CSV file with IP addresses to check
```plaintext
8.8.8.8
184.86.236.41
```

- Command
```shell
./iplookup.sh --nmap --file ip_to_check.txt --output result.csv
[2025-08-05T14:59:19+z][INFO][IP Lookup] : 2 lookup(s) successfully performed for 2 IP address(s) given.
```

- CSV file
```plaintext
IP,Primary FQDN,FQDN Certificates,PTR,Origin AS,Prefix,AS path,AS Org Name,Org Name,Net Name,Cache Date,Latitude,Longitude,City,Region,Country,CC
8.8.8.8,dns.google,dns.google:443,8.8.8.8.in-addr.arpa,15169,8.8.8.0/24,8220 15169,Google LLC,Google LLC,GOGL,Oct 29 2025 05:56:26,37.405992,-122.078515,Mountain View,California,United States of America,US
184.86.236.41,a184-86-236-41.deploy.static.akamaitechnologies.com,www.homelandsecurity.gov:443,41.236.86.184.in-addr.arpa,16625,184.86.236.0/22,293 6453 20940 16625,"Akamai Technologies, Inc.","Akamai International, BV",AIBV,Oct 29 2025 05:56:26,43.296950,5.381070,Marseille,Provence-Alpes-Cote-d'Azur,France,FR
```