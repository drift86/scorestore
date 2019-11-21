import sqlite3

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

cursor.execute('''INSERT INTO Users(userID, name, clubID, email, password)
                  VALUES(1000, 'Edward Robinson', 1, 'ebrobinson.2lbc@gmail.com', 'geoffery');''')
db.commit()
