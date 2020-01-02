import socket
import pickle
from datetime import date


def main(query, values):

    mySocket.send(query.encode())
    val = bool(mySocket.recv(1024).decode())
    print(val)
    if val is not True:
        return

    values = pickle.dumps(values)
    mySocket.send(values)

    print("hello1")
    val = bool(mySocket.recv(1024).decode())
    print(val)
    if val is not True:
        print("hello2")
        return

    print("hello3")
    results = mySocket.recv(1024)
    results = pickle.loads(results)
    return results


host = '127.0.0.1'
port = 5431

mySocket = socket.socket()
mySocket.connect((host, port))

query1 = '''SELECT setupID FROM Setups WHERE userID LIKE ?'''
values1 = [1001]


query2 = '''INSERT INTO Scores(userID, setupID, score, distance, ammo, light, weather, range, target, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
values2 = [1001, 2, 49.5, 300, "RWS", "Good", "Warm", "Connaught A", 18, date(2019, 8, 12)]

if __name__ == '__main__':
    main(query2, values2)
