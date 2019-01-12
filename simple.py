"""
***
Prosty klient TCP w pythonie wysyłający żądanie pod wskazany adres IP
Źródło oryginalne Black Hat Python
wersja oryginalna python 2.X
przepisany zgodnie z wersja 3.X
Krzysztof Nowakowski
***
"""

import socket
import pprint
import argparse


parser = argparse.ArgumentParser(description="Simple TCP client")
parser.add_argument('--local', dest="local", required=False)
# Zakładam że używamy domyślnych wartości serwera TCP z książki, w przypadku dynamicznych trzeba byłoby przemodelować projekt
args = parser.parse_args()

if args.local:
    target_host = "0.0.0.0"
    target_port = 9999
else:
    target_host = "www.google.com"
    target_port = 80

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# AF_INET - standarodowy IPv4 adres albo nazwa hosta, sock_stream oznacza że będzie to standarodowy klient TCP

client.connect((target_host,target_port))
# mówi samo za siebie

# wysyłanie wiadomości pod zadany adres
messeage = 'GET / HTTP/1.1.\r\nHOST: google.com\r\n\r\n'
byte_mess = messeage.encode()
client.send(byte_mess)

response = client.recv(4096)

pprint.pprint(response)