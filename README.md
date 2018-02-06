# SSHscanner
botnet scanner written in python

SSH scanner which runs a bruteforce attack with known default login credentials

Saves to vuln list

Dependencies: paramiko

# Setup(assuming you have a basic understanding of python and linux command line)

Copy SSHScanner.py to any location on your linux file system

pip install paramiko

# Usage(from the location of SSHScanner.py)

python SSHScanner.py <threads> <range> <octets> <timeout>

threads(integer 1 - 4000) - How many scanning threads to run at once

range(A, B, C) - How many IP octets will be specified

octets(IP octets) - Set default address for the specified octet range

timeout(integer 1 - inf) - Specify wait time for SSH connection

# DISCLAIMER

This tool is capable of causing damage to computers, 
computer networks, and the operators thereof. This tool was 
created for educational purposes. Illegal use of this tool 
and its variants is not encouraged by its author. The end-user 
is solely responsible for any use(legal or illegal) of this 
tool and/or its variants. By using this tool, you accept the 
reponsibity of ethical use.
