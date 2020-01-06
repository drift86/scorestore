import socket
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

host = "127.0.0.1"
port = 5432

mySocket = socket.socket()
mySocket.bind((host, port))


def main(conn):
    query = conn.recv(1024).decode()
    if not query:
        try:
            main(conn)

        except:
            init()

    conn.send("True".encode())
    values = conn.recv(1024)
    values = pickle.loads(values)
    cursor.execute(query, values)
    results = cursor.fetchall()
    results = pickle.dumps(results)
    conn.send(results)
    db.commit()
    try:
        main(conn)

    except:
        init()


def init():
    mySocket.listen()
    conn, addr = mySocket.accept()
    print("Connection from:" + str(addr))
    main(conn)


if __name__ == '__main__':
    init()
