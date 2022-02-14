import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = input('Enter server ip: ')

try:
    # подключаемся к серверу
    clientsocket.connect((server_ip , 9090))
    print(f'connection with {server_ip} successful')


    # отправляем серверу своё имя/ID
    client_name = input("Enter name or ID:: ")
    clientsocket.send(client_name.encode())

    # получаем имя сервера
    server_name = clientsocket.recv(1024).decode()
    print(f"""Connection to the {server_name} is established,
enter "exit" to exit""")

    # общение с сервером
    try:
        while True:
            message_client = input("Я: ")
            if message_client == 'exit':
                clientsocket.close()
                break
            clientsocket.send(message_client.encode())
            message_server = clientsocket.recv(1024).decode()
            print(f"{server_name}: {message_server}")
    except:
        clientsocket.close()
        print(f"connection with {server_name} lost")
except:
    clientsocket.close()
    print(f'failed to connect to {server_ip}')
