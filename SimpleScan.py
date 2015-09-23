
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
#!/usr/bin/python
 
# __author__: Mansoor (manz@digitz.org)
# Visit digitz.org
 
# Importing the modules
# socket :=> This is what we use to create a socket connection
# argparse is used to parse arguments. This is not important now
# and it is out of the scope of this post
import socket,sys,time,datetime,argparse,os
flag = 0  # we're gonna use this flag later. Just keep it in mind
os.system('clear') # Clear the console window
line = "+" * 80 # Just a fancy line consisting '+'
desc = line+'''\nA Simple port scanner that works!! (c) digitz.org
	Example usage: python port_scanner.py example.com 1 1000
	The above example will scan the host \'example.com\' from port 1 to 1000
	To scan most common ports, use: python port_scanner.py example.com\n'''+line+"\n"
	# Just a description about the script and how to use it
 
# I would suggest you to read about "argparse", it comes in handy
# when you want to parse arguments 
parser = argparse.ArgumentParser(description = desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('host', metavar='H', help='Host name you want to scan')
parser.add_argument('startport', metavar='P1', nargs='?', help='Start scanning from this port')
parser.add_argument('endport', metavar='P2', nargs='?',help='Scan until this port')
args = parser.parse_args()
 
host = args.host # The host name to scan for open ports
ip = socket.gethostbyname(host) # Converts the host name into IP address 
 
# args.startpoint corresponds to the first port we will scan
# args.endport corresponds to the last port
 
# Here, we're checking if both starting port and ending port is defined
# If it is not defined, we will do a scan over most popular TCP ports. 
if (args.startport) and args.endport :
	# If this condition is true, the script will scan over this port range
	start_port = int(args.startport)
	end_port = int(args.endport)
else:
	# In this case, the script will scan the most common ports.
	# that is, if you did not give any ports as argument.
	flag = 1
 
open_ports = []  # This list is used to hold the open ports
 
# This dictionary contains the most popular ports used
# You can add ports here. 
# The key is the port number and the values is the service used by that port
common_ports = {
 
	'21': 'FTP',
	'22': 'SSH',
	'23': 'TELNET',
	'25': 'SMTP',
	'53': 'DNS',
	'69': 'TFTP',
	'80': 'HTTP',
	'109': 'POP2',
	'110': 'POP3',
	'123': 'NTP',
	'137': 'NETBIOS-NS',
	'138': 'NETBIOS-DGM',
	'139': 'NETBIOS-SSN',
	'143': 'IMAP',
	'156': 'SQL-SERVER',
	'389': 'LDAP',
	'443': 'HTTPS',
	'546': 'DHCP-CLIENT',
	'547': 'DHCP-SERVER',
	'995': 'POP3-SSL',
	'993': 'IMAP-SSL',
	'2086': 'WHM/CPANEL',
	'2087': 'WHM/CPANEL',
	'2082': 'CPANEL',
	'2083': 'CPANEL',
	'3306': 'MYSQL',
	'8443': 'PLESK',
	'10000': 'VIRTUALMIN/WEBMIN'
}
 
starting_time = time.time() # Get the time at which the scan was started
print "+" * 40
print "\tSimple Port Scanner..!!!"
print "+" * 40
 
if (flag): # The flag is set, that means the user did not provide any ports as argument
	print "Scanning for most common ports on %s" % (host)
else:
	# The user did specify a port range to scan
	print "Scanning %s from port %s - %s: " % (host, start_port, end_port)
print "Scanning started at %s" %(time.strftime("%I:%M:%S %p"))
 
 
# This is the function that will connect to a port and will check
# if it is open or closed
def check_port(host, port, result = 1):
	# The function takes 3 arguments
	# host : the IP to scan
	# port : the port number to connect
	try:
		# Creating a socket object named 'sock'
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Setting socket timeout so that the socket does not wait forever to complete  a connection
		sock.settimeout(0.5)
		# Connect to the socket
		# if the connection was successful, that means the port
		# is open, and the output 'r' will be zero
		r = sock.connect_ex((host, port))	
		if r == 0:
			result = r 
		sock.close() # closing the socket
	except Exception, e:
		pass
 
	return result # returns the result of the scan.
 
# This function reads the dictonary of ports and services and 
# Checks for the service name corresponding to a port.
def get_service(port):
	port = str(port) # converts the int to string
	if port in common_ports: # check if the port is available in the common ports dictionary
		return common_ports[port] # returns the service name if available
	else:
		return 0 # return 0 if no service is identified
 
 
try:
	print "Scan in progress.."
	print "Connecting to Port: ",
 
	if flag: # The flag is set, means the user did not give any port range
		for p in sorted(common_ports): # So we will scan the common ports. 
			sys.stdout.flush() # flush the stdout buffer.
			p = int(p)
			print p,	
			response = check_port(host, p) # call the function to connect to the port
			if response == 0: # The port is open
				open_ports.append(p) # append it to the list of open ports
			#if not p == end_port:
				sys.stdout.write('\b' * len(str(p))) # This is just used to clear the port number displayed. This is not important at all
	else:
		
		# The user did provide a port range, now we have to scan through that range 
		for p in range(start_port, end_port+1):
			sys.stdout.flush()
			print p,
			response = check_port(host, p) # Call the function to connect to the port 
			if response == 0: # Port is open
				open_ports.append(p) # Append to the list of open ports
			if not p == end_port:
				sys.stdout.write('\b' * len(str(p)))
 
	print "\nScanning completed at %s" %(time.strftime("%I:%M:%S %p"))
	ending_time = time.time()
	total_time = ending_time - starting_time # Calculating the total time used to scan
	print "=" * 40
	print "\tScan Report: %s" %(host)
	print "=" * 40
	if total_time <= 60:
		total_time = str(round(total_time, 2))
		print "Scan Took %s seconds" %(total_time)
	else:
		total_time = total_time / 60
		print "Scan Took %s Minutes" %(total_time)
		
	if open_ports: # There are open ports available
		print "Open Ports: "
		for i in sorted(open_ports):
			service = get_service(i)
			if not service: # The service is not in the disctionary
				service = "Unknown service"
			print "\t%s %s: Open" % (i, service)
	else:
		# No open ports were found
		print "Sorry, No open ports found.!!"
 
except KeyboardInterrupt: # This is used in case the  user press "Ctrl+C", it will show the following error instead of a python's scary error
	print "You pressed Ctrl+C. Exiting "		
	sys.exit(1)
