# certinfo Python library
import nmap
import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from lib.log import setup_logger

class fqdncert:
	def __init__(self, ip, ports=None, timeout=5, logger=setup_logger()):
		self.ip = ip
		self.ports = ports if ports else range(1, 10000)
		self.timeout = timeout
		self.open_ports = []
		self.logger = logger

	def scan_ports(self):
		""" Search opened ports """
		nm = nmap.PortScanner()
		try:
			nm.scan(self.ip, arguments=f"-p {','.join(map(str, self.ports))} -Pn")
			hosts = nm.all_hosts()
			self.open_ports = [
				port for port in self.ports
				if nm[self.ip]['tcp'].get(int(port), {}).get('state') == 'open'
			]
		except Exception as e:
			self.logger.error(f"Nmap scan failed: {e}")
			self.open_ports = []

	def get_certificate(self, port):
		""" Get TLS certificate from port specified in input """
		context = ssl.create_default_context()
		# Ignore Host/IP check
		context.check_hostname = False
		context.verify_mode = ssl.CERT_NONE

		try:
			self.logger.debug(f"IP:{self.ip} - Port:{port} - Timeout:{self.timeout}")
			with socket.create_connection((self.ip, port), timeout=self.timeout) as sock:
				with context.wrap_socket(sock, server_hostname=self.ip) as ssock:
					cert = ssock.getpeercert(binary_form=True)
					return cert
		except Exception as e:
			self.logger.warn(f"TLS certificat not found on {self.ip}:{port}: {e}")
			return None

	def extract_fqdn_from_cert(self, cert_bytes):
		""" Get FQDN from TLS certificate found """
		try:
			cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
			# Check SAN
			try:
				san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
				for dns_name in san.value.get_values_for_type(x509.DNSName):
					return dns_name
			except x509.ExtensionNotFound:
				pass
			# Check CN
			subject = cert.subject
			for attribute in subject:
				if attribute.oid == x509.NameOID.COMMON_NAME:
					return attribute.value
		except Exception as e:
			self.logger.error(f"TLS certificate parsing failed: {e}")
		return None

	def find_fqdns(self):
		""" Main """
		self.scan_ports()
		fqdns = []
		for port in self.open_ports:
			cert = self.get_certificate(port)
			if cert:
				fqdn = self.extract_fqdn_from_cert(cert)
				if fqdn:
					fqdns.append({'port': port, 'fqdn': fqdn})
		return fqdns