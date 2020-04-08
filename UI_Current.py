import kivy   # import Kivy module for GUI
from kivy.app import App    # import specific Kivy items to be used in code
from kivy.lang import Builder
from kivy.uix.screenmanager import *

import hashlib    # import module for hashing algorithms

import math       # import modules for stats analysis
import statistics

import socket     # import  modules for client-server interface
import pickle


import datetime   # import module for assigning score dates

kivy.require("1.11.0")    # require specific version of Kivy framework

host = '127.0.0.1'  # specify ip and open port of server
port = 5432         # could be changed to suit offsite server

mySocket = socket.socket()      # set up server connection with socket module
mySocket.connect((host, port))

# read kivy language to define GUI features/layout
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
        
    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Coaches"
        on_press:
            root.manager.current = 'coach-login'

<CoachLoginScreen>
    name: 'coach-login'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}

    Label:
        text: "Coach Email Address"
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
            root.manager.current = 'coach-register'
            
    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.4}
        
<CoachRegisterScreen>
    name: 'coach-register'
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

<CoachHomeScreen>
    name: 'coach-home'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}
        
    Label:
        id: user
        text: "Logged in as: "
        font_size: 15
        pos_hint: {"x": 0.35, "y": 0.35}
        
    Label:
        text: "Shooter           Averages:      2&7       2&10      2&15          Standard Deviation"
        font_size: 20
        pos_hint: {"x": 0, "y": 0.25}
        
    ScrollView:
        size_hint: 0.8, 0.65
        pos_hint: {"x": 0.075, "y": 0.05}
        Label:
            id: stats
            font_size: 15
            size_hint: None, None
            size: self.texture_size
            text: ""     
        

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
        on_press:
            root.view_score()
        
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
        
<ViewScoreHomeScreen>
    name: 'view-score-home'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}
    
    Label:
        text: "Most recent scores:"
        pos_hint: {"x": -0.3, "y": 0.3}
        
    Label:
        text: "Score    Distance       Date"
        pos_hint: {"x": -0.035, "y": 0.275}
        
    Label:
        id: most_recent_scores
        text: ""
        pos_hint: {"x": 0, "y": -0.025}  
        
    Button:
        text: "Score analysis"
        size_hint: 0.2, 0.1
        pos_hint: {"x": 0.2, "y": 0.12}
        on_press:
            root.view_stats()
        
    Button:
        text: "View all scores"
        size_hint: 0.2, 0.1
        pos_hint: {"x": 0.6, "y": 0.12}
        on_press:
            root.view_all_scores()
        
    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home' 

<ViewStatsScreen>
    name: 'view-stats-home'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}
        
    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'
            
    Label:
        font_size: 20
        text: "Averages    (2,7)    (2,10)    (2,15):"
        pos_hint: {"x": 0, "y":0.275}
        
    Label:
        font_size: 20
        id: average
        text: ""
        pos_hint: {"x": 0, "y": 0.175}
        
    Label:
        font_size: 20
        text: "Standard deviation:"
        pos_hint: {"x": 0, "y": 0}
        
    Label:
        font_size: 20
        id: st_dev
        text: ""
        pos_hint: {"x": 0, "y": -0.075}
        
    Label:
        text: "(Most scores within this value of the mean)"
        pos_hint: {"x": 0, "y": -0.15}
        
    Label:
        font_size: 10
        text: "(Statistics may not be accurate until you have entered at least 10 scores)"
        pos_hint: {"x": 0, "y": -0.3}
        
    Label:
        id: error
        text: ""
        pos_hint: {"x":0, "y":-0.42}
    
<ViewAllScoresScreen>
    name: 'view-all-scores'
    Image:
        source: 'scorestorelogo.png'
        size_hint: 0.8, 0.8
        pos_hint: {"x":0.1 , "y":0.535}
        
    Button:
        font_size: 15
        size_hint: 0.1, 0.05
        pos_hint: {"x": 0.05, "y": 0.05}
        text: "Home"
        on_press:
            root.manager.current = 'home'
            
    Label:
        text: "Score    Distance    Weather    Light    Ammo    Range    Target     Date"
        pos_hint: {"x": 0, "y": 0.325}
        
    ScrollView:
        size_hint: 0.6, 0.65
        pos_hint: {"x": 0.2, "y": 0.125}
        Label:
            id: scores
            size_hint: None, None
            size: self.texture_size
            text: ""                                              
