import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# вычисляем и печатаем ip сервера для подключения к нему
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
print(f'IP to access the chat: {server_ip}')
# server_ip = 'localhost'

try:
    serversocket.bind((server_ip, 9090))
    print('Bind successful' )

    # указываем своё имя/ID
    server_name = input("Enter name or ID: ")

    serversocket.listen(5)
    while True:
        # ожидаем подключение от клиента
        print("Waiting for connection... ")
        clientsocket, address = serversocket.accept()

        # получем имя/ID клиента, будем указывать его как отправителя сообщений
        client_name = clientsocket.recv(1024).decode()
        print(f"""{client_name} has connected to chat, enter "next"
to skip client or "exit" to exit program""")

        # отправляем клиенту наше имя/ID
        clientsocket.send(server_name.encode())

        # общение с клиентом
        while True:
            try:
                message_client = clientsocket.recv(1024).decode()
                print(f"{client_name}: {message_client}")
                message_server = input("Me: ")
                if message_server == 'next':
                    clientsocket.close()
                elif message_server == 'exit':
                    clientsocket.close()
                    exit()
                clientsocket.send(message_server.encode())
            except:
                print(f'user {client_name} has left the chat')
                clientsocket.close()
                break

except:
    serversocket.close()
    print('Bind fail')
