import socket
import pickle

def main():
    host = '10.101.0.70'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host, port))

    userID = 1001
    setupID = 1
    score = 50.8
    distance =600
    ammo = "GGG"
    light = "Good"
    weather = "Good"
    range = "Bisley"
    target = 54
    date = "19/02/2019"

    mySocket.send('''INSERT INTO Scores(userID, setupID, score, distance, ammo, light, weather, range, target, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''.encode())
    val = bool(mySocket.recv(1024).decode())
    if val is not True:
        return

    values = [userID, setupID, score, distance, ammo, light, weather, range, target, date]
    values = pickle.dumps(values)
    mySocket.send(values)


if __name__ == '__main__':
    main()
