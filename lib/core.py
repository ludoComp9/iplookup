#Python pwhois library

import socket
import time
import re
import logging

pw_server = 'whois.pwhois.org'
pw_port = 43

class ip(object):
	"""This is the data returned by a pwhois lookup, format is modeled after the output of whob"""
	@classmethod
	def lookup(cls, query, logger=None):
		def _msg(level, msg):
			if logger:
				eval(f"logger.{level}")(msg)
			else:
				print(f"[{level}] [{query}] DNS lookup failed: {e}")

		def _prepare_result(ip='', fqdn='', ptr='', origin_as='', prefix='', as_path='', as_org_name='', org_name='', net_name='', cache_date='', latitude='', longitude='', city='', region='', country='', cc=''):
			return {"IP": ip, "Primary FQDN": fqdn, "PTR": ptr, "Origin AS": origin_as, "Prefix": prefix, "AS path": as_path, "AS Org Name": as_org_name, "Org Name": org_name, "Net Name": net_name, "Cache Date": cache_date, "Latitude": latitude, "Longitude": longitude, "City": city, "Region": region, "Country": country, "CC": cc}

		"""Single query, takes a single IP (represented as a string) and returns a pwhois_obj."""
		if ip_check(query):
			# Get FQDN(s)
			try:
				answers = socket.gethostbyaddr(query)
				fqdn = answers[0]
				ptr = answers[1]
			except Exception as e:
				_msg('error', f"[{query}] DNS lookup failed: {e}")			
				fqdn = ''
				ptr = ['']

			# Get Lookup information
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((pw_server, pw_port))
			query_bytes = (query + "\r\n").encode()
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
				_msg('error', f"Could not retrieve information about {query}: {error}")
				return _prepare_result(query, fqdn, ptr)
		else:
			_msg('error', f"Input {query} is invalid")

class asn(object):
	def __init__(self, asn, ranges):
		self.asn = asn
		self.ranges = list(ranges)

	@classmethod
	def lookup(cls, as_n):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((pw_server, pw_port))
		query_bytes = 'app="Python pwhois client" routeview source-as={}\r\n'.format(as_n).encode()
		s.send(query_bytes)
		resp = recvall(s)
		range_output = resp.split("\n")[2:-1]
		ranges = set()
		for range in range_output:
			ranges.add(range.lstrip("*> ").split(" ")[0])
		return asn(as_n, ranges)

	def __str__(self):
		return "ASN {}\nRanges:\n{}".format(self.asn, "\n".join([r for r in self.ranges]))


def ip_check(ip):
	ip_reg = re.compile(
		'(?:^(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})$)')
	if ip_reg.match(ip):
		return True
	else:
		return False


def recvall(sock):
	data = ""
	part = None
	while part != "":
		part = sock.recv(4096)
		data += part
	return data
