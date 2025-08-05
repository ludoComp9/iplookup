# lookup

A small Python script to retrieve information from IP address(es) given in parameter.

# Purpose

Purpose of this very simple tool is to:
- get a reverse DNS lookup
- get IP information such as ASN, Organisation name, Network name, Country

Note: IP Lookup uses pwhois server to get information.

# Note

This tool has been successfully tested on macOS 15.6/Python 3.9.6 with 255 IP requests.

IP information like Longitude, Latitude, City and Region could be incorrect.

# Requirements

***If Git client tool is not already installed on your environment***

- **Debian / Linux**
```
sudo apt update && sudo apt install git -y
```

- **macOS**
```
brew update
brew install git
```

# Installation

```
git clone https://github.com/ludoComp9/lookup.git
cd lookup
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Usage

```
usage: lookup.py [-h] [-V] [-d] [-i <ip address>] [--file <filename>] [-s <separator_character>] [--field <separator_field>] [--format {json,csv}]
                 [-o <filename>]

--== IP lookup v0.02 ==--

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -d, --debug           Enable debug mode
  -i <ip address>       IP to check
  --file <filename>     IPs to check
  -s <separator_character>, --separator <separator_character>
                        Separator used in input CSV file
  --field <separator_field>, --field <separator_field>
                        Select field includes IP address
  --format {json,csv}   Specify output format (default: csv)
  -o <filename>, --output <filename>
                        Specify the output filename
```

# Example

## Get IP information for an IPv4 address given in input

```
./lookup.py -i 8.8.8.8
[2025-08-05T23:55:20+z][INFO][IP Lookup] : 1 lookup(s) successfully performed for 1 IP address(s) given.
[{'IP': '8.8.8.8', 'Primary FQDN': 'dns.google', 'PTR': ['8.8.8.8.in-addr.arpa'], 'Origin AS': '15169', 'Prefix': '8.8.8.0/24', 'AS path': '8220 15169', 'AS Org Name': 'Google LLC', 'Org Name': 'Google LLC', 'Net Name': 'GOGL', 'Cache Date': 'Aug 05 2025 06:03:15', 'Latitude': '37.405992', 'Longitude': '-122.078515', 'City': 'Mountain View', 'Region': 'California', 'Country': 'United States of America', 'CC': 'US'}]
```

## Get IP information for a list of IPv4 addresses recorded in a CSV file and save result to result.csv CSV file

- Content of `ip_to_check.csv` CSV file with IP addresses to check
```
8.8.8.8
184.86.236.41
```

- Command
```
./lookup.py --file ip_to_check.txt --output result.csv
[2025-08-05T14:59:19+z][INFO][IP Lookup] : 2 lookup(s) successfully performed for 2 IP address(s) given.
```

- Result file
```
IP,Primary FQDN,PTR,Origin AS,Prefix,AS path,AS Org Name,Org Name,Net Name,Cache Date,Latitude,Longitude,City,Region,Country,CC
8.8.8.8,dns.google,['8.8.8.8.in-addr.arpa'],15169,8.8.8.0/24,8220 15169,Google LLC,Google LLC,GOGL,Aug 05 2025 06:03:15,37.405992,-122.078515,Mountain View,California,United States of America,US
184.86.236.41,a184-86-236-41.deploy.static.akamaitechnologies.com,['41.236.86.184.in-addr.arpa'],16625,184.86.236.0/22,293 6453 20940 16625,"Akamai Technologies, Inc.","Akamai International, BV",AIBV,Aug 05 2025 06:03:15,43.296950,5.381070,Marseille,Provence-Alpes-Cote-d'Azur,France,FR
```