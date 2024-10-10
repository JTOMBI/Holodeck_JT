import paramiko

command = "ls /home/"

# Update the next three lines with your
# server's information

host = "192.168.75.129"
username = "jtombi"
password = "salakae"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command(command)
print(_stdout.read().decode())
client.close()
