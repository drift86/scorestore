import socket       # import used modules
import sqlite3
import pickle

with sqlite3.connect('scorestore.db') as db:    # connect to scorestore database using SQLite 3
    cursor = db.cursor()

host = "127.0.0.1"      # set host IP and port for server
port = 5432

mySocket = socket.socket()      # start server
mySocket.bind((host, port))     # tell server what IP and port to use


def main(conn):
    query = conn.recv(1024).decode()    # get sql query without values from client
    if not query:       # if query is empty
        try:
            main(conn)  # go back to beginning

        except:
            init()      # if any errors occur, re initialise connection

    conn.send("True".encode())          # tell client query has been recieved
    values = conn.recv(1024)            # get values that go with query
    values = pickle.loads(values)       # turn the values into usable data
    cursor.execute(query, values)       # execute query using values sent from client using SQLite 3
    results = cursor.fetchall()         # get the results from query
    results = pickle.dumps(results)     # turn results into form that can be sent using sockets
    if not results:         # if no results generated go back to beginning and wait for new query
        main(conn)
    conn.send(results)      # send results back to client
    db.commit()             # commit any changes made to DB
    try:
        main(conn)          # try to go back and wait for new query

    except:
        init()              # if any errors occur, restart connection


def init():
    mySocket.listen()       # wait for connection for client
    conn, addr = mySocket.accept()      # when client connects record their info
    print("Connection from:" + str(addr))   # output clients IP
    main(conn)      # start main and wait for query to be sent


if __name__ == '__main__':
    init()
