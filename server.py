import socket
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

host = "10.101.0.70"
port = 5000

mySocket = socket.socket()
mySocket.bind((host, port))


def main():
    mySocket.listen()
    conn, addr = mySocket.accept()
    print("Connection from:" + str(addr))
    query = conn.recv(1024).decode()
    if not query:
        main()

    conn.send("True".encode())
    values = conn.recv(1024)
    values = pickle.loads(values)

    cursor.execute(query, values)
    db.commit()

    main()


if __name__ == '__main__':
    main()