""")


class LoginScreen(Screen):          # create login screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.email = ""             # set up variables
        self.password = ""
        self.password_attempt = ""
        self.user_name = ""
        self.user_id = 0

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_password(self):
        user_pw = self.exec_sql('''SELECT password FROM Users WHERE email LIKE ? AND userID > 1000''', (self.email,))
        user_pw = str(user_pw)                  # get hashed password from db for the inputted email
        user_pw = user_pw.strip("[]")           # formatting of returned value so it can be compared to user inputted
        user_pw = user_pw.strip("()")           # password
        user_pw = user_pw.strip(",")
        user_pw = user_pw.strip("'")
        return user_pw                          # return formatted hashed password

    def get_user_name(self):
        user_name = self.exec_sql('''SELECT name FROM Users WHERE email LIKE ? AND userID > 1000''', (self.email,))
        user_name = str(user_name)              # get users name from db from their email address
        user_name = user_name.strip("[]")       # formatting of returned value
        user_name = user_name.strip("()")
        user_name = user_name.strip(",")
        user_name = user_name.strip("'")
        return user_name                        # return user name

    def get_user_id(self):
        user_id = self.exec_sql('''SELECT userID FROM Users WHERE email LIKE ? AND userID > 1000''', (self.email,))
        user_id = str(user_id)                  # get user ID of user trying to log in
        user_id = user_id.strip("[]")           # formatting of returned value
        user_id = user_id.strip("()")
        user_id = user_id.strip(",")
        user_id = user_id.strip("'")
        user_id = int(user_id)                  # return user ID
        return user_id

    def login(self, emailText, passwordText):
        try:
            self.ids.error.text = ""                # clear any error messages
            self.email = emailText                  # get email from GUI
            self.password_attempt = passwordText    # get password attempt from GUI
            self.password = self.get_password()     # get password hash value from DB using function
            self.user_name = self.get_user_name()   # get user name value from DB using function
            self.user_id = self.get_user_id()       # get user ID value from DB using function
            self.password_attempt = hashlib.md5(self.password_attempt.encode())
            # convert password attempt to UTF-8 and hash using MD5 hash
            self.password_attempt = self.password_attempt.hexdigest()
            # turn password attempt hash value into hex value

        except ValueError:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            # if there are any errors in inputted text, allow user to try again
            return

        if self.password == self.password_attempt:          # check if inputted value matches stored value
            home_screen.ids.user.text += self.user_name     # pass user details to home screen to be displayed
            home_screen.user_name = self.user_name
            home_screen.user_id = self.user_id
            sm.current = 'home'                             # move to home screen

        else:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            return                                          # if password is incorrect allow user to retry


class RegisterScreen(Screen):       # create register screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.fullname = ""          # set up variables
        self.email = ""
        self.password = ""
        self.clubID = 0
        self.userID = 0
        self.last_user = []
        self.last_uid = 0

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def create_uid(self, last_user):
        for i in last_user:             # get user ID from sql passed to function
            last_uid = i
            break

        last_uid = str(last_uid)            # convert sql query result into usable integer value
        last_uid = last_uid.strip("()")
        last_uid = last_uid.strip(",")
        last_uid = int(last_uid)
        userID = last_uid + 1               # add one to biggest user ID to create next user ID
        return userID

    def register_account(self, nameText, emailText, passwordText, clubidText):
        self.ids.error.text = ""                # clear any error messages
        try:
            self.fullname = nameText            # get name from GUI
            self.email = emailText.lower()      # get email from GUI
            self.password = passwordText        # get password from GUI
            self.clubID = int(clubidText)       # get club ID from GUI
            self.userID = self.create_uid(self.exec_sql('''SELECT max(userID) as userID FROM Users;''', []))
            # create new user ID using create uid method

        except ValueError:
            self.ids.error.text = "Invalid input check format of inputted info"
            # if there are any errors in inputted text, allow user to try again
            return

        already = self.exec_sql('''SELECT email FROM Users WHERE email LIKE ? AND userID > 1000''', (self.email,))
        # try and select any individual accounts with the same email

        if already:
            self.ids.error.text = "An account with that email already exists"
            # if an account with that email exists show error
            return

        self.password = hashlib.md5(self.password.encode())     # hash password ready to be stored in DB
        self.password = self.password.hexdigest()

        self.exec_sql('''INSERT INTO Users(userID, name, clubID, email, password) VALUES (?,?,?,?,?)''',
                     (self.userID, self.fullname, self.clubID, self.email, self.password))
        # insert new user's info into the database

        sm.current = 'login'    # go to login screen to allow the user to log in for the first time


class FindClubScreen(Screen):       # create find club screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.club = ""              # set up variables
        self.results = []
        self.search_terms = []
        self.result_labels = []

    # find club screen allows users to find their club's ID when registering an account

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_club(self, clubText):
        self.club = clubText            # get user inputted search
        self.club = self.club.split()   # split users search into individual words
        self.search_terms = []          # makes sure lists are empty
        self.results = []
        self.result_labels = []
        for i in self.club:
            if i.lower() not in ["college", "rifle", "club", "school", "association", "and"]:
                self.search_terms.append(i)    # if word is not in common words then add it to the search terms
            else:
                self.club.remove(i)    # remove common words to make search results more relevant

        for i in self.search_terms:
            self.results += self.exec_sql('''SELECT * FROM Clubs WHERE name LIKE ?''', ('%'+i+'%',))

        self.ids.no_clubs.text = ""         # clear error messages
        self.ids.index.text = ""
        self.ids.result_list.text = ""

        if len(self.results) == 0:
            self.ids.no_clubs.text = "No clubs with that name found"    # if no clubs found with search criteria
            return                                                      # display error message

        self.ids.index.text = "ID, Club name"       # index/guide to results of search

        count = 0
        for i in range(len(self.results)):      # display results of search
            count += 1
            self.ids.result_list.text += str(self.results[i]).strip('()') + "\n"    # format search results
            if count == 5:      # only display first 5 results
                break


class CoachLoginScreen(Screen):     # create coach login screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.email = ""             # set up variables
        self.password = ""
        self.password_attempt = ""
        self.user_name = ""
        self.user_id = 0

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_password(self):
        user_pw = self.exec_sql('''SELECT password FROM Users WHERE email LIKE ? AND userID < 1000''', (self.email,))
        user_pw = str(user_pw)                  # get hashed password from db for the inputted email
        user_pw = user_pw.strip("[]")           # formatting of returned value so it can be compared to user inputted
        user_pw = user_pw.strip("()")           # password
        user_pw = user_pw.strip(",")
        user_pw = user_pw.strip("'")
        return user_pw                          # return formatted hashed password

    def get_user_name(self):
        user_name = self.exec_sql('''SELECT name FROM Users WHERE email LIKE ? AND userID < 1000''', (self.email,))
        user_name = str(user_name)              # get users name from db from their email address
        user_name = user_name.strip("[]")       # formatting of returned value
        user_name = user_name.strip("()")
        user_name = user_name.strip(",")
        user_name = user_name.strip("'")
        return user_name                        # return user name

    def get_user_id(self):
        user_id = self.exec_sql('''SELECT userID FROM Users WHERE email LIKE ? AND userID < 1000''', (self.email,))
        user_id = str(user_id)                  # get user ID of user trying to log in
        user_id = user_id.strip("[]")           # formatting of returned value
        user_id = user_id.strip("()")
        user_id = user_id.strip(",")
        user_id = user_id.strip("'")
        user_id = int(user_id)
        return user_id                          # return user ID

    def login(self, emailText, passwordText):
        try:
            self.ids.error.text = ""                # clear any error messages
            self.email = emailText                  # get email from GUI
            self.password_attempt = passwordText    # get password attempt from GUI
            self.password = self.get_password()     # get password hash value from DB using function
            self.user_name = self.get_user_name()   # get user name value from DB using function
            self.user_id = self.get_user_id()        # get user ID value from DB using function
            self.password_attempt = hashlib.md5(self.password_attempt.encode())
            # convert password attempt to UTF-8 and hash using MD5 hash
            self.password_attempt = self.password_attempt.hexdigest()
            # turn password attempt hash value into hex value

        except ValueError:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            # if there are any errors in inputted text, allow user to try again
            return

        if self.password == self.password_attempt:              # check if inputted value matches stored value
            coach_home_screen.ids.user.text += self.user_name   # pass user details to coach home screen to be displayed
            coach_home_screen.user_name = self.user_name
            coach_home_screen.user_id = self.user_id
            coach_home_screen.get_club_members()
            sm.current = 'coach-home'                           # move to coach home screen

        else:
            self.ids.error.text = "Login unsuccessful please check your details and try again"
            return                                              # if password is incorrect allow user to retry


class CoachRegisterScreen(Screen):  # create coach register screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.fullname = ""          # set up variables
        self.email = ""
        self.password = ""
        self.clubID = 0
        self.userID = 0
        self.last_user = []
        self.last_uid = 0

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def create_uid(self, last_user):
        for i in last_user:             # get user ID from sql passed to function
            last_uid = i
            break

        last_uid = str(last_uid)            # convert sql query result into usable integer value
        last_uid = last_uid.strip("()")
        last_uid = last_uid.strip(",")
        last_uid = int(last_uid)
        userID = last_uid + 1               # add one to biggest user ID to create next user ID
        return userID

    def register_account(self, nameText, emailText, passwordText, clubidText):
        self.ids.error.text = ""                # clear any error messages
        try:
            self.fullname = nameText            # get name from GUI
            self.email = emailText.lower()      # get email from GUI
            self.password = passwordText        # get password from GUI
            self.clubID = int(clubidText)       # get club ID from GUI
            self.userID = self.create_uid(self.exec_sql('''SELECT max(userID) as userID FROM Users WHERE userID < 1000;''', []))
            # create new user ID using create uid method

        except ValueError:
            self.ids.error.text = "Invalid input check format of inputted info"
            # if there are any errors in inputted text, allow user to try again
            return

        already = self.exec_sql('''SELECT email FROM Users WHERE email LIKE ? AND userID < 1000''', (self.email,))
        # try and select any coach accounts with the same email

        if already:
            self.ids.error.text = "An account with that email already exists"
            # if a coach account with that email exists show error
            return

        self.password = hashlib.md5(self.password.encode())     # hash password ready to be stored in DB
        self.password = self.password.hexdigest()

        self.exec_sql('''INSERT INTO Users(userID, name, clubID, email, password) VALUES (?,?,?,?,?)''',
                     (self.userID, self.fullname, self.clubID, self.email, self.password))
        # insert new coach's info into the database

        sm.current = 'coach-login'      # go to coach login screen to allow the coach to log in for the first time


class CoachHomeScreen(Screen):      # create coach home screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_name = ""         # set up variables
        self.user_id = 0
        self.club_id = 0
        self.club_members_ids = []
        self.get_club_members_ids = []

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_club_members(self):
        self.club_id = self.exec_sql('''SELECT clubID FROM Users WHERE userID LIKE ?''', (self.user_id,))
        # find the club that the coach belongs to
        self.club_id = self.club_id[0]          # select the club ID from sql query results
        self.club_id = str(self.club_id)        # convert to string to be formatted
        self.club_id = self.club_id.strip("()")
        self.club_id = self.club_id.strip(",")
        self.club_id = int(self.club_id)        # convert club ID to int to be used later
        self.get_club_members_ids = self.exec_sql('''SELECT userID FROM Users WHERE clubID LIKE ? AND userID > 1000''', (self.club_id,))
        # select all user IDs in coach's club
        for i in self.get_club_members_ids:     # format club members user IDs so they are usable
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = int(i)
            self.club_members_ids.append(i)

        for i in self.club_members_ids:         # generate stats for each user in club
            self.generate_user_stats(i)

    def generate_user_stats(self, user_id):
        # get all users scores from DB for each type of shoot
        two_seven_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 0 AND 35.7 
                                                         AND userID LIKE ?''', (user_id,))
        two_seven_scores = []
        two_ten_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 35.8 AND 50.99 
                                                             AND userID LIKE ?''', (user_id,))
        two_ten_scores = []
        two_fifteen_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 51 AND 76 
                                                             AND userID LIKE ?''', (user_id,))
        two_fifteen_scores = []
        for i in two_seven_scores_temp:     # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            two_seven_scores.append(i)

        for i in two_ten_scores_temp:       # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            two_ten_scores.append(i)

        for i in two_fifteen_scores_temp:   # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            two_fifteen_scores.append(i)

        # generate users mean scores and standard deviations for each type of shoot
        try:
            two_seven_mean = self.get_mean(two_seven_scores)
            two_ten_mean = self.get_mean(two_ten_scores)
            two_fifteen_mean = self.get_mean(two_fifteen_scores)
            two_seven_stdev = statistics.stdev(two_seven_scores)
            two_ten_stdev = statistics.stdev(two_ten_scores)
            two_fifteen_stdev = statistics.stdev(two_fifteen_scores)
            mean_stdev = statistics.mean([two_seven_stdev, two_ten_stdev, two_fifteen_stdev])
            # calculate average standard deviation for each type of shoot
            mean_stdev = round(mean_stdev, 1)

            # create stats string that can be displayed in GUI
            stats = str(two_seven_mean) + "           " + str(two_ten_mean) + "           " + str(two_fifteen_mean) + \
                    "                                    " + str(mean_stdev)

        except:
            # if any errors occur display error message
            stats = "Could not generate statistics"

        user_name = self.exec_sql('''SELECT name FROM Users WHERE userID LIKE ?''', (user_id,))
        # select users name so it can be displayed next to their statistics
        user_name = str(user_name)              # format user name to be displayed
        user_name = user_name.strip("[]")
        user_name = user_name.strip("()")
        user_name = user_name.strip(",")
        user_name = user_name.strip("'")
        spaces = 52 - len(user_name)            # attempt to get even spacings for different length names
        gap = ""
        for i in range(spaces):
            gap += " "
        self.ids.stats.text += (user_name + gap + stats + "\n\n")   # add users stats into GUI

    def get_mean(self, scores):                     # function to calculate mean score for type of shoot
        vees = []
        points = []
        for i in scores:            # split score into main integer score and V bull count
            a, b = math.modf(i)
            a = round(a, 1)
            vees.append(a)          # append V count to V count list
            points.append(b)        # append integer score to integer score list

        mean_vees = statistics.mean(vees)       # calculate average V count
        mean_vees = round(mean_vees, 1)         # round to 1 d.p.
        mean_points = statistics.mean(points)   # calculate average integer score
        mean_points = round(mean_points, 0)     # round to nearest integer
        mean = mean_points + mean_vees          # create average score by adding mean V count
        return mean                             # and mean average integer score


class HomeScreen(Screen):           # create home screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_name = ""         # set up variables
        self.user_id = 0

    def go_setup(self):                         # function to go to setup menu screen
        setup_screen.user_id = self.user_id     # pass users ID so it can be used in setup menu screen

    def enter_score(self):                      # function to go to enter score screen
        enter_details.userID = self.user_id     # pass users ID so it can be used in enter score screen
        sm.current = 'enter-score'              # go to enter score screen

    def view_score(self):                       # function to go to view scores menu
        view_score_home.userID = self.user_id   # pass users ID so it can be used in view score menu screen
        view_score_home.get_recent_scores()     # call get recent scores method of view scores menu
        sm.current = 'view-score-home'          # go to view score menu


class SetupsMenuScreen(Screen):     # create setup menu screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_id = 0            # set up variables

    def view_setups(self):          # function to go to view setups screen
        view_setup.view_setup()     # call view setups module of view setups screen
        sm.current = 'view_setups'  # go to view setups screen

    def edit_setups(self):          # function to go to edit setups screen
        edit_setup.view_setup()     # call view setups module of edit setups screen
        sm.current = 'edit_setups'  # go to edit setups screen


class NewSetupScreen(Screen):       # create new setup screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_id = 0            # set up variables
        self.setup_id = 0
        self.rifle = ""
        self.jacket = ""
        self.sling = ""
        self.glove = ""

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def new_setup_id(self):             # method to find greatest (largest int value) setup ID and create new setup ID
        last_sid = self.exec_sql('''SELECT max(setupID) as setupID FROM Setups;''', [])
        last_sid = str(last_sid)        # use sql query to find largest setup ID value
        last_sid = last_sid.strip("[]") # format returned value
        last_sid = last_sid.strip("()")
        last_sid = last_sid.strip(",")
        last_sid = int(last_sid)
        setup_id = last_sid + 1         # add one to largest setup ID to create new setup ID
        return setup_id

    def add_new_setup(self, rifleText,  jacketText, slingText, gloveText):
        self.ids.error.text = ""                    # clear any error messages
        try:
            self.rifle = rifleText                  # get rifle info from GUI
            self.jacket = jacketText                # get jacket info from GUI
            self.sling = slingText                  # get sling info from GUI
            self.glove = gloveText                  # get glove info from GUI
            self.setup_id = self.new_setup_id()     # use new_setup_id method to create new setup ID
            self.user_id = home_screen.user_id      # get user ID from home screen object
            for i in [self.rifle, self.jacket, self.sling, self.glove]:
                if len(i) == 0:                                                     # check if all fields have been
                    self.ids.error.text = "Please input a value for all fields"     # filled in
                    return

        except ValueError:                                                          # if there are any errors in
            self.ids.error.text = "Invalid input check format of inputted info"     # inputted info display
            return                                                                  # appropriate error message

        self.exec_sql('''INSERT INTO Setups(setupID, userID, rifle, jacket, sling_setting, glove)
                        VALUES (?,?,?,?,?,?)''',
                       (self.setup_id, self.user_id, self.rifle, self.jacket, self.sling, self.glove))
        # sql statement to create a new setup in Setups table from users inputted data

        sm.current = 'setups'   # return to setup menu screen


class ViewSetupScreen(Screen):      # create view setup screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_id = 0            # set up variables
        self.user_name = ""
        self.setup_id = 0
        self.user_setups = []

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def format_setups(self, setups):        # method to format setups into a readable form
        setups = str(setups)
        setups = setups.strip("[]")         # tidy up formatting from returned value from sql query
        setups = setups.strip("()")
        setups = setups.strip(",")
        setups = setups.replace(",", " ")
        setups = setups.replace("(", " ")
        setups = setups.replace(")", " ")
        if len(setups) == 0:                # if there are no setups in DB
            setups = "No setups in DB"      # display error message
            return setups

        return setups

    def view_setup(self):
        self.user_name = home_screen.user_name      # get users name from homescreen object
        self.user_id = home_screen.user_id          # get users ID from homescreen object
        self.user_setups = self.exec_sql('''SELECT setupID FROM Setups WHERE userID LIKE ?''', (self.user_id,))
        # get all users setups using sql query
        self.ids.id_view.text = str(self.user_name) + "'s setup IDs: " + self.format_setups(self.user_setups)
        # display users name and all setups that belong to them

    def show_setup(self, setup_idText):
        self.ids.error.text = ""                    # clear any error message displayed
        self.setup_id = setup_idText                # get setup ID that user wants to view from the GUI
        setup = self.exec_sql('''SELECT rifle, jacket, sling_setting, glove FROM Setups WHERE setupID LIKE ?''',
                             (self.setup_id,))      # get kit used from setup using setup ID as identifier
        try:
            rifle = setup[0][0]         # get items of kit from returned sql value
            jacket = setup[0][1]
            sling = setup[0][2]
            glove = setup[0][3]

        except IndexError:
            self.ids.error.text = "Cannot find that setup, check the search term"
            return                      # if inputted setup ID did not return anything return appropriate error message

        self.ids.rifle.text = rifle     # display kit items in GUI
        self.ids.jacket.text = jacket
        self.ids.sling.text = sling
        self.ids.glove.text = glove


class EditSetupScreen(Screen):      # create edit setup screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.user_id = 0            # set up variables
        self.user_name = ""
        self.setup_id = 0
        self.user_setups = []

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def format_setups(self, setups):        # method to format setups into a readable form
        setups = str(setups)
        setups = setups.strip("[]")         # tidy up formatting from returned value from sql query
        setups = setups.strip("()")
        setups = setups.strip(",")
        setups = setups.replace(",", " ")
        setups = setups.replace("(", " ")
        setups = setups.replace(")", " ")
        if len(setups) == 0:                # if there are no setups in DB
            setups = "No setups in DB"      # display error message
            return setups

        return setups

    def view_setup(self):
        self.user_name = home_screen.user_name      # get users name from homescreen object
        self.user_id = home_screen.user_id          # get users ID from homescreen object
        self.user_setups = self.exec_sql('''SELECT setupID FROM Setups WHERE userID LIKE ?''', (self.user_id,))
        # get all users setups using sql query
        self.ids.id_view.text = str(self.user_name) + "'s setup IDs: " + self.format_setups(self.user_setups)
        # display users name and all setups that belong to them

    def show_setup(self, setup_idText):
        self.ids.error.text = ""                    # clear any error message displayed
        self.setup_id = setup_idText                # get setup ID that user wants to view from the GUI
        setup = self.exec_sql('''SELECT rifle, jacket, sling_setting, glove FROM Setups WHERE setupID LIKE ?''',
                             (self.setup_id,))      # get kit used from setup using setup ID as identifier
        try:
            rifle = setup[0][0]         # get items of kit from returned sql value
            jacket = setup[0][1]
            sling = setup[0][2]
            glove = setup[0][3]

        except IndexError:
            self.ids.error.text = "Cannot find that setup, check the search term"
            return                      # if inputted setup ID did not return anything return appropriate error message

        self.ids.rifle.text = rifle     # display kit items in GUI
        self.ids.jacket.text = jacket
        self.ids.sling.text = sling
        self.ids.glove.text = glove

    def commit_changes(self, rifleText, jacketText, slingText, gloveText):
        user_id = self.exec_sql('''SELECT userID FROM Setups WHERE setupID LIKE ?''', (self.setup_id,))
        user_id = str(user_id)          # get user ID for which the setup belongs to
        user_id = user_id.strip("[]")   # format into usable form
        user_id = user_id.strip("()")
        user_id = user_id.strip(",")
        user_id = user_id.strip("'")
        user_id = int(user_id)
        if self.user_id != user_id:     # check if users who is editing setup/logged in, is the same as setup's user
            self.ids.error.text = "You cannot alter this setup, it does not belong to you"
            return                      # display error message if user IDs do not match

        rifle = rifleText           # change setup info to that inputted by user
        jacket = jacketText         # if it has not been changed it will remain the same as before
        sling = slingText
        glove = gloveText

        self.exec_sql('''DELETE FROM Setups WHERE setupID = ?''', (self.setup_id,))
        # delete old setup
        self.exec_sql('''INSERT INTO Setups(setupID, userID, rifle, jacket, sling_setting, glove)
                                VALUES (?,?,?,?,?,?)''',
                     (self.setup_id, self.user_id, rifle, jacket, sling, glove))
        # replace with setup with edited values

        sm.current = 'home'     # return to home screen


class EnterScoreScreen(Screen):     # create enter score screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.score = 0              # set up variables
        self.max = 0
        self.ids.seven.bind(active=self.score_format)       # bind checkboxes in GUI to function
        self.ids.ten.bind(active=self.score_format)
        self.ids.fifteen.bind(active=self.score_format)

    def score_format(self, checkbox, checked):      # method to give checkboxes functionality to allow user
        self.max = 0                                # to select the type of shoot
        if not checked:
            self.max = 0
            return

        if checkbox == self.ids.seven:              # if the type of shoot is 2&7
            self.max = 35                           # max integer score is 35
            return

        if checkbox == self.ids.ten:                # if the type of shoot is 2&10
            self.max = 50                           # max integer score is 50
            return

        if checkbox == self.ids.fifteen:            # if the type of shoot is 2&15
            self.max = 75                           # max integer score is 75
            return

        else:
            self.max = 0
            return

    def get_score(self, scoreText):
        self.ids.error.text = ""        # clear any error messages in GUI
        self.score = scoreText          # get user inputted score from GUI
        if self.max == 0:               # if no shoot type selected, display error message
            self.ids.error.text = "Please make sure you have chosen the correct shoot format"
            return

        try:                            # if score is greater than score type max, display error message
            if int(float(self.score)) > self.max:
                self.ids.error.text = "Please make sure you have chosen the correct shoot format"
                return

        except ValueError:              # if any value errors occur display error message
            self.ids.error.text = "Please make sure you have chosen the correct shoot format"
            return

        self.score = float(self.score)      # convert score into float
        enter_details.score = self.score    # pass score to enter details object
        sm.current = 'enter_details'        # go to enter details screen of GUI


class EnterDetailsScreen(Screen):       # create enter details screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):           # initialise object
        super().__init__(**kw)          # inherit default values from Kivy's parent Screen class
        self.score = 0                  # set up variables
        self.distance = 0
        self.ammo = ""
        self.light = ""
        self.weather = ""
        self.range = ""
        self.target = 0
        self.date = ""
        self.setupID = 0
        self.userID = 0
        self.ids.three.bind(active=self.get_dist)       # bind checkboxes in GUI to function
        self.ids.five.bind(active=self.get_dist)
        self.ids.six.bind(active=self.get_dist)
        self.ids.nine.bind(active=self.get_dist)
        self.ids.ten.bind(active=self.get_dist)

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_dist(self, checkbox, checked):      # method to give checkboxes functionality to allow user
        self.distance = 0                       # to select distance of shoot
        if not checked:
            self.distance = 0
            return

        if checkbox == self.ids.three:          # if checkbox is x
            self.distance = 300                 # make distance y
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

    def get_details(self, setupidText, ammoText, lightText, weatherText, rangeText, targetNum, dayText, monthText, yearText):
        self.ids.error.text = ""        # clear any error messages in GUI
        try:
            self.setupID = int(setupidText)     # get shoot details from GUI
            self.ammo = ammoText
            self.light = lightText
            self.weather = weatherText
            self.range = rangeText
            self.target = int(targetNum)
            self.date = datetime.date(int(yearText), int(monthText), int(dayText))
            # convert inputted date into datetime so it can be put into sql database/query
        except ValueError:
            self.ids.error.text = "Please make sure you have the correct format for all fields"
            # if any value errors occur, i.e. input is not correct format, display appropriate error message

        if self.distance == 0:
            self.ids.error.text = "Please make sure you have selected the correct distance"
            # if no distance is selected, display appropriate error message
            return

        for i in (self.userID, self.setupID, self.distance, self.ammo, self.light, self.weather, self.range, self.target):
            try:
                if len(i) <= 0:     # check that all char fields have been filled in
                    self.ids.error.text = "Please make sure all fields are filled in correctly"
                    return

            except:
                if i <= 0:          # check that all int/float fields have been filled in
                    self.ids.error.text = "Please make sure all fields are filled in correctly"
                    return

        try:
            self.exec_sql('''INSERT INTO Scores(userID, setupID, score, distance, ammo, light, weather, range, target, 
                           date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           [self.userID, self.setupID, self.score, self.distance, self.ammo, self.light, self.weather,
                            self.range, self.target, self.date])
            # input users shoot data into DB using sql query

        except:
            self.ids.error.text = "Please make sure you have entered all info in the correct format"
            # if any errors occur, display appropriate error message
            return

        sm.current = 'home'     # return to home screen


class ViewScoreHomeScreen(Screen):      # create view score home screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):           # initialise object
        super().__init__(**kw)          # inherit default values from Kivy's parent Screen class
        self.userID = 0                 # set up variables

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def view_stats(self):
        view_stats.userID = self.userID     # pass user ID to the view stats page
        view_stats.get_scores()             # call get score method of the view stats page
        sm.current = 'view-stats-home'      # go to the view stats main page

    def view_all_scores(self):
        view_all_scores.userID = self.userID    # pass user ID to the view all scores page
        view_all_scores.view_scores()           # call view scores method of the view all scores page
        sm.current = 'view-all-scores'          # go to the view all scores page

    def get_recent_scores(self):
        self.ids.most_recent_scores.text = ""   # clear all most recent scores
        most_recent = self.exec_sql('''SELECT score, distance, date FROM Scores WHERE userID LIKE ? ORDER BY date(date)
                                       DESC LIMIT 8''', (self.userID,))
        # select the 8 most recent scores, using date field to get most recent ones
        for i in most_recent:   # parse through most recent shoots getting each shoots data
            for j in i:
                j = str(j)
                if len(j) == 4:                     # check length of fields to get them aligned in GUI properly
                    self.ids.most_recent_scores.text += (j + "       ")

                else:
                    self.ids.most_recent_scores.text += (j+"        ")

            self.ids.most_recent_scores.text += "\n\n"  # make a 2 new lines between scores/shoots in GUI


class ViewStatsScreen(Screen):      # create view stats screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):       # initialise object
        super().__init__(**kw)      # inherit default values from Kivy's parent Screen class
        self.userID = 0             # set up variables
        self.two_seven_scores_temp = []
        self.two_ten_scores_temp = []
        self.two_fifteen_scores_temp = []
        self.two_seven_scores = []
        self.two_ten_scores = []
        self.two_fifteen_scores = []

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_scores(self):       # get all users scores from DB for each type of shoot
        self.two_seven_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 0 AND 35.7 
                                                 AND userID LIKE ?''', (self.userID,))
        self.two_ten_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 35.8 AND 50.99 
                                                 AND userID LIKE ?''', (self.userID,))
        self.two_fifteen_scores_temp = self.exec_sql('''SELECT score FROM Scores WHERE score BETWEEN 51 AND 76 
                                                 AND userID LIKE ?''', (self.userID,))
        for i in self.two_seven_scores_temp:        # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            self.two_seven_scores.append(i)

        for i in self.two_ten_scores_temp:          # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            self.two_ten_scores.append(i)

        for i in self.two_fifteen_scores_temp:      # format scores so they can be analysed
            i = str(i)
            i = i.strip("()")
            i = i.strip(",")
            i = float(i)
            self.two_fifteen_scores.append(i)

        self.get_stats()    # work out stats using get_stats method

    def get_stats(self):
        try:         # generate users mean scores and standard deviations for each type of shoot
            two_seven_mean = self.get_mean(self.two_seven_scores)
            two_ten_mean = self.get_mean(self.two_ten_scores)
            two_fifteen_mean = self.get_mean(self.two_fifteen_scores)
            st_dev = self.get_stdev()
            # display score averages in GUI
            self.ids.average.text = str(two_seven_mean) + "       " + str(two_ten_mean) + "       " + str(
                two_fifteen_mean)
            # display average standard deviation in GUI
            self.ids.st_dev.text = str(st_dev)

        except statistics.StatisticsError:
            self.ids.error.text = "You do not have enough scores to do any analysis"
            # display error message if there aren't enough scores in the DB to do any analysis

    def get_stdev(self):
        # calculate average standard deviation for each type of shoot
        two_seven_stdev = statistics.stdev(self.two_seven_scores)
        two_ten_stdev = statistics.stdev(self.two_ten_scores)
        two_fifteen_stdev = statistics.stdev(self.two_fifteen_scores)
        mean_stdev = statistics.mean([two_seven_stdev, two_ten_stdev, two_fifteen_stdev])
        mean_stdev = round(mean_stdev, 1)   # average the standard deviations and round to 1 d.p.
        return mean_stdev

    def get_mean(self, scores):                     # function to calculate mean score for type of shoot
        vees = []
        points = []
        for i in scores:            # split score into main integer score and V bull count
            a, b = math.modf(i)
            a = round(a, 1)
            vees.append(a)          # append V count to V count list
            points.append(b)        # append integer score to integer score list

        mean_vees = statistics.mean(vees)       # calculate average V count
        mean_vees = round(mean_vees, 1)         # round to 1 d.p.
        mean_points = statistics.mean(points)   # calculate average integer score
        mean_points = round(mean_points, 0)     # round to nearest integer
        mean = mean_points + mean_vees          # create average score by adding mean V count
        return mean                             # and mean average integer score


class ViewAllScoresScreen(Screen):      # create view all scores screen object (in Kivy each 'screen' is its own object)
    def __init__(self, **kw):           # initialise object
        super().__init__(**kw)          # inherit default values from Kivy's parent Screen class
        self.userID = 0                 # set up variables
        self.scores = []

    def exec_sql(self, query, values):            # function to execute sql using the client-server interface
        mySocket.send(query.encode())             # encode the sql by breaking it into bit form
        val = bool(mySocket.recv(1024).decode())  # check to see if query has been received by server
        if val is not True:                       # if query has not been received exit the function
            return
        values = pickle.dumps(values)             # encode the values needed for the sql query into bit form
        mySocket.send(values)                     # send values to server
        results = mySocket.recv(1024)             # receive results of query back from server
        results = pickle.loads(results)           # decode results of query back from bit form
        if len(results) > 0:                      # if the query generated results return these
            return results
        else:
            return                                # if query did not generate any results no need to return them

    def get_date(self, oldest_date):        # get oldest date from sql query and format it so it can be used
        oldest_date = str(oldest_date)
        oldest_date = oldest_date.strip("[]")
        oldest_date = oldest_date.strip("()")
        oldest_date = oldest_date.strip(",")
        oldest_date = oldest_date.strip("'")
        oldest_date = datetime.date(int(oldest_date[0:4]), int(oldest_date[5:7]), int(oldest_date[8:10]))
        return oldest_date

    def view_scores(self):
        self.ids.scores.text = ""
        oldest_date = self.exec_sql('''SELECT date FROM Scores WHERE userID LIKE ? ORDER BY date(date) ASC LIMIT 1''',
                                    (self.userID,))     # get date of first shoot (oldest) from DB
        oldest_date = self.get_date(oldest_date)        # format it
        tomorrow = datetime.date.today()        # get todays date
        tomorrow += datetime.timedelta(days=1)  # add one day to get tomorrows data
        while oldest_date != tomorrow:          # increment days until date is tomorrow
            scores = self.exec_sql('''SELECT score, distance, weather, light, ammo, range, target, date FROM Scores 
                                    WHERE userID LIKE ? AND date(date) LIKE ?''',
                                   ([self.userID, oldest_date,]))
            # select scores with "oldest" date
            if scores is not None:
                for i in scores:            # if any scores are found on "oldest date" add them to be put into GUI
                    self.scores.append(i)

            if oldest_date == tomorrow:     # when "oldest date" reaches tomorrow exit loop
                break

            oldest_date += datetime.timedelta(days=1)   # add one to oldest date

        for i in self.scores:       # increment through scores and add them (and details of shoot) into GUI
            for j in i:
                j = str(j)
                self.ids.scores.text += (j + "    ")
            self.ids.scores.text += "\n\n"


login_screen = LoginScreen()                # create instances of all screens ready to be put
register_screen = RegisterScreen()          # into Kivy's screen manager
find_club = FindClubScreen()
home_screen = HomeScreen()
enter_score = EnterScoreScreen()
enter_details = EnterDetailsScreen()
view_score_home = ViewScoreHomeScreen()
setup_screen = SetupsMenuScreen()
new_setup = NewSetupScreen()
view_setup = ViewSetupScreen()
edit_setup = EditSetupScreen()
view_stats = ViewStatsScreen()
view_all_scores = ViewAllScoresScreen()
coach_login = CoachLoginScreen()
coach_register = CoachRegisterScreen()
coach_home_screen = CoachHomeScreen()

sm = ScreenManager(transition=FadeTransition())     # set transition between screens

sm.add_widget(login_screen)         # add all the screens to Kivy's screen manager
sm.add_widget(register_screen)
sm.add_widget(find_club)
sm.add_widget(home_screen)
sm.add_widget(enter_score)
sm.add_widget(enter_details)
sm.add_widget(setup_screen)
sm.add_widget(new_setup)
sm.add_widget(view_setup)
sm.add_widget(edit_setup)
sm.add_widget(view_score_home)
sm.add_widget(view_stats)
sm.add_widget(view_all_scores)
sm.add_widget(coach_login)
sm.add_widget(coach_register)
sm.add_widget(coach_home_screen)


class ScoreStore(App):      # create Kivy 'App' class
    def build(self):        # build app
        return sm           # display GUI using screen manager


if __name__ == "__main__":
    ScoreStore().run()
