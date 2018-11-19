#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


# Cliente UDP simple.

# Dirección IP del servidor.
try:
    METHOD = sys.argv[1]
    RECEIVER = sys.argv[2].split('@')[0]
    IP = sys.argv[2].split('@')[1].split(':')[0]
    PORT = int(sys.argv[2].split(':')[1])
except IndexError:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar
LINE = METHOD + ' sip:' + RECEIVER + '@' + IP + ' SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    i_data = data.decode('utf-8').split()

    if i_data[1] == '100':
        if i_data[4] == '180':
            if i_data[7] == '200':
                print('Send ACK')
                my_socket.send(bytes('ACK' + ' sip:' + RECEIVER
                + '@' + IP + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
