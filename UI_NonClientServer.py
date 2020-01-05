import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.config import Config

import hashlib

import sqlite3

from datetime import date

with sqlite3.connect('scorestore.db') as db:
    cursor = db.cursor()

kivy.require("1.11.0")

Builder.load_string("""
<RegisterScreen>
    name: 'register'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        text: "Name"
        pos_hint: {"x":-0.3, "y":0.275}

    TextInput:
        id: name
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.75}

    Label:
        text: "Email Address"
        pos_hint: {"x":-0.3, "y":0.1925}

    TextInput:
        id: email
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.667}

    Label:
        text: "Password"
        pos_hint: {"x":-0.3, "y":0.11}

    TextInput:
        id: password
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.584}
        password: True

    Label:
        text: "Club ID"
        pos_hint: {"x":-0.3, "y":0.0275}

    TextInput:
        id: clubid
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.501}

    Button:
        font_size: 30
        size_hint: 0.4, 0.1
        pos_hint: {"x":0.3, "y":0.35}
        text: "Register Account"
        on_press: 
            root.register_account(name.text, email.text, password.text, clubid.text)

    Button:
        font_size: 20
        size_hint: 0.15, 0.05
        pos_hint: {"x":0.82, "y":0.500}
        text: "Find Club ID"
        on_press: root.manager.current = 'find-club'

    Label:
        id: error
        text: ""
        pos_hint: {"x": 0, "y": -0.2}

    Button:
        font_size: 20
        text: "Return to login"
        size_hint: 0.2, 0.05
        pos_hint: {"x": 0.4, "y":0.15}
        on_press: root.manager.current = 'login'

<LoginScreen>
    name: 'login'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        text: "User Email Address"
        pos_hint: {"x":-0.3, "y":0.1925}

    TextInput:
        id: email
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.667}

    Label:
        text: "Password"
        pos_hint: {"x":-0.3, "y":0.11}

    TextInput:
        id: password
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.584}
        password: True

    Button:
        font_size: 30
        size_hint: 0.4, 0.1
        pos_hint: {"x":0.3, "y":0.42}
        text: "Log in"
        on_press:
            root.login(email.text, password.text)

    Label:
        font_size: 20
        text: "or"
        pos_hint: {"x":0, "y":-0.12}

    Button:
        font_size: 30
        size_hint: 0.4, 0.1
        pos_hint: {"x":0.3, "y":0.23}
        text: "Register"
        on_press: 
            root.manager.current = 'register'

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}

<FindClubScreen>
    name: 'find-club'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        text: "Search club name"
        pos_hint: {"x":-0.25, "y":0.275}

    TextInput:
        id: club
        size_hint: 0.5, 0.1
        pos_hint: {"x":0.35, "y":0.7}

    Label:
        id: no_clubs
        text: ''
        pos_hint: {"x": 0.05, "y": 0}

    Label:
        id: index
        text: ""
        pos_hint: {"x": 0.05, "y": 0.07}

    Label:
        id: result_list
        text: ""
        pos_hint: {"x": 0.08, "y": -0.05}

    Button:
        font_size: 30
        size_hint: 0.3, 0.075
        pos_hint: {"x": 0.4, "y": 0.6}  
        text: "Search Clubs"
        on_press: 
            root.get_club(club.text)

    Label:
        text: "Can't see your club? Try changing your search terms"  
        pos_hint: {"x": 0.05, "y": -0.4}    

    Button:
        font_size: 30
        size_hint: 0.3, 0.075
        pos_hint: {"x": 0.4, "y": 0.15}
        text: "Register Account"
        on_press:
            root.manager.current = 'register'

<HomeScreen>
    name: 'home'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        id: user
        text: "Logged in as: "
        font_size: 15
        pos_hint: {"x": 0.35, "y": 0.35}

    Button:
        font_size: 30
        size_hint: 0.4, 0.1
        pos_hint: {"x": 0.3, "y": 0.6}
        text: "Enter new score"
        on_press:
            root.enter_score()

    Button:
        font_size: 30
        size_hint: 0.4, 0.1
        pos_hint: {"x": 0.3, "y": 0.4}
        text: "View scores"

    Button:
        font_size: 12
        size_hint: 0.2, 0.05
        pos_hint: {"x": 0.05, "y": 0.8}
        text: "Add new or view setups"
        on_press:
            root.manager.current = 'setups'

<SetupsMenuScreen>
    name: 'setups'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Button:
        font_size: 25
        size_hint: 0.3, 0.1
        pos_hint: {"x":0.35 , "y": 0.65}
        text: "Create new setup"
        on_press:
            root.manager.current = 'new_setup'

    Button:
        font_size: 25
        size_hint: 0.3, 0.1
        pos_hint: {"x":0.35 , "y": 0.5}
        text: "View setups"
        on_press:
            root.view_setups()

    Button:
        font_size: 25
        size_hint: 0.3, 0.1
        pos_hint: {"x":0.35 , "y": 0.35}
        text: "Edit setup"
        on_press:
            root.edit_setups()

    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'        

<NewSetupScreen>
    name: 'new_setup'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        text: "Rifle"
        pos_hint: {"x":-0.3, "y":0.275}

    Label:
        text: "(Suggested: Name and serial num)"
        font_size: 12.5
        pos_hint: {"x":-0.33, "y": 0.255}

    TextInput:
        id: rifle
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.75}

    Label:
        text: "Jacket"
        pos_hint: {"x":-0.3, "y":0.1925}

    TextInput:
        id: jacket
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.667}

    Label:
        text: "Sling setting"
        pos_hint: {"x":-0.3, "y":0.11}

    TextInput:
        id: sling
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.584}

    Label:
        text: "Glove"
        pos_hint: {"x":-0.3, "y":0.0275}

    TextInput:
        id: glove
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.501}

    Button:
        font_size: 30
        size_hint: 0.3, 0.1
        pos_hint: {"x": 0.35, "y": 0.3}
        text: "Add setup"        
        on_press:
            root.add_new_setup(rifle.text, jacket.text, sling.text, glove.text)

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}

    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'  

<ViewSetupScreen>
    name: 'view_setups'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        id: id_view
        text: "" 
        pos_hint: {"x": -0.15, "y": 0.3}

    Label
        text: "Setup ID:"
        pos_hint: {"x": -0.1, "y":0.25}

    TextInput:
        id: setup_id_choice
        size_hint: 0.1, 0.04
        pos_hint: {"x": 0.45, "y": 0.73}

    Button:
        font_size: 15
        size_hint: 0.1, 0.04
        pos_hint: {"x": 0.555, "y": 0.73}
        text: "View setup"
        on_press:
            root.show_setup(setup_id_choice.text)


    Label:
        text: "Rifle:"
        pos_hint: {"x":-0.3, "y":0.155}

    Label:
        id:rifle
        pos_hint: {"x":0, "y":0.155}

    Label:
        text: "Jacket:"
        pos_hint: {"x":-0.3, "y":0.0825}

    Label:
        id: jacket
        pos_hint: {"x":0, "y":0.0825}

    Label:
        text: "Sling setting:"
        pos_hint: {"x":-0.3, "y":0.01}

    Label:
        id: sling
        pos_hint: {"x":0, "y":0.01}

    Label:
        text: "Glove:"
        pos_hint: {"x":-0.3, "y":-0.0722}

    Label:
        id: glove
        pos_hint: {"x":0, "y":-0.0722}

    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}

<EditSetupScreen>
    name: 'edit_setups'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        id: id_view
        text: "" 
        pos_hint: {"x": -0.15, "y": 0.3}

    Label:
        text: "Setup ID:"
        pos_hint: {"x": -0.1, "y":0.25}

    TextInput:
        id: setup_id_choice
        size_hint: 0.1, 0.04
        pos_hint: {"x": 0.45, "y": 0.73}

    Button:
        font_size: 15
        size_hint: 0.1, 0.04
        pos_hint: {"x": 0.555, "y": 0.73}
        text: "View setup"
        on_press:
            root.show_setup(setup_id_choice.text)

    Label:
        text: "Rifle:"
        pos_hint: {"x":-0.3, "y":0.155}

    TextInput:
        id:rifle
        text: ""
        pos_hint: {"x":0.3, "y":0.645}
        size_hint: 0.5, 0.05

    Label:
        text: "Jacket:"
        pos_hint: {"x":-0.3, "y":0.0825}

    TextInput:
        id: jacket
        text: ""
        pos_hint: {"x":0.3, "y":0.565}
        size_hint: 0.5, 0.05

    Label:
        text: "Sling setting:"
        pos_hint: {"x":-0.3, "y":0.01}

    TextInput:
        id: sling
        text: ""
        pos_hint: {"x":0.3, "y":0.485}
        size_hint: 0.5, 0.05

    Label:
        text: "Glove:"
        pos_hint: {"x":-0.3, "y":-0.0722}

    TextInput:
        id: glove
        text: ""
        pos_hint: {"x":0.3, "y":0.405}
        size_hint: 0.5, 0.05

    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}

    Button:
        font_size: 20
        size_hint:0.2, 0.1
        pos_hint: {"x": 0.4, "y": 0.275}
        text: "Commit Changes"
        on_press:
            root.commit_changes(rifle.text, jacket.text, sling.text, glove.text)

<EnterScoreScreen>
    name: 'enter-score'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        pos_hint: {"x":0, "y": 0.3}
        text: "Enter your score and format:"

    Label:
        text: "2 & 7"
        pos_hint: {"x": -0.1, "y": 0.2}

    CheckBox:
        id: seven
        pos_hint: {"x": 0.385, "y": 0.65}
        size_hint: 0.03, 0.03

    Label:
        text: "2 & 10"
        pos_hint: {"x": 0, "y": 0.2}

    CheckBox:
        id: ten
        pos_hint: {"x": 0.485, "y": 0.65}
        size_hint: 0.03, 0.03

    Label:
        text: "2 & 15"
        pos_hint: {"x": 0.1, "y": 0.2}

    CheckBox:
        id: fifteen
        pos_hint: {"x": 0.585, "y": 0.65}
        size_hint: 0.03, 0.03

    TextInput:
        id: score
        font_size: 30
        size_hint: 0.12, 0.08
        pos_hint: {"x": 0.44, "y":0.5}

    Button:
        text: "Continue"
        size_hint: 0.2, 0.1
        pos_hint: {"x": 0.4, "y": 0.3}
        on_press: root.get_score(score.text)

    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}

<EnterDetailsScreen>
    name: 'enter_details'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        pos_hint: {"x":0, "y": 0.35}
        text: "Enter the details of your shoot:"

    Label:
        text: "Distance"
        pos_hint: {"x": -0.3, "y": 0.3}

    Label
        text: "(Yards)"
        pos_hint: {"x": -0.3, "y": 0.265}

    Label:
        text: "300"
        pos_hint: {"x": -0.15, "y": 0.3}

    CheckBox:
        id: three
        pos_hint: {"x": 0.335, "y": 0.75}
        size_hint: 0.03, 0.03

    Label:
        text: "500"
        pos_hint: {"x": -0.05, "y": 0.3}

    CheckBox:
        id: five
        pos_hint: {"x": 0.435, "y": 0.75}
        size_hint: 0.03, 0.03

    Label:
        text: "600"
        pos_hint: {"x": 0.05, "y": 0.3}

    CheckBox:
        id: six
        pos_hint: {"x": 0.535, "y": 0.75}
        size_hint: 0.03, 0.03

    Label:
        text: "900"
        pos_hint: {"x": 0.15, "y": 0.3}

    CheckBox:
        id: nine
        pos_hint: {"x": 0.635, "y": 0.75}
        size_hint: 0.03, 0.03

    Label:
        text: "1000"
        pos_hint: {"x": 0.25, "y": 0.3}

    CheckBox:
        id: ten
        pos_hint: {"x": 0.735, "y": 0.75}
        size_hint: 0.03, 0.03

    Label:
        text: "Ammo:"
        pos_hint: {"x":-0.3, "y":0.1925}

    TextInput:
        id: ammo
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.667}

    Label:
        text: "Light:"
        pos_hint: {"x":-0.3, "y":0.11}

    TextInput:
        id: light
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.584}

    Label:
        text: "Weather:"
        pos_hint: {"x":-0.3, "y":0.0275}

    TextInput:
        id: weather
        size_hint: 0.5, 0.05
        pos_hint: {"x":0.3, "y":0.501}   

    Label:
        text: "Range:"
        pos_hint: {"x": -0.3, "y": -0.055}

    TextInput:
        id: range
        size_hint: 0.5, 0.05
        pos_hint: {"x": 0.3, "y": 0.418} 

    Label:
        text: "Target/Lane"
        pos_hint: {"x": -0.3, "y": -0.1375}

    TextInput:
        id: target
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.3, "y": 0.335}

    Label:
        text: "Date:"
        pos_hint: {"x": 0, "y": -0.1375}

    TextInput:
        id: day
        size_hint: 0.05, 0.05
        pos_hint: {"x": 0.55, "y": 0.335}

    TextInput:
        id: month
        size_hint: 0.05, 0.05
        pos_hint: {"x": 0.625, "y": 0.335}

    TextInput:
        id: year
        size_hint: 0.075, 0.05
        pos_hint: {"x": 0.7, "y": 0.335}

    Label:
        text: "(Day, Month, Year)"
        pos_hint: {"x": 0.1, "y": -0.22}

    Label:
        text: "Setup ID:"
        pos_hint: {"x": -0.3, "y": -0.22}

    TextInput:
        id: setup_id
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.3, "y": 0.252}

    Button:
        text: "Enter score/shoot"
        size_hint: 0.2, 0.1
        pos_hint: {"x": 0.4, "y": 0.12}
        on_press:
            root.get_details(setup_id.text, ammo.text, light.text, weather.text, range.text, target.text, day.text, month.text, year.text)

    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.42}


""")


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.email = ""
        self.password = ""
        self.password_attempt = ""
        self.user_name = ""
        self.user_id = 0

    def get_password(self):
        cursor.execute('''SELECT password FROM Users WHERE email LIKE ?''', (self.email,))
        user_pw = cursor.fetchall()
        user_pw = str(user_pw)
        user_pw = user_pw.strip("[]")
        user_pw = user_pw.strip("()")
        user_pw = user_pw.strip(",")
        user_pw = user_pw.strip("'")
        return user_pw

    def get_user_name(self):
        cursor.execute('''SELECT name FROM Users WHERE email LIKE ?''', (self.email,))
        user_name = cursor.fetchall()
        user_name = str(user_name)
        user_name = user_name.strip("[]")
        user_name = user_name.strip("()")
        user_name = user_name.strip(",")
        user_name = user_name.strip("'")
        return user_name

    def get_user_id(self):
        cursor.execute('''SELECT userID FROM Users WHERE email LIKE ?''', (self.email,))
        user_id = cursor.fetchall()
        user_id = str(user_id)
        user_id = user_id.strip("[]")
        user_id = user_id.strip("()")
        user_id = user_id.strip(",")
        user_id = user_id.strip("'")
        user_id = int(user_id)
        return user_id

    def login(self, emailText, passwordText):
        try:
            self.ids.error.text = ""
            self.email = emailText
            self.password_attempt = passwordText
            self.password = self.get_password()
            self.user_name = self.get_user_name()
            self.user_id = self.get_user_id()
            self.password_attempt = hashlib.md5(self.password_attempt.encode())
            self.password_attempt = self.password_attempt.hexdigest()

        except ValueError:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            return

        if self.password == self.password_attempt:
            home_screen.ids.user.text += self.user_name
            home_screen.user_name = self.user_name
            home_screen.user_id = self.user_id
            sm.current = 'home'

        else:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            return


