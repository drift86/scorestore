import socket
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

host = "127.0.0.1"
port = 5431

mySocket = socket.socket()
mySocket.bind((host, port))


def main():
    mySocket.listen()
    conn, addr = mySocket.accept()
    print("Connection from:" + str(addr))
    query = conn.recv(1024).decode()
    print(query)
    if not query:
        main()

    print("yos")
    conn.send("True".encode())
    values = conn.recv(1024)
    values = pickle.loads(values)
    print(values)

    cursor.execute(query, values)
    results = cursor.fetchall()

    if len(results) > 0:
        results = pickle.dumps(results)
        conn.send(results)
        main()

    db.commit()

    print("hi")
    main()


if __name__ == '__main__':
    main()
