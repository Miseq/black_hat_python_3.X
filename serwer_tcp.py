"""
***
Serwer TCP
Skrypt z książki Black Hat Python
Przepisany na składnie Python 3.x
oryginał napisany był w Python 2.x
Krzysztof Nowakowski
***
"""
import socket
import threading


# wątek do obsługi klienta
def handle_client(client_socket):
    # wpisani czego klient żąda
    request = client_socket.recv(1024)

    print("[*] Recived ", request)

    # odesłanie pakietu(odpowiedź)
    client_socket.send("ACK!")

    client_socket.close()


def main():
    bind_ip = "0.0.0.0"
    bind_port = 9999

    serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serwer.bind((bind_ip, bind_port))
    serwer.listen(5)

    print("[*] Listening at " + bind_ip + ":", str(bind_port))

    while True:
        client, addr = serwer.accept()
        print("[*] Accepted connection from ", addr[0], ":", addr[1])

        # spin up client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client(), args=(client, ))


if __name__ == '__main__':
    main()
