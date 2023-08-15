# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:05:11 2023

@author: alexa
"""

#import libraries
import tkinter as tk
from cryptography.fernet import Fernet
import socket
import threading
import html

#Genrate encryption keys 
key = Fernet.generate_key()
cipher_suite = Fernet(key)

#Set server Ip and Port
server_ip = '127.0.0.1'
server_port= 12345

#Create Gui
app = tk.Tk()
app.title("Enigma") #app name
#Create chat histort and buttons
chat_history = tk.Text(app, state=tk.DISABLED)
message_entry = tk.Entry(app)
send_button = tk.Button(app, text="Transmit", state=tk.DISABLED)

client_socket = None  
#will be assigned later

#connecting to server
def connect_to_server():
    global client_socket 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    #Recieve server started to recieve continous messages from server
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    #Enable the Send button
    send_button.config(state=tk.NORMAL) 

def send_message(client_socket):
    message = message_entry.get()
    if client_socket:
        #prevent XSS attacks by preventing empty messages and escaping special characters
        sanitized_message = html.escape(message)
        if sanitized_message:
            encrypted_message = cipher_suite.encrypt(sanitized_message.encode())
            client_socket.send(encrypted_message)
            chat_history.insert(tk.END, f"You: {sanitized_message}\n")
            message_entry.delete(0, tk.END)

def receive_messages(client_socket):
    while True:
        #deal with socket errors
        try:
            encrypted_message = client_socket.recv(1024)
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
            sanitized_message = html.escape(decrypted_message)
            chat_history.insert(tk.END, f"Friend: {sanitized_message}\n")
        except (socket.error, ConnectionResetError):
            break

send_button.config(command=lambda: send_message(client_socket))
chat_history.pack(fill=tk.BOTH, expand=True)
message_entry.pack(fill=tk.BOTH, padx=20, pady=10)
send_button.pack(fill=tk.BOTH, padx=5, pady=5)

#run GUI
app.mainloop()

if client_socket:
    client_socket.close()


