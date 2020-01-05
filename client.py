import socket
import pickle
from datetime import date


def exec_sql(query, values):
    mySocket.send(query.encode())
    val = bool(mySocket.recv(1024).decode())
    if val is not True:
        return
    values = pickle.dumps(values)
    mySocket.send(values)
    results = mySocket.recv(1024)
    results = pickle.loads(results)
    if len(results) > 0:
        return results
    else:
        return


host = '127.0.0.1'
port = 5432

mySocket = socket.socket()
mySocket.connect((host, port))

query1 = '''SELECT setupID FROM Setups WHERE userID LIKE ?'''
values1 = [1001]


query2 = '''INSERT INTO Scores(userID, setupID, score, distance, ammo, light, weather, range, target, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
values2 = [1001, 2, 49.5, 300, "RWS", "Good", "Warm", "Connaught A", 18, date(2019, 8, 12)]

if __name__ == '__main__':
    print(main(query1, values1))
