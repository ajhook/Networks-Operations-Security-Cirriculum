# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:50:25 2023

@author: alexa
"""
#import libraries
from http.server import HTTPServer, BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        #set response code and headers
        self.send_response(200)
       
        #response content
        content = "<html><body><h1>Hello, World!</h1></body></html>"
        self.wfile.write(content.encode('utf-8'))
        
#run server
def run_server(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
