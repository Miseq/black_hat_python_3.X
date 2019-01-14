import sys
import socket
import getopt
import threading
import subprocess
import argparse
import pprint




def client_sender(buffer, target, port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # próba połączenia do docelowego hosta
        client.connect((target,port))
        if buffer:
            client.send(buffer)

        while True:
            # czekanie na odpowiedź
            # TODO rewrite with do..while
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            pprint.pprint(response)

            # czekanie na dalszy input
            buffer = ""
            buffer += "\n"
            client.send(buffer)


    except:
        print("[*] Exception! Exiting.")
        client.close()


def server_loop( port, execute, command, upload_destination="", target = "0.0.0.0"):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket, execute, command, upload_destination))
        client_thread.start()


def run_command(command):

    # trim the newline
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Failed to execute command \r\n"

    # send the output back to the client
    return  output


def client_handler(client_socket,  execute, command, upload_destination=""):

    # sprawdzanie wysyłania
    if len(upload_destination):

        file_buffer = ""


        # w pętli sprawdzamy czy odczytujemy jakieś dane, następnie otwieramy plik i zapisujemy w nim otrzymywane dane
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_description = open(upload_destination, "wb")
            file_description.write(file_buffer)
            file_description.close()

            # potwierdź zapisanie plików
            client_socket.send("Successfully saved file to ", upload_destination)

        except:
            client_socket.send("Failed to save to ", upload_destination)


    if len(execute):

        # wykonaj komendę
        output = run_command(execute)
        client_socket.send(output)


    # jeśli client zażądał wykonania komendy
    if command:
        while True:
            # pokaż pojedyncze powiadomienie

            client_socket.send("<BHP:#>".encode())

            # szukamy \n jako końca komendy
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += str(client_socket.recv(1024))

            # odeślij komendę
            response = run_command(cmd_buffer)
            # wyślij odpowiedź do clienta
            client_socket(response)

def main():

    parser = argparse.ArgumentParser(description="Netcat replace written in python3")
    parser.add_argument('-l', '--listen',help="listen on[host]:[port] for incoming connections",
                        dest='listen', action='store_true',  required=False)

    parser.add_argument('-e', '--execute', help="execute the given file upon reciving a connection",
                        dest='execute', default='', required=False)

    parser.add_argument('-c', '--command',   help="initialize a command shell",
                        dest='command', action='store_true', required=False)

    parser.add_argument('-u', '--upload', help='upon reciving connection upload a file and write to destination',
                        dest='upload', action='store_true', required=False)

    parser.add_argument('-t', '--target', help="stores ip address of target",
                        dest='target', default="", required=False)

    parser.add_argument('-p', '--port', help='stores port of a target',
                        dest='port', type=int, default=0, required=False)
    args = parser.parse_args()

    if not len(sys.argv[1:]):
        print(parser.print_help())

    # będziemy nasłuchiwać i potencjalnie wysyłac pliki i wykonywać polecenia zaleznie od opcji powyżej


    # czytaj buffer z lini poleceń, zablokuje się więc użyj CTRL-D jeśli nie wysyłasz danych do stdin
    if not args.listen and (args.port and len(args.target)):
        buffer = sys.stdin.read()
        client_sender(buffer, args.target, args.port)

    if args.listen:
        server_loop(args.port, args.execute, args.command, args.target)

if __name__ == '__main__':
    main()