class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.fullname = ""
        self.email = ""
        self.password = ""
        self.clubID = 0
        self.userID = 0
        self.last_user = []
        self.last_uid = 0

    def create_uid(self, last_user):
        for i in last_user:
            last_uid = i
            break

        last_uid = str(last_uid)
        last_uid = last_uid.strip("()")
        last_uid = last_uid.strip(",")
        last_uid = int(last_uid)
        userID = last_uid + 1
        return userID

    def register_account(self, nameText, emailText, passwordText, clubidText):
        self.ids.error.text = ""
        try:
            self.fullname = nameText
            self.email = emailText.lower()
            self.password = passwordText
            self.clubID = int(clubidText)
            self.userID = self.create_uid(cursor.execute('''SELECT max(userID) as userID FROM Users;'''))

        except ValueError:
            self.ids.error.text = "Invalid input check format of inputted info"
            return

        cursor.execute('''SELECT email FROM Users WHERE email LIKE ?''', (self.email,))
        already = cursor.fetchall()

        if len(already) > 0:
            self.ids.error.text = "An account with that email already exists"
            return

        self.password = hashlib.md5(self.password.encode())
        self.password = self.password.hexdigest()

        cursor.execute('''INSERT INTO Users(userID, name, clubID, email, password) VALUES (?,?,?,?,?)''',
                       (self.userID, self.fullname, self.clubID, self.email, self.password))
        db.commit()

        sm.current = 'login'


class FindClubScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.club = ""
        self.results = []
        self.search_terms = []
        self.result_labels = []

    def get_club(self, clubText):
        self.club = clubText
        self.club = self.club.split()
        self.search_terms = []
        self.results = []
        self.result_labels = []
        for i in self.club:
            if i.lower() not in ["college", "rifle", "club", "school", "association", "and"]:
                self.search_terms.append(i)
            else:
                self.club.remove(i)

        for i in self.search_terms:
            self.results += cursor.execute('''SELECT * FROM Clubs WHERE name LIKE ?''', ('%' + i + '%',))

        self.ids.no_clubs.text = ""
        self.ids.index.text = ""
        self.ids.result_list.text = ""

        if len(self.results) == 0:
            self.ids.no_clubs.text = "No clubs with that name found"
            return

        self.ids.index.text = "ID, Club name"

        count = 0
        for i in range(len(self.results)):
            count += 1
            self.ids.result_list.text += str(self.results[i]).strip('()') + "\n"
            if count == 5:
                break


class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_name = ""
        self.user_id = 0

    def go_setup(self):
        setup_screen.user_id = self.user_id

    def enter_score(self):
        enter_details.userID = self.user_id
        sm.current = 'enter-score'


class SetupsMenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0

    def view_setups(self):
        view_setup.view_setup()
        sm.current = 'view_setups'

    def edit_setups(self):
        edit_setup.view_setup()
        sm.current = 'edit_setups'


class NewSetupScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0
        self.setup_id = 0
        self.rifle = ""
        self.jacket = ""
        self.sling = ""
        self.glove = ""

    def new_setup_id(self):
        cursor.execute('''SELECT max(setupID) as setupID FROM Setups;''')
        last_sid = cursor.fetchall()
        last_sid = str(last_sid)
        last_sid = last_sid.strip("[]")
        last_sid = last_sid.strip("()")
        last_sid = last_sid.strip(",")
        last_sid = int(last_sid)
        setup_id = last_sid + 1
        return setup_id

    def add_new_setup(self, rifleText, jacketText, slingText, gloveText):
        self.ids.error.text = ""
        try:
            self.rifle = rifleText
            self.jacket = jacketText
            self.sling = slingText
            self.glove = gloveText
            self.setup_id = self.new_setup_id()
            self.user_id = home_screen.user_id
            for i in [self.rifle, self.jacket, self.sling, self.glove]:
                if len(i) == 0:
                    self.ids.error.text = "Please input a value for all fields"
                    return

        except ValueError:
            self.ids.error.text = "Invalid input check format of inputted info"
            return

        cursor.execute('''INSERT INTO Setups(setupID, userID, rifle, jacket, sling_setting, glove)
                        VALUES (?,?,?,?,?,?)''',
                       (self.setup_id, self.user_id, self.rifle, self.jacket, self.sling, self.glove))
        db.commit()

        sm.current = 'setups'


class ViewSetupScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0
        self.user_name = ""
        self.setup_id = 0
        self.user_setups = []

    def format_setups(self, setups):
        setups = str(setups)
        setups = setups.strip("[]")
        setups = setups.strip("()")
        setups = setups.strip(",")
        setups = setups.replace(",", " ")
        setups = setups.replace("(", " ")
        setups = setups.replace(")", " ")
        if len(setups) == 0:
            setups = "No setups in DB"
            return setups

        return setups

    def view_setup(self):
        self.user_name = home_screen.user_name
        self.user_id = home_screen.user_id
        cursor.execute('''SELECT setupID FROM Setups WHERE userID LIKE ?''', (self.user_id,))
        self.user_setups = cursor.fetchall()
        self.ids.id_view.text = str(self.user_name) + "'s setup IDs: " + self.format_setups(self.user_setups)

    def show_setup(self, setup_idText):
        self.ids.error.text = ""
        self.setup_id = setup_idText
        cursor.execute('''SELECT rifle, jacket, sling_setting, glove FROM Setups WHERE setupID LIKE ?''',
                       (self.setup_id,))
        setup = cursor.fetchall()
        try:
            rifle = setup[0][0]
            jacket = setup[0][1]
            sling = setup[0][2]
            glove = setup[0][3]

        except IndexError:
            self.ids.error.text = "Cannot find that setup, check the search term"
            return

        self.ids.rifle.text = rifle
        self.ids.jacket.text = jacket
        self.ids.sling.text = sling
        self.ids.glove.text = glove


class EditSetupScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0
        self.user_name = ""
        self.setup_id = 0
        self.user_setups = []

    def format_setups(self, setups):
        setups = str(setups)
        setups = setups.strip("[]")
        setups = setups.strip("()")
        if len(setups) == 0:
            setups = "No setups in DB"
            return setups

        return setups

    def view_setup(self):
        self.user_name = home_screen.user_name
        self.user_id = home_screen.user_id
        cursor.execute('''SELECT setupID FROM Setups WHERE userID LIKE ?''', (self.user_id,))
        self.user_setups = cursor.fetchall()
        self.ids.id_view.text = str(self.user_name) + "'s setup IDs: " + self.format_setups(self.user_setups)

    def show_setup(self, setup_idText):
        self.ids.error.text = ""
        self.setup_id = setup_idText
        cursor.execute('''SELECT rifle, jacket, sling_setting, glove FROM Setups WHERE setupID LIKE ?''',
                       (self.setup_id,))
        setup = cursor.fetchall()
        try:
            rifle = setup[0][0]
            jacket = setup[0][1]
            sling = setup[0][2]
            glove = setup[0][3]

        except IndexError:
            self.ids.error.text = "Cannot find that setup, check the search term"
            return

        self.ids.rifle.text += rifle
        self.ids.jacket.text += jacket
        self.ids.sling.text += sling
        self.ids.glove.text += glove

    def commit_changes(self, rifleText, jacketText, slingText, gloveText):
        cursor.execute('''SELECT userID FROM Setups WHERE setupID LIKE ?''', (self.setup_id,))
        user_id = cursor.fetchall()
        user_id = str(user_id)
        user_id = user_id.strip("[]")
        user_id = user_id.strip("()")
        user_id = user_id.strip(",")
        user_id = user_id.strip("'")
        user_id = int(user_id)
        if self.user_id != user_id:
            self.ids.error.text = "You cannot alter this setup, it does not belong to you"
            return

        rifle = rifleText
        jacket = jacketText
        sling = slingText
        glove = gloveText

        cursor.execute('''DELETE FROM Setups WHERE setupID = ?''', (self.setup_id,))
        cursor.execute('''INSERT INTO Setups(setupID, userID, rifle, jacket, sling_setting, glove)
                                VALUES (?,?,?,?,?,?)''',
                       (self.setup_id, self.user_id, rifle, jacket, sling, glove))
        db.commit()
        sm.current = 'home'


class EnterScoreScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.max = 0
        self.ids.seven.bind(active=self.score_format)
        self.ids.ten.bind(active=self.score_format)
        self.ids.fifteen.bind(active=self.score_format)

    def score_format(self, checkbox, checked):
        self.max = 0
        if not checked:
            self.max = 0
            return

        if checkbox == self.ids.seven:
            self.max = 35
            return

        if checkbox == self.ids.ten:
            self.max = 50
            return

        if checkbox == self.ids.fifteen:
            self.max = 75
            return

        else:
            self.max = 0
            return

    def get_score(self, scoreText):
        self.ids.error.text = ""
        self.score = scoreText
        if self.max == 0:
            self.ids.error.text = "Please make sure you have chosen the correct shoot format"
            return

        try:
            if int(float(self.score)) > self.max:
                self.ids.error.text = "Please make sure you have chosen the correct shoot format"
                return

        except ValueError:
            self.ids.error.text = "Please make sure you have chosen the correct shoot format"
            return

        self.score = float(self.score)
        enter_details.score = self.score
        sm.current = 'enter_details'


class EnterDetailsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.distance = 0
        self.ammo = ""
        self.light = ""
        self.weather = ""
        self.range = ""
        self.target = 0
        self.date = ""
        self.setupID = 0
        self.userID = 0
        self.ids.three.bind(active=self.get_dist)
        self.ids.five.bind(active=self.get_dist)
        self.ids.six.bind(active=self.get_dist)
        self.ids.nine.bind(active=self.get_dist)
        self.ids.ten.bind(active=self.get_dist)

    def get_dist(self, checkbox, checked):
        self.distance = 0
        if not checked:
            self.distance = 0
            return

        if checkbox == self.ids.three:
            self.distance = 300
            return

        if checkbox == self.ids.five:
            self.distance = 500
            return

        if checkbox == self.ids.six:
            self.distance = 600
            return

        if checkbox == self.ids.nine:
            self.distance = 900
            return

        if checkbox == self.ids.ten:
            self.distance = 1000
            return

        else:
            self.distance = 0
            return

    def get_details(self, setupidText, ammoText, lightText, weatherText, rangeText, targetNum, dayText, monthText,
                    yearText):
        self.ids.error.text = ""
        try:
            self.setupID = int(setupidText)
            self.ammo = ammoText
            self.light = lightText
            self.weather = weatherText
            self.range = rangeText
            self.target = int(targetNum)
            self.date = date(int(yearText), int(monthText), int(dayText))
        except ValueError:
            self.ids.error.text = "Please make sure you have the correct format for all fields"

        if self.distance == 0:
            self.ids.error.text = "Please make sure you have selected the correct distance"
            return

        for i in (
        self.userID, self.setupID, self.distance, self.ammo, self.light, self.weather, self.range, self.target):
            try:
                if len(i) <= 0:
                    self.ids.error.text = "Please make sure all fields are filled in correctly"
                    return

            except:
                if i <= 0:
                    self.ids.error.text = "Please make sure all fields are filled in correctly"
                    return

        try:
            cursor.execute('''INSERT INTO Scores(userID, setupID, score, distance, ammo, light, weather, range, target, 
                           date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           [self.userID, self.setupID, self.score, self.distance, self.ammo, self.light, self.weather,
                            self.range, self.target, self.date])

        except sqlite3.OperationalError as e:
            print(e)
            self.ids.error.text = "Please make sure you have entered all info in the correct format"
            return

        db.commit()
        sm.current = 'home'


login_screen = LoginScreen()
register_screen = RegisterScreen()
find_club = FindClubScreen()
home_screen = HomeScreen()
enter_score = EnterScoreScreen()
enter_details = EnterDetailsScreen()
setup_screen = SetupsMenuScreen()
new_setup = NewSetupScreen()
view_setup = ViewSetupScreen()
edit_setup = EditSetupScreen()

sm = ScreenManager(transition=FadeTransition())

sm.add_widget(login_screen)
sm.add_widget(register_screen)
sm.add_widget(find_club)
sm.add_widget(home_screen)
sm.add_widget(enter_score)
sm.add_widget(enter_details)
sm.add_widget(setup_screen)
sm.add_widget(new_setup)
sm.add_widget(view_setup)
sm.add_widget(edit_setup)


class ScoreStore(App):
    def build(self):
        return sm


if __name__ == "__main__":
    ScoreStore().run()