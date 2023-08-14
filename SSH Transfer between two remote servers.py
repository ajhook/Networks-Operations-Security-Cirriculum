# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 15:10:09 2023

@author: alexa
"""
#Impport libraries
import paramiko
import subprocess

# Source and destination server information
source_server_ip = "192.168.56.101"
destination_server_ip = "192.168.56.102"
username = "ajhook"
private_key_path = "C:\\Users\\alexa\\.ssh\\id_rsa"

# SSH client initialization for the source server
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load your private key
private_key = paramiko.RSAKey(filename=private_key_path)

# Connect to the source server using key-based authentication
client.connect(source_server_ip, username=username, pkey=private_key)

# Run ifconfig and iw dev commands to get network interfaces and status
stdin, stdout, stderr = client.exec_command("ifconfig && iw dev")

# Read the output of the commands
network_info = stdout.read().decode("utf-8")

# Close the SSH connection to the source server
client.close()

# SSH client initialization for the destination server
client_dest = paramiko.SSHClient()
client_dest.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the destination server using key-based authentication
client_dest.connect(destination_server_ip, username=username, pkey=private_key)

# Create a temporary file to store network information
with client_dest.open_sftp().file("/tmp/network_info.txt", "w") as f:
    f.write(network_info)

# Transfer the temporary file to the destination server using scp
scp_command = f"scp -i {private_key_path} /tmp/network_info.txt {username}@{destination_server_ip}:/path/on/destination/server/"
subprocess.call(scp_command, shell=True)

# Close the SSH connection to the destination server
client_dest.close()

print("Network information transferred successfully.")

