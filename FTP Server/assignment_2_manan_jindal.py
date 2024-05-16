import socket
import os
import threading

HOST = socket.gethostname()
PORT = 9999
BUFFER_SIZE = 1024
USER_DATABASE = {'manan': 'manan123'}  

def handle_client(client_socket):
    client_socket.sendall(b'Welcome to the FTP server\n')

    authentication = False
    current_user = None

    while not authentication:
        data = client_socket.recv(BUFFER_SIZE).decode().strip()
        if not data:
            break

        command_parts = data.split()
        command = command_parts[0].upper()
        arguments = command_parts[1:]

        if command == 'USER':
            response = handle_user(*arguments)
        elif command == 'PASS':
            response, authentication, current_user = handle_pass(*arguments)
        else:
            response = 'Please give login commands.'

        client_socket.sendall(response.encode())

    if authenticated:
        client_socket.sendall(b'Login successfully done\n')

    while authenticated:
        data = client_socket.recv(BUFFER_SIZE).decode().strip()
        if not data:
            break

        command_parts = data.split()
        command = command_parts[0].upper()
        arguments = command_parts[1:]

        if command == 'LIST':
            response = handle_list()
        elif command == 'RETR':
            response = handle_retr(*arguments)
        elif command == 'STOR':
            response = handle_stor(*arguments, client_socket)
        elif command == 'QUIT':
            response = 'logged out successfully'
            break
        else:
            response = 'please provide further commands'

        client_socket.sendall(response.encode())

    client_socket.close()

def handle_user(username):
    if username in USER_DATABASE:
        return 'Please specify the password'
    else:
        return 'Invalid username'

def handle_pass(password):
    if USER_DATABASE.get(username) == password:
        return 'Login successful', True, username
    else:
        return 'invalid password', False, None

def handle_list():
    files = os.listdir('.')
    return '\n'.join(files)

def handle_retr(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return file.read()
    else:
        return 'File not found.'

def handle_stor(filename, client_socket):
    if not os.path.exists(filename):
        with open(filename, 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
            return 'File stored successfully.'
    else:
        return 'File already exists.'

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print('FTP server started...')

    while True:
        client_socket, address = server_socket.accept()
        print(f'Connection from {address}')
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()
