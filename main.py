from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import os
from myfirebase import Myfirebase
import requests
import json

class HomeScreen(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class SignInScreen(Screen):
    #username = ObjectProperty()
    pass

class RegisterScreen(Screen):
    pass

class DashBoardScreen(Screen):
    pass

class ProfileScreeen(Screen):
    pass

GUI = Builder.load_file("main.kv")

class MainApp(App):
    stdID = 12
    def build(self):
        self.my_firebase = Myfirebase()
        return GUI

    #def get_id(self):
    #    print("id: ", self.username.text)
    #    ID = self.username.text

    def on_start(self):

        try:
            #try to read the persisent idToken
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read()

            #use refresh token to get a new id token
            id_token, local_id = self.my_firebase.exchange_refresh_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            #get database data
            #print("https://emucovidtrackingapplication-default-rtdb.firebaseio.com/" + local_id +".json?auth=" + id_token)
            result = requests.get("https://emucovidtrackingapplication-default-rtdb.firebaseio.com/users/" + local_id +".json?auth=" + id_token)
            print("Was it ok,", result.ok)
            #print(result.json())
            data = json.loads(result.content.decode())
            #print(data)
            #stName = data['name']
            #stSurname = data['surname']

            # get data and update the student name and surname for dashboard screen
            student_name_surname = self.root.ids['dashboard_screen'].ids['student_name_surname']
            student_name_surname.text = "Hello " + str(data['name'])

            # get data and update student's last test date and result for dashboard screen
            lst_test_date = self.root.ids['dashboard_screen'].ids['lst_test_date']
            lst_test_result = self.root.ids['dashboard_screen'].ids['lst_test_result']

            lst_test_date.text = data['last_test_date']
            lst_test_result.text = data['last_test_result']

            # get student details for profile screen
            std_name = self.root.ids['profile_screen'].ids['std_name']
            std_id = self.root.ids['profile_screen'].ids['std_id']
            address = self.root.ids['profile_screen'].ids['address']
            phone_no = self.root.ids['profile_screen'].ids['phone_no']
            email = self.root.ids['profile_screen'].ids['email']

            std_name.text = str(data['name'])
            std_id.text = str(data['student_id'])
            address.text = str(data['address'])
            phone_no.text = str(data['phone_no'])
            email.text = str(data['email'])

            self.change_screen("dashboard_screen")
        except:
            pass


    #    name = data['name']
    #    print(name)
        #poulate the dashboard
    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.transition = NoTransition()
        screen_manager.current = screen_name
if __name__ == '__main__':

    MainApp().run()