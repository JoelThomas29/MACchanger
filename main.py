#!/usr/bin/env python

""" This program checks if running on root, creates objects to handle user arguments and validate inputs """

import os
import re
import sys
import subprocess
import optparse
from setting_mac import new_mac
from setting_mac import retrieve_mac

def userid():

	# Verifying if current user has privileges
	if os.geteuid() != 0:
		print("[-] Permission denied. Run as root")
		sys.exit()
	else:
		pass

def arg_handeling():

	# *************************************************************************************************************
	# Creating object that could handle user inputs as arguments
	parse = optparse.OptionParser()

	# Defining all arguments that the program will support
	parse.add_option("-i", "--interface", dest="INTERFACE", help="Interface to change MAC address")
	parse.add_option("-m", "--mac", dest="NEW_MAC", help="New MAC address")
	#parse.add_option("-r", "--revert", help="Change back to original MAC")
	#parse.add_option("-o", "--original", dest="ORIGINAL", help="Display original MAC address")

	# Parsing the arguments to the program
	(options,arguments) = parse.parse_args()
	# *************************************************************************************************************

	# Validating if input is provided
	if options.INTERFACE == None and options.NEW_MAC == None:
		parse.error(" Use --help for more info")
	if not options.INTERFACE:
		parse.error(" Interface not specified. Use --help for more info.")
	elif not options.NEW_MAC:
		parse.error(" MAC not specified. Use --help for more info.")
	return options

def validation(options):

	# Verifying the interface exists
	flag = False
	try:
		if subprocess.check_output('ifconfig ' + options.INTERFACE, shell=True):
			pass
	except:
		flag = True

	# Verifying MAC entered follows the convention
	if re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", options.NEW_MAC):
		pass
	else:
		print("[-] Invalid MAC address \n    Format : xx:xx:xx:xx:xx:xx \n    where x is any hexadecimal value")
		flag = True

	# Exit program if error found in any of the two verification (interface/MAC)
	if flag == True:
		sys.exit()
	else:
		pass

def getting_fixed_MAC():
	
	# Finding the value of permanent MAC and store in text file/ if already present retrieve the value
	global permanent_mac
	if os.path.isfile("permanent_mac.txt"):
		with open("permanent_mac.txt", "r") as temp:
			temp.seek(0)
			permanent_mac = temp.read()
	else:
		permanent_mac = retrieve_mac(options)
		with open("permanent_mac.txt", "w") as temp:
			temp.write(permanent_mac)

userid()
options = arg_handeling()
validation(options)
getting_fixed_MAC()
new_mac(options, permanent_mac)
