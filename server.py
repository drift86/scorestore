import socket
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

host = "127.0.0.1"
port = 5432

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
    results = cursor.fetchall()
    results = pickle.dumps(results)
    conn.send(results)
    db.commit()
    main()


if __name__ == '__main__':
    main()
