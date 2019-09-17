import paramiko
from scp import SCPClient


username='root'
password='root'
port=22

with open('DSS_IP.txt', 'r') as f:
	lines = f.readlines()
	for line in lines:
		line = line.replace('\n', '')
		line = line.split(',')
		print('Current IP: {} - {}'.format(line[0], line[2]))
		try:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			print('Connecting to host')
			client.connect(hostname=line[0], username=username, password=password, port=line[1])
			# backup source file
			#resp = client.exec_command('cp /etc/config/wireless /etc/config/wireless_bkp')
			#resp = client.exec_command('cp /etc/config/network /etc/config/network_')
			# replace in file
			#resp = client.exec_command('sed -i -e \'s/8.8.8.8/10.10.0.35/g\' /etc/config/network')
			#resp = client.exec_command('sed -i -e \'s/US/RU/g\' /etc/config/wireless')
			# print('Killing processes')
			# resp = client.exec_command('killall skyreaper')
			# resp = client.exec_command('killall airodump-ng')
			# print('Removing files')
			# resp = client.exec_command('rm /root/skyreaper')
			# resp = client.exec_command('rm /usr/bin/skyreaper')

			# scp = SCPClient(client.get_transport())
			# print('Uploading skyreaper')
			# scp.put('skyreaper', '/usr/bin/skyreaper')			
			# resp = client.exec_command('chmod 0755 /usr/bin/skyreaper')
			# print('Done!')
			# resp = client.exec_command('mv /usr/bin/SendWatchDog.sh /usr/bin/SendDataWatchdog.sh')
			# resp = client.exec_command('mv /root/test.sh /usr/bin/SendData.sh')
			# resp = client.exec_command('sed -i -e \'s/O \\/ /O \\/wtf\\/ /g\' /usr/bin/SendData.sh')
			_, resp, err = client.exec_command('du -sh /usr/bin/skyreaper')
			for elem in resp:				
				print(str(elem))
			for elem2 in err:				
				print(str(elem2))
			# print('Patching cron')
			# try:
			# 	scp.put('cron', '/etc/crontabs/root')
			
			# 	print('Done!')
			# except scp.SCPException:
			# 	print('There is no space')			

			#print(str(resp[1].read().find('option dns \'10.10.0.35\'')))
		except TimeoutError:
			print('Can not connect to {}'.format(line[0]))
		except paramiko.ssh_exception.NoValidConnectionsError:
			print('NoValidConnectionsError for {}'.format(line[0]))
	