# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:45:14 2018

@author: bsilski
"""


import socket
import requests
import threading

RESPONSE = b"""\
HTTP/1.1 200 OK
Content-Type: text/html
Content-length: 15

<h1>Mock Sock!</h1>""".replace(b"\n", b"\r\n")
    


class MockSockContext(threading.Thread):
       
    
    def __init__(self, port=80, host='localhost'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.buffer_size = 4096
        self.mock_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mock_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def __enter__(self):
        self.run()
        return self

    def __exit__(self, *args):
        self.mock_sock.close()
    
    def start_sock(self):
        try:
            self.mock_sock.bind((self.host, self.port))
        except socket.error:
            print(socket.error)
        
        self.mock_sock.listen(0)
        print("listen")
        conn, addr = self.mock_sock.accept()
        data = conn.recv(self.buffer_size)
        print(data)
        with conn:
            conn.sendall(RESPONSE)
            
    def run(self):
        threading.Thread(name='start_sock', target=self.start_sock).start()
  
# EXAMPLE
with MockSockContext() as ms:
    d = requests.get("http://localhost")
    print(d.headers, d.content)



