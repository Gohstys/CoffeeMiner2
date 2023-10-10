#!/usr/bin/env python
import http.server
import socketserver
import os
import ssl

PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'miner_script')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

# Cargar el certificado y la clave
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.crt', keyfile='./server.key', server_side=True)

print("serving at port", PORT)
httpd.serve_forever()
