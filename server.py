import socket
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

host = "10.37.6.61"
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

    print(query, values)
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.send("True".encode())

    if len(result) > 0:
        conn.send("True".encode())
        result = str(result)

        conn.send(result.encode())

    else:
        db.commit()
        main()

    db.commit()
    main()


if __name__ == '__main__':
    main()
