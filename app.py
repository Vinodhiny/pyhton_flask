import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from business_logic import image_compression

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
   "apiKey": "AIzaSyCbbqXxeWO7yM3pK0YCxvTiouOV-YrYjs0",
    "authDomain": "image-resize-c5a00.firebaseapp.com",
    "projectId": "image-resize-c5a00",
    "storageBucket": "image-resize-c5a00.appspot.com",
    "messagingSenderId": "998075835495",
    "appId": "1:998075835495:web:a7f4ac0de7a51aa933e0c2",
    "measurementId": "G-ETWZP06JES",
    "databaseURL": "https://image-resize-c5a00-default-rtdb.asia-southeast1.firebasedatabase.app",
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Upload page
@app.route("/processing")
def processing():
    if person["is_logged_in"] == True:
        return render_template("processing.html")
    else:
        return render_template("welcome.html", email = person["email"], name = person["name"])
# @app.route("/welcome")
# def welcome():
#     if person["is_logged_in"] == True:
#         return render_template("welcome.html", email = person["email"], name = person["name"])
#     else:
#         return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('processing'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('processing'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('processing'))
        else:
            return redirect(url_for('register'))
        

#When user click on upload, the image file will processed
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    if file:
        filename = file.filename
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Process the uploaded image
        output_filename = f"processed_{filename}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
        width_range = (2.63, 7.5)  # Example width range
        height_range = (0.25, 8.75)  # Example height range
        dpi = (300, 600)  # Example DPI setting

        image_compression.resize_image(upload_path, output_path, width_range, height_range, dpi)

        # Optionally, you can delete the uploaded file after processing
        os.remove(upload_path)

        # Provide a link or button for downloading the processed image
        download_link = f"<a href='/download/{output_filename}'>Download</a>"

        return f"Image uploaded and processed successfully! {download_link}"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run()
