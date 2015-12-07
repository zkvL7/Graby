#!/usr/bin/env python

# Graby - 1.0
# Copyright 2015 Yael Basurto
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
from sys import argv
from sys import exit
from platform import system
from threading import Thread 
from time import sleep, strftime

''' Colors  '''
WHITE = '\033[97m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

''' Global flag '''
global flag

def setColors():
	if system() == 'Windows':
		global WHITE; WHITE = ''
		global CYAN; CYAN = ''
		global PURPLE; PURPLE = ''
		global YELLOW; YELLOW = ''
		global GREEN; GREEN = ''
		global RED; RED = ''
		global ENDC; ENDC = ''

def waitBanner(s,o):
	banner =  s.recv(1024)
	if len(banner) > 0:
		print GREEN + banner + ENDC
		o.write(banner+"\n")
		global flag; flag=True
	return

def output():
	now = strftime("%c")
	name = "GrabyReport "+argv[1]+" "+now
	print WHITE + "Results will be saved into file:\n" + name + ENDC
	o = open(name,"w+")
	o.write("Graby 1.0 - Report\nC0d3d by @zkvL7\nReport created on "+now+"\n")
	o.write("--------------------------------------------\n\n")
	o.write("Target: "+argv[1]+"\n")
	o.write("--------------------------------------------\n\n")
	return o

if __name__ == "__main__":
	setColors()
	print CYAN + '''
	    = graby =
	- C0d3d by zkvL -	
	''' + ENDC

	if len(argv) != 3:
		print GREEN + "Usage: %s {IP ADDRESS} {PORT1,PORT2,PORT3,...,PORTn}" %argv[0]
		print "Example: %s 172.22.34.107 22,23,25,80,443" %argv[0] + ENDC
		exit(0)

	try:	
		o = output()
		ports = argv[2].split(",")
		print YELLOW + "Getting banners from " + argv[1] + ENDC
		for port in ports:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			global flag; flag=False
			print YELLOW + "Connecting to port", port + " ..." + ENDC
			o.write("Banner grabbing from port "+port+"\n")
			s.connect((argv[1], int(port)))
			sub = Thread(target=waitBanner, args=(s,o)); sub.setDaemon(True); sub.start()
			sleep(3)
			if not flag:
				o.write("[!] No banner received\n\n")
				print RED + "[!] No banner received" + ENDC
			s.close
		o.close()
	except:
		print RED + "[!] Something wrong happened dude ... =(" +ENDC
		raise

