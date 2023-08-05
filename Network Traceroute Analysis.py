# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 16:48:08 2023

@author: alexa
"""
#Import Libraries 
from scapy.all import *
import time
import geoip2.database
import folium

#Found this online, thought it was cool
#get IP address
def get_geolocation(IP):
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    try:
        response = reader.city(IP)
        city = response.city.name if response.city else "Unknown"
        country = response.country.name if response.country else "Unknown"
        return city, country, response.location.latitude, response.location.longitude
    except geoip2.errors.AddressNotFoundError:
        return "Not found", "Unknown", None, None
    finally:
        reader.close()

def traceroute(destination,max_hops=30,port=8080):
    ttl = 1
    map = folium.Map(location=[0, 0], zoom_start=2)


    while True:
        #Create ICMP Echo packet
        pkt = IP(dst = destination, ttl = ttl)/ICMP()
        
        #Send packet and record time 
        start_time = time.time()
        reply = sr1(pkt, verbose=False, timeout=2)
        
        #responce if no responce recieved
        if reply is None:
            print(f"{ttl}", "Time Exceeded")
            
            #Responce if TTL is exceed 
        elif reply.type ==11:
            #Retrieve hop IP and record time of reply 
            hop_ip = reply.src
            reply_time = time.time()
            #Calculate round-trip-time in ms units
            RTT = (reply_time - start_time)*1000
            #Find location
            city, country, lat, lon = get_geolocation(hop_ip)
            #Print hop number, ip RTT, cit and country
            print(f"{ttl}. {hop_ip} ({RTT:.2f} ms) - {city}, {country}" )
            
            #Add to map
            if lat and lon:
                folium.Marker(location=[lat, lon], popup=f"{hop_ip}\n{city}, {country}").add_to(map)
            
            #Responce if destination is reached 
        elif reply.type ==0:
            #Retrieve Hop ip and time of reply
            hop_IP = reply.src
            responce_time = time.time()
            #calculate RTT
            RTT = (responce_time - start_time)*1000
            #Find location
            city, country, lat, lon = get_geolocation(hop_ip)
            print(f"{ttl}. {hop_IP} ({RTT:.2f} ms) - {city}, {country}")
            print("Destination Reached.")
            
            #add to map
            if lat and lon:
                folium.Marker(location=[lat, lon], popup=f"{hop_ip}\n{city}, {country}").add_to(map)
                break 
            
        #if destination is not reached add one to ttl 
        ttl =+ 1 
        #Max hops reached message
        if ttl > max_hops:
            print("Max number of hops reached")
            break 

if __name__ == "__main__":
    #user input destination ip
    destination_ip = input("Enter the destination IP address: ")
    traceroute(destination_ip)
    
    # Save the map as an HTML file
    traceroute_map.save("traceroute_map.html")
                
            
            
            
        
   
        
