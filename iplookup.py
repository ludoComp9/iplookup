#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# IPlookup
# 05/08/2025	0.01	Initial script
# 06/08/2025	0.02	Logging policy updated
# 11/08/2025	0.03	Minor update
# 14/08/2025	0.04	Add proxy support
# 05/09/2025	0.05	Change standard output to JSON format and proxy configuration

import argparse
import os
import sys
import json
import csv
import easydict
from sys import stdout
from lib.log import setup_logger
from lib.ipinfo import ip


__version__ = '0.05'

def get_options():
	""" Argument control """
	parser = argparse.ArgumentParser(description=f"--== IP lookup v{__version__} ==--")
	parser.add_argument('-V', '--version', action='version', version='{} v{}'.format(os.path.basename(__file__), __version__))
	parser.add_argument('-d', '--debug', dest='debug', help='enable debug mode', action="store_true")
	parser.add_argument('-i', dest='ip', help='IP to check', metavar='<ip address>')
	parser.add_argument('--file', dest='ipfile', help='IPs to check', metavar='<filename>', action='store')
	parser.add_argument('-s', '--separator', dest='separator', help='specify the separator used in input CSV file', metavar='<separator_character>', default=',')
	parser.add_argument('--field', '--field', dest='field', help='select field includes IP address', metavar='<separator_field>')
	parser.add_argument('--format', dest='output_format', help='specify output format (default: csv)', choices=['json', 'csv'], default='csv', type=str.lower)
	parser.add_argument('-o', '--output', dest='output_file', help='specify the output filename', metavar='<filename>', action='store')
	parser.add_argument('--proxy', dest='proxy', help='specify HTTP proxy with port. Example: "localhost:3128"', metavar='<proxy_host>:<proxy_port>', type=parse_proxy, action='store')
	parser.add_argument('--noproxy', dest='noproxy', help='Ignore system proxy (if defined)', action="store_true")
	return parser

def parse_proxy(value):
	try:
		host, port = value.split(":")
		return host, int(port)
	except ValueError:
		raise argparse.ArgumentTypeError("Proxy must be defined as <host>:<port>. (Example: localhost:3128)")

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
	args_parser = get_options()
	args = args_parser.parse_args()
	script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	if not args.proxy and not args.noproxy and 'https_proxy' in os.environ:
		# Use default proxy
		logger.debug('Proxy system detected. Script will use it.')
		default_proxy = os.environ['https_proxy'].split('/')[-1].split('@')[-1]
		args.proxy = parse_proxy(default_proxy)
	else:
		# Ignore system proxy
		args.proxy = None

	if args.debug:
		log_level = 10	# DEBUG
	else:
		log_level = 20	# INFO
	logger = setup_logger(script_name, log_level)
	result = []
	nb_ip = 0

	if not args.ip and not args.ipfile:
		args_parser.print_help()
		sys.exit(1)
	
	if args.ip:
		nb_ip += 1
		ip.set_log_level(log_level)
		result.append(ip.lookup(args.ip, args.proxy))
	elif args.ipfile:
		with open(args.ipfile, newline='', encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile, delimiter=args.separator)
			ip.set_log_level(log_level)
			for row in reader:
				if len(row) == 1:
					item = row[0]
				else:
					item = row[args.field]
				nb_ip += 1
				if res := ip.lookup(item, args.proxy):
					result.append(res)
	if result:
		logger.info(f"{len(result)} lookup(s) successfully performed for {nb_ip} IP address(s) given.")
		if isinstance(result, dict):
			result = [result]
		if args.output_file:
			eval(f"output_{args.output_format}")(result, args.output_file)
		else:
			# Return result (in JSON format) to STDOUT
			output_json(result)