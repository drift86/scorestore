import socket
import pickle

def main():
    host = '10.37.6.61'
    port = 5432

    mySocket = socket.socket()
    mySocket.connect((host, port))

    userID = 1001
    setupID = 1
    score = 50.4
    distance = 500
    ammo = "GGG"
    light = "Good"
    weather = "Good"
    range = "Bisley"
    target = 54
    date = "21/02/2019"

    mySocket.send('''SELECT userID FROM Setups WHERE setupID LIKE ?'''.encode())
    val = bool(mySocket.recv(1024).decode())
    if val is not True:
        return

    values = [setupID]
    values = pickle.dumps(values)
    mySocket.send(values)

    print("hello")
    val = bool(mySocket.recv(1024).decode())
    print(val)
    if val is not True:
        print("hello")
        return


    print("hello")
    results = mySocket.recv(1024).decode()
    print(results)


if __name__ == '__main__':
    main()
