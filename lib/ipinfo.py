#Python ipinfo library

import socket
import time
import re
import logging
import ipaddress
from lib.log import setup_logger

pw_server = 'whois.pwhois.org'
pw_port = 43

class ip(object):
	logger = setup_logger(__name__)

	@classmethod
	def set_log_level(cls, log_level=logging.INFO):
		cls.logger.setLevel(log_level)

	@classmethod
	def lookup(cls, query):
		def _prepare_result(ip='', fqdn='', ptr='', origin_as='', prefix='', as_path='', as_org_name='', org_name='', net_name='', cache_date='', latitude='', longitude='', city='', region='', country='', cc=''):
			return {"IP": ip, "Primary FQDN": fqdn, "PTR": ptr, "Origin AS": origin_as, "Prefix": prefix, "AS path": as_path, "AS Org Name": as_org_name, "Org Name": org_name, "Net Name": net_name, "Cache Date": cache_date, "Latitude": latitude, "Longitude": longitude, "City": city, "Region": region, "Country": country, "CC": cc}

		"""Single query, takes a single IP (represented as a string) and returns a pwhois_obj."""
		# Support IP address that could contain [.] separator
		upd_query = normalize_ip(query)

		if ip_ver := check_ip(upd_query):
			cls.logger.debug(f"{upd_query} is a valid {ip_ver} address")
			# Get FQDN(s)
			try:
				answers = socket.gethostbyaddr(upd_query)
				fqdn = answers[0]
				ptr = answers[1]
			except Exception as e:
				cls.logger.error(f"[{upd_query}] DNS lookup failed: {e}")			
				fqdn = ''
				ptr = ['']

			# Get Lookup information
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((pw_server, pw_port))
			query_bytes = (upd_query + "\r\n").encode()
			s.send(query_bytes)
			resp = s.recv(500)
			whois_data = resp.decode('utf-8').split('\n')
			try:
				return _prepare_result(
						whois_data[0].split(': ')[1],
						fqdn,
						ptr,
						whois_data[1].split(': ')[1],
						whois_data[2].split(': ')[1],
						whois_data[3].split(': ')[1],
						whois_data[4].split(': ')[1],
						whois_data[5].split(': ')[1],
						whois_data[6].split(': ')[1],
						whois_data[7].split(': ')[1],
						whois_data[8].split(': ')[1],
						whois_data[9].split(': ')[1],
						whois_data[10].split(': ')[1],
						whois_data[11].split(': ')[1],
						whois_data[12].split(': ')[1],
						whois_data[13].split(': ')[1]
					)
			except Exception as error:
				cls.logger.error(f"Could not retrieve information about {query}: {error}")
				return _prepare_result(upd_query, fqdn, ptr)
		else:
			cls.logger.error(f"Input {query} is invalid")

def normalize_ip(ip_str: str) -> str:
    # Replace [.] with .
    return re.sub(r'\[\.\]', '.', ip_str)

def check_ip(data):
	try:
		valid_ip = ipaddress.ip_address(data)
		if isinstance(valid_ip, ipaddress.IPv4Address):
			return 'IPv4'
			#self.logger.debug(f"{data} is a valid IPv4 address")
		elif isinstance(valid_ip, ipaddress.IPv6Address):
			#self.logger.debug(f"{data} is a valid IPv6 address")
			return 'IPv6'
	except ValueError:
		return False