import requests
import json
from kivy.app import App
class Myfirebase():
    webapi = "AIzaSyCNGkk13BIaYT6GO0aj_7mxxUc0wN9t8p0"
    def sign_up(self, email, password):
        global sign_up_data
        global localId
        global idToken

        app = App.get_running_app()
        #print("Signed up!!")
        #send email and password to firebase
        #firebase will return a localid, idtoken, authtoken and refreshtoken

        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.webapi
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        signup_request = requests.post(signup_url, data=signup_payload)
        print(signup_request.ok)
        print(signup_request.content.decode())
        sign_up_data = json.loads(signup_request.content.decode())
        if signup_request.ok == True:
            refresh_token = sign_up_data["refreshToken"]
            localId = sign_up_data["localId"]
            idToken = sign_up_data["idToken"]
            #save refreshtoken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            #save localid to a variable to main app class
            app.local_id = localId
            app.id_token = idToken

            #app.root.ids["signin_screen"].ids["signin_message"].text = "Account now registered, Please Enter your personal detials"
            app.change_screen("register_screen")
        if signup_request.ok == False:
            error_data = json.loads(signup_request.content)
            error_message = error_data["error"]["message"]
            if error_message == "EMAIL_EXISTS":
                self.sign_in_existing_user(email, password)
            else:
                app.root.ids["signin_screen"].ids["signin_message"].text = '[b][u][i]' + error_message + '[/b][/u][/i]'
    def sign_in_existing_user(self,email, password):
        ##Called if a user tried to signup  and their email already existed
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.webapi
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        app = App.get_running_app()

        if(signin_request.ok == True):
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']

            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            app.local_id = localId
            app.id_token = idToken

            app.on_start()

        elif (signin_request.ok) == False:
            error_data = json.load(signin_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids["signin_screen"].ids["signin_message"].text = "EMAIL EXISTS - " + error_message.replace("_", "")


    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.webapi
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        print("WAS REFRESH OK?", refresh_req.ok)
        print(refresh_req.json())
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        print("LOCALID:", local_id)
        print("IDTOKEN:", id_token)
        return id_token, local_id

    def register(self):
        global sign_up_data
        global localId
        global idToken
        app = App.get_running_app()
        print("Registered!!")
        # send email and password to firebase
        # firebase will return a localid, idtoken, authtoken and refreshtoken

        #signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.webapi
        #signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        #signup_request = requests.post(signup_url, data=signup_payload)
        #print(signup_request.ok)
        #print(signup_request.content.decode())
        #sign_up_data = json.loads(signup_request.content.decode())
        #

        name = app.root.ids['register_screen'].ids['name']
        std_id = app.root.ids['register_screen'].ids['std_id']
        address = app.root.ids['register_screen'].ids['address']
        phone_no = app.root.ids['register_screen'].ids['phone_no']
        email = app.root.ids['register_screen'].ids['email']

        my_data = {"address":address.text, "last_test_date":"None", "last_test_result":"None", "name":name.text, "phone_no":phone_no.text, "student_id":std_id.text, "email":email.text}
        user_data =json.dumps(my_data)
        post_request = requests.patch("https://emucovidtrackingapplication-default-rtdb.firebaseio.com/users/" + localId + ".json?auth=" + idToken,
                   data = user_data)
        print(post_request.ok)
        print(json.loads(post_request.content.decode()))

        app.on_start()

