from flask import *
def getLoginPage(email, password):
    # returns true if the person is authenticated otherwise it returns false
    import pyrebase

    app = Flask(__name__)
    config = {
        "apiKey": "AIzaSyCkjsbkDtmKUU_77XHDYfNnBZS1E3F82iw",
        "authDomain": "csc207-tli.firebaseapp.com",
        "databaseURL": "https://csc207-tli.firebaseio.com",
        "projectId": "csc207-tli",
        "storageBucket": "csc207-tli.appspot.com",
        "messagingSenderId": "707734809591",
        "appId": "1:707734809591:web:313eb97ac705e6ebb21cf2",
        "measurementId": "G-VQCPWR41LV"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
       user = auth.sign_in_with_email_and_password(email, password)
       token = user['idToken']
       return token
    except:
        return ""