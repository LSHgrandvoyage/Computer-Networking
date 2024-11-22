import socket
import threading
import time

host = '127.0.0.1'
port = 55555


def receive_messages(client, nickname, user_input):
    while True:
        try: 
          message = client.recv(1024).decode()
          print(message)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

room_list = client.recv(1024).decode()
print(room_list)

room = input("Enter the chat room name(If you enter what does not exist, a new room will be created): ")
client.send(room.encode())

nickname = input("Enter your nickname that will be used in chat room: ")
client.send(nickname.encode())

user_input = ""
client.send(user_input.encode())

print("Please wait for system setup (estimated time: around 3 seconds) ")
receive_thread = threading.Thread(target=receive_messages, args=(client, nickname, user_input))
receive_thread.start()

time.sleep(2)
print("Start to chat!")

while True:
    user_input = input()
    client.send(user_input.encode())
    if user_input == '!quit':
        client.close()
        break

