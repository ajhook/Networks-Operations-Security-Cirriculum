# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:33:22 2023

@author: alexa
"""
#import libraries
import requests
from bs4 import BeautifulSoup

#set base url
base_url = 'https://google.com/search?q='

#function to retrieve results
def get_results(search,num_results=10):
    
    #cerate search request
    url = base_url+search

    response = requests.get(url)
    
    #create soup
    soup = BeautifulSoup(response.content, 'html.parser')
    search_results = soup.select('div.tF2Cxc')
    
    titles = []
    for result in search_results[:num_results]:
        title_element = result.select_one('h3')
        if title_element:
            title = title_element.get_text()
            titles.append(title)
    
    return titles 

def main():
    #user input
    search = input("Enter your search prompt: ")
    top_results = get_results(search)
    
    #print results
    if not top_results:
        print("No search results found.")
    else:
        print("\nTop 10 search results:")
        for i, result in enumerate(top_results, 1):
            print(f"{i}. {result}")

  

if __name__ == "__main__":
    main()