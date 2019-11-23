import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.config import Config

import hashlib

import sqlite3

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
            root.manager.current = 'enter-score'
        
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
            root.new_setup()
        
    Button:
        font_size: 25
        size_hint: 0.3, 0.1
        pos_hint: {"x":0.35 , "y": 0.5}
        text: "View setups"
        
    Button:
        font_size: 25
        size_hint: 0.3, 0.1
        pos_hint: {"x":0.35 , "y": 0.35}
        text: "Edit setup"
        
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
            
<EnterScoreScreen>
    name: 'enter-score'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}
        
    Label:
        pos_hint: {"x":0, "y": 0}
        text: "Enter your score and details of the shoot"
        
    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'  
        
                             
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
            self.results += cursor.execute('''SELECT * FROM Clubs WHERE name LIKE ?''', ('%'+i+'%',))

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


class SetupsMenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0

    def new_setup(self):
        new_setup.user_id = self.user_id
        sm.current = 'new_setup'


class EnterScoreScreen(Screen):
    pass


class NewSetupScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = 0
        self.rifle = ""
        self.jacket = ""
        self.sling = ""
        self.glove = ""

    def add_new_setup(self, rifleText,  jacketText, slingText, gloveText):
        self.ids.error.text = ""
        try:
            self.rifle = rifleText
            self.jacket = jacketText
            self.sling = slingText
            self.glove = gloveText
            for i in [self.rifle, self.jacket, self.sling, self.glove]:
                if len(i) == 0:
                    self.ids.error.text = "Please input a value for all fields"
                    return

        except ValueError:
            self.ids.error.text = "Invalid input check format of inputted info"
            return

        cursor.execute('''INSERT INTO Users(userID, name, clubID, email, password) VALUES (?,?,?,?,?)''',
                       (self.userID, self.fullname, self.clubID, self.email, self.password))

login_screen = LoginScreen()
register_screen = RegisterScreen()
find_club = FindClubScreen()
home_screen = HomeScreen()
enter_score = EnterScoreScreen()
setup_screen = SetupsMenuScreen()
new_setup = NewSetupScreen()

sm = ScreenManager(transition=FadeTransition())

sm.add_widget(login_screen)
sm.add_widget(register_screen)
sm.add_widget(find_club)
sm.add_widget(home_screen)
sm.add_widget(enter_score)
sm.add_widget(setup_screen)
sm.add_widget(new_setup)


class ScoreStore(App):
    def build(self):
        return sm


if __name__ == "__main__":
    ScoreStore().run()
