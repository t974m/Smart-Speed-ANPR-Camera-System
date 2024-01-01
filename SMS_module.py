#pip install vonage
#pip install pyshorteners

from datetime import datetime as DT # For timestamp
import time
import vonage
import pyshorteners

client = vonage.Client(key="0f88ee00", secret="GNEoafH3PN0OL2Iy") #0f8..00; GNE..Iy -> Tamim
sms = vonage.Sms(client)
shorten = pyshorteners.Shortener()

#========Test params. ==============
# name = "Tamim M." #Firebase
# np = "551487" #ANPR
# phone = "97466194252" #Firebase
# speed = "29" #uRAD
#===================================

def send(name, np, phone, speed, imageURL):
    #tstamp = DT.now.strftime('%d/%m/%Y, %H:%M') # current date and time
    shortURL = shorten.chilpit.short(imageURL)
    message = ("Dear %s, New traffic violation recorded on (%s) with %s km/h (Photo: %s) Please visit the security." % (name, np, speed, shortURL))
    #print(message) #TEST

    responseData = sms.send_message(
    {
        "from": "TAU Secure", #Premium feature
        "to": phone,
        "text": message,
    }    )
    #print("responseData =\n",responseData) #TEST 
    print("Sending SMS...")
    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.\n")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}\n")

##########################################DEBUG+Test###################
#send(name, np, phone, speed, "https://firebasestorage.googleapis.com/v0/b/tau-ac002.appspot.com/o/violation_images%2F551487_2022-04-05_14-39-53.jpg?alt=media")  #======== TEST RUN ============