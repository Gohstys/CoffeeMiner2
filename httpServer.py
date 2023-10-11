#!/usr/bin/env python
import http.server
import socketserver
import os
import ssl

PORT = 443

web_dir = os.path.join(os.path.dirname(__file__), 'miner_script')
os.chdir(web_dir)


# Clave privada y certificado en formato PEM
certfile = '/ruta/al/certificado.pem'
keyfile = '/ruta/a/clave-privada.pem'

# Configura el contexto SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile, keyfile)



Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

# Cargar el certificado y la clave
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.crt', keyfile='./server.key', server_side=True)

print("serving at port", PORT)
httpd.serve_forever()
