import socket
import traceback
from backend.url_handler import url_handler as url


def start_socket():
    hostname = "172.105.24.31"
    port = 5555

    # create an INET, STREAMing socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversock:

        print("listening on interface " + hostname)

        # bind the socket to a public host, and a well-known port
        # This accepts a tuple...
        serversock.bind((hostname, port))
        # become a server socket
        serversock.listen(5)

        while True:
            conn, addr = serversock.accept()
            # multi thread here!
            with conn:  # this is a socket! With syntax does not work on python 2
                try:
                    # print('Connected by', addr)
                    data = conn.recv(1024)
                    print("heard:")
                    headers = data.decode('UTF-8').splitlines()
                    print(headers[0])

                    response = url(headers)

                    print(f'sending a status of {response["response_status"]}')
                    response_header = f"HTTP/1.1 {response['response_status']}\nContent-Type: text/html\n\n"
                    conn.sendall(response_header.encode('utf-8'))

                    if response['response_content']:
                        conn.sendall(response['response_content'])

                except Exception as e:
                    print(e)
                    traceback.print_exc()
                finally:
                    print()
