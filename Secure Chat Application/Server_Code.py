# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:37:49 2023

@author: alexa
"""
#import libraries
import socket
import threading
from cryptography.fernet import Fernet
import tkinter as tk
import logging

#set up logging for troubleshooting
logging.basicConfig(filename='C:\\Users\\alexa\\OneDrive\\Documents\\serverlog.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#Generate encryption keys 
key = Fernet.generate_key()
cipher_suite = Fernet(key)

#Set server information (same as client)
server_ip = '127.0.0.1'
server_port = 12345
server_name = 'Turing' #server name 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(2)  
#accepts up to two client connections

#notify user that server has started
print(f"{server_name} started and listening on", '127.0.0.1', ":", '12345')

clients = []

#Recieves messages from client  broadcasts to others connected
def handle_client(client_socket):
    print("client connected:", client_socket.getpeername())
    while True:
        encrypted_message = client_socket.recv(1024)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        for client in clients:
            if client != client_socket:
                client.send(encrypted_message) 
#accepts upto two client connections
for _ in range(2):  
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

logging.shutdown()
server_socket.close()
