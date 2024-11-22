import socket
import threading

host = '127.0.0.1'
port = 55555

chat_rooms = {}
clients = {}

def send_room(client):
    if len(chat_rooms) != 0:
      room_list = ','.join(chat_rooms.keys())
      client.send(f"Existing chat rooms: {room_list}".encode())
    else:
      client.send("There is no chat room.".encode())

def handle_client(client, address):
        try:
            send_room(client)
            room = client.recv(1024).decode()
            nickname = client.recv(1024).decode()
            if room not in chat_rooms:
                chat_rooms[room] = []
                print(f"Chat room : {room} is established!")
            chat_rooms[room].append(client)
            clients[client] = (room, nickname)
            announcement(f"{nickname} has joined this chat room.", room)

            while True:
                message = client.recv(1024).decode()
                if message == "!quit":
                    announcement(f"{nickname} has left this chat room.", room)
                    print(f"Closed Connection : {address}")
                    break
                else:
                    send_message(message, room, nickname, client)

        except Exception as error:
            print(f"Error: {error}")
            client.close()

        finally:
            del clients[client]
            chat_rooms[room].remove(client)
            client.close()

def send_message(message, room, nickname, client):
    for member in chat_rooms[room]:
        try:
          if member != client:
              member.send(f"{nickname}: {message}".encode())
              #member.send(message.encode())
          else:
            pass
        except Exception as error:
          print(f"Error: {error}")
          client.close()

def announcement(message, room):
    try:
      for member in chat_rooms[room]:
        member.send(f"----------------{message} To exit this room, type !quit----------------\n".encode())
    except Exception as error:
      print(f"Error: {error}")
      client.close()
        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server is ready to listen on {host}:{port}")

while True:
    client, address = server.accept()
    print(f"New Connection : {address}")
    client_handler = threading.Thread(target=handle_client, args = (client, address))
    client_handler.start()
