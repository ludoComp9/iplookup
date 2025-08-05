#!python3

# -*- coding: utf-8 -*-

import argparse
import os
import yaml
import json
import csv
import easydict
import logging
from sys import stdout
from lib.core import ip
import ipaddress

__version__ = '0.01'
config_file = './etc/config.yml'

def getOptions():
	""" Argument control """
	args = argparse.ArgumentParser(description=f"--== IP lookup v{__version__} ==--")
	"""
	args.add_argument('-V', '--version', action='version', version='{} v{}'.format(os.path.basename(__file__), __version__))
	args.add_argument('-d', '--debug', dest='debug', help='Enable debug mode', action="store_true")
	args.add_argument('-i', dest='ip', help='IP to check')
	args.add_argument('--file', dest='ipfile', help='IPs to check')
	args.add_argument('-s', '--separator', dest='separator', help='Separator used in input CSV file', default=',')
	args.add_argument('--field', '--field', dest='field', help='Select field includes IP address')
	args.add_argument('--format', dest='output_format', help='Specify output format (CSV by default)', choices=['json', 'csv'], default='csv', type=str.lower)
	args.add_argument('-o', '--output', dest='output_file', help='Specify the output filename')
	"""
	args.add_argument('-V', '--version', action='version', version='{} v{}'.format(os.path.basename(__file__), __version__))
	args.add_argument('-d', '--debug', dest='debug', help='Enable debug mode', action="store_true")
	args.add_argument('-i', dest='ip', help='IP to check', metavar='<ip address>')
	args.add_argument('--file', dest='ipfile', help='IPs to check', metavar='<filename>', action='store')
	args.add_argument('-s', '--separator', dest='separator', help='Separator used in input CSV file', metavar='<separator_character>', default=',')
	args.add_argument('--field', '--field', dest='field', help='Select field includes IP address', metavar='<separator_field>')
	args.add_argument('--format', dest='output_format', help='Specify output format (default: csv)', choices=['json', 'csv'], default='csv', type=str.lower)
	args.add_argument('-o', '--output', dest='output_file', help='Specify the output filename', metavar='<filename>', action='store')
	return args.parse_args()

def set_logger():
	if args.debug:
		level = 10
	else:
		level = config.logger.level

	logger = logging.getLogger(__name__)
	logging.basicConfig(
		format=config.logger.log_format,
		datefmt=config.logger.datetime_format,
		style='{',
		level=level,
		handlers=[ logging.StreamHandler(stream=stdout)]
	)
	logger.debug(f"Configuration: {str(config)}")
	return logging.getLogger("IP Lookup")

def ip_info(data):
	try:
		valid_ip = ipaddress.ip_address(data)
		if isinstance(valid_ip, ipaddress.IPv4Address):
			logger.debug(f"{data} is a valid IPv4 address")
		elif isinstance(valid_ip, ipaddress.IPv6Address):
			logger.debug(f"{data} is a valid IPv6 address")
	except ValueError:
		logger.error("Invalid IP ({data})")
		return False
	else:
		return ip.lookup(data, logger)

def output_json(data, output_file=None):
	if output_file:
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2)
	else:
		json.dump(data, sys.stdout, indent=2)
		print()  # newline for clean terminal output

def output_csv(data, output_file=None):
	if not data:
		logger.error("No data to write to CSV.")
		return False
	with open(output_file, 'w', newline='', encoding='utf-8') as f:
		writer = csv.DictWriter(f, fieldnames=data[0].keys())
		writer.writeheader()
		writer.writerows(data)

if __name__ == "__main__":
	# Initialization
	args = getOptions()
	with open(config_file, 'r') as file:
		config = easydict.EasyDict(yaml.safe_load(file))
	logger = set_logger()
	result = []
	nb_ip = 0

	if args.ip:
		nb_ip += 1
		result.append(ip_info(args.ip))
	elif args.ipfile:
		with open(args.ipfile, newline='', encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile, delimiter=args.separator)
			for row in reader:
				if len(row) == 1:
					item = row[0]
				else:
					item = row[args.field]
				nb_ip += 1
				if res := ip_info(item):
					result.append(res)
	if result:
		logger.info(f"{len(result)} lookup(s) successfully performed for {nb_ip} IP address(s) given.")
		if isinstance(result, dict):
			result = [result]
		if args.output_file:
			eval(f"output_{args.output_format}")(result, args.output_file)
		else:
			""" Return result to STDOUT """
			print(result)