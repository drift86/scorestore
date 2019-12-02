import sqlite3

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()


class Database:
    def __init__(self):
        # create clubs table
        cursor.execute('''CREATE TABLE Clubs (clubID int NOT NULL,
                                                      name varchar(128) NOT NULL,
                                                      PRIMARY KEY (clubID) 
                                                      );''')
        # create users table
        cursor.execute('''CREATE TABLE Users (userID int NOT NULL, 
                                              name varchar(128) NOT NULL,
                                              clubID int NOT NULL,
                                              email varchar(128) NOT NULL,
                                              password varchar(128) NOT NULL,
                                              PRIMARY KEY (userID),
                                              FOREIGN KEY (clubID) REFERENCES Clubs(clubID)
                                              );''')
        # create setups table
        cursor.execute('''CREATE TABLE Setups (setupID int NOT NULL,
                                               userID int NOT NULL,
                                               rifle varchar(128),
                                               jacket varchar(128),
                                               sling_setting varchar(128),
                                               glove varchar(128), 
                                               PRIMARY KEY (setupID),
                                               FOREIGN KEY (userID) REFERENCES Users(userID)
                                               );''')

        cursor.execute('''CREATE TABLE  Scores (userID int NOT NULL,
                                                setupID int NOT NULL,
                                                score float(2,2) NOT NULL,
                                                distance int NOT NULL,
                                                ammo varchar(128),
                                                light varchar(128),
                                                weather varchar(128),
                                                range varchar(128),
                                                target int,
                                                date DATE,
                                                FOREIGN KEY (userID) REFERENCES Users(userID),
                                                FOREIGN KEY (setupID) REFERENCES Setups(setupID)
                                                );''')

        db.commit()


def main():
    # create instance of object Database to create SQL database
    scorestore = Database()


if __name__ == "__main__":
    main()
