import paramiko
import socket
import subprocess
import sys
import threading
host_key = paramiko.RSAKey(filename="test_rsa.key")
paramiko.util.log_to_file("filename.log")
class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        #if (username=="root") and (password=="apakekgitu91114045"):
        return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[*] Waiting for Connection...")
    client, addr = sock.accept()
except Exception as e:
    print("[-] Listen Failed " + str(e))
    sys.exit(1)
print("Dapat Koneksi!!!")
if True:#try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException as x:
        print("[x] SSH negotiation failed")
    chan = bhSession.accept(20)
        
    print("Ter Autentikasi...bla bla bla")
    print(chan.recv(1024))
    chan.send(b"Welcome to SSH")
    while True:
        try:
            command = input("Perintah: ").strip("\n").encode("utf-8")
            if command != "exit".encode("utf-8"):
                chan.send(command)
                print(chan.recv(1024) + b"\n")
            else:
                chan.send("exit".encode("utf-8"))
                print("KELUAR!!!!")
                bhSession.close()
                raise Exception ("exit")
        except KeyboardInterrupt:
            bhSession.close()
"""
except Exception as e:
    print("Exception: %s" %(str(e)))
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)"""