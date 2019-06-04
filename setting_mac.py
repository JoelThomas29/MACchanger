#!/usr/bin/env python

""" This program stores current MAC and sets the new """

import subprocess
import re

def retrieve_mac(options):

	# Saving the original MAC address
	check = re.search(b"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", subprocess.check_output("ifconfig " + options.INTERFACE, shell=True))
	return str(check.group()).lstrip('b')[1:18]

def new_mac(options, permanent_mac):
	
	# Getting the current MAC address
	current_mac = retrieve_mac(options)

	# Setting the New MAC address
	subprocess.call("ifconfig " + options.INTERFACE + " down", shell=True)
	subprocess.call("ifconfig " + options.INTERFACE + " hw ether " + options.NEW_MAC , shell=True)
	subprocess.call("ifconfig " + options.INTERFACE + " up", shell=True)

	# Verifying the change has been made before printing out to the user
	new_mac = retrieve_mac(options)

	# Printing the result
	print("[+] Permanent MAC : " + permanent_mac)
	print("[+] Current MAC : " + current_mac)
	print("[+] New MAC : " + new_mac)
	