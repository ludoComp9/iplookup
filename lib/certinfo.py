# certinfo Python library
import nmap
import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from lib.log import setup_logger

class fqdncert:
	def __init__(self, ip, ports=None, timeout=5):
		self.ip = ip
		self.ports = ports if ports else range(1, 10000)
		self.timeout = timeout
		self.open_ports = []

	def scan_ports(self):
		""" Search opened ports """
		nm = nmap.PortScanner()
		if True: #try:
			#nm.scan(self.ip, arguments='-p ' + ','.join(map(str, self.ports)) + ' -Pn')
			print(','.join(map(str, self.ports)))
			nm.scan(self.ip, arguments='-p 5443 -Pn')
			hosts = nm.all_hosts()
			print(f"RESULT={nm._scan_result}")
			print(f"IP:{self.ip} - HOSTS:{hosts}")
			if self.ip in hosts:
				host_info = nm[self.ip]
				print(host_info)
			
			self.open_ports = [
				port for port in self.ports
				if nm[self.ip]['tcp'].get(port, {}).get('state') in ('open', 'filtered')
			]
		# except Exception as e:
		#     print(f"[Erreur] Échec du scan Nmap : {e}")
		#     self.open_ports = []

	def get_certificate(self, port):
		"""Récupère le certificat TLS depuis l'IP et le port spécifiés."""
		context = ssl.create_default_context()
		try:
			with socket.create_connection((self.ip, port), timeout=self.timeout) as sock:
				with context.wrap_socket(sock, server_hostname=self.ip) as ssock:
					cert = ssock.getpeercert(binary_form=True)
					return cert
		except Exception as e:
			print(f"[Erreur] Certificat sur {self.ip}:{port} - {e}")
			return None

	def extract_fqdn_from_cert(self, cert_bytes):
		"""Extrait le FQDN du certificat."""
		try:
			cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
			# Vérifier SAN
			try:
				san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
				for dns_name in san.value.get_values_for_type(x509.DNSName):
					return dns_name
			except x509.ExtensionNotFound:
				pass
			# Vérifier CN
			subject = cert.subject
			for attribute in subject:
				if attribute.oid == x509.NameOID.COMMON_NAME:
					return attribute.value
		except Exception as e:
			print(f"[Erreur] Analyse du certificat : {e}")
		return None

	def find_fqdns(self):
		"""Main method pour scanner et récupérer les FQDNs."""
		self.scan_ports()
		fqdns = []
		for port in self.open_ports:
			cert = self.get_certificate(port)
			if cert:
				fqdn = self.extract_fqdn_from_cert(cert)
				if fqdn:
					fqdns.append({'port': port, 'fqdn': fqdn})
		return fqdns