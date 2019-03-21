import paramiko

def ssh_command(user, password, ip, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password, port=port)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        while True:
            try:
                ssh_session.exec_command(input("command"))
                ssh_session = client.get_transport().open_session()
                print(ssh_session.recv(1024))
            except KeyboardInterrupt:
                ssh_session.close()
ssh_command("root", "567890", "192.168.43.1", 22)