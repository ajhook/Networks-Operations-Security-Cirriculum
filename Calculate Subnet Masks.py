# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#importing libraries
import ipaddress

#Function to calculate Network Information
def network_info(IPV4):
    network = ipaddress.IPv4Network(IPV4, strict=False)
    
    #Get relevent Network Information
    subnet_address = str(network.network_address)
    broadcast_address = str(network.broadcast_address)
    first_valid_host = str(network.network_address + 1)
    last_valid_host = str(network.broadcast_address - 1)
    
    return subnet_address, broadcast_address, first_valid_host, last_valid_host

# function to take info from user and print results
def main():
    #get input 
    IPV4 = input("Enter IP Address in CIDR notation")
    
    #Calculate details 
    subnet_address, broadcast_address, first_valid_host, last_valid_host = network_info(IPV4)
    
    #display results
    print(f"Subnet Address: {subnet_address}")
    print(f"Broadcast Address: {broadcast_address}")
    print(f"Valid Hosts Range: {first_valid_host} - {last_valid_host}")
    
if __name__ == "__main__":
    main()