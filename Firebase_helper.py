#pip install pyrebase
import pyrebase
from datetime import datetime as DT # For timestamp
import time
import os

config = {
  "apiKey": "AIzaSyBEIcm1EL4uu3ihQFO7iaF3Jj5A7ajzFe4", 
  "authDomain": "864167782777.firebaseapp.com",
  "databaseURL": "https://tau-ac002-default-rtdb.firebaseio.com",
  "storageBucket": "tau-ac002.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

def getInfo(np):
    residentsOnline = db.child("residents").get() # Read the DB
    residents = dict(residentsOnline.val())
    for id in residents: # For each parent 
        for key,value in residents[id].items(): # Get the child elements
             if (key == "np" and value == np): # If NP matches the one from ANPR
                     return residents[id]["name"],residents[id]["phone"] # Grab the ID's name + phone

def getSpeedLimit():
    speed = db.child("speedLimit").get()
    return int(speed.val()) # Speed of type 'str' -> 'int' in km/h

def uploadData(filename, np, speed):
    newFilename = (np + DT.now().strftime('_%Y-%m-%d_%H-%M-%S')) # New name string
    os.rename(filename, (newFilename  + ".jpg"))
    
    newFileLocation = ("/home/pi/Desktop/" + newFilename + ".jpg") # Local photo dir.
    folderIndex = ("violation_images/" + newFilename + ".jpg") # Online photo dir.

    storage.child(folderIndex).put(newFileLocation) # Upload photo to storage
    imageURL = storage.child(folderIndex).get_url(None) # Fetch URL of the newly uploaded image
    #print(imageURL)
    pushData = {"np":np, "speed":(str(speed)+" km/h"), "imageURL": imageURL}  # Push data to Firebase-RTDB
    db.child("violationDetails").child(newFilename).set(pushData)
    return imageURL
    
##########################################DEBUG+Test###################    
#uploadData("/home/pi/Desktop/image0.jpg","123456",100)
# while True:
#     print(getSpeedLimit())
#print(getInfo("463951"))