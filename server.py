#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    fichero_audio = sys.argv[3]
except IndexError:
    sys.exit('Usage: python3 server.py IP port audio_file')

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        #Filtramos por metodos.
        for line in self.rfile:
            method = line.decode('utf-8').split(' ')[0]
            if method not in ['INVITE', 'BYE', 'ACK']:
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n')
            if method == 'INVITE':
                self.wfile.write(b'SIP/2.0 100 Triying\r\n')
                self.wfile.write(b'SIP/2.0 180 Ringing\r\n')
                self.wfile.write(b'SIP/2.0 200 OK\r\n')
                print("El cliente nos manda " + line.decode('utf-8'))
            elif method == 'ACK':
                # aEjecutar es un string con lo que se ha de ejecutar en la shell
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + fichero_audio
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            elif method == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n')
                print("El cliente nos manda " + line.decode('utf-8'))
            break


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
