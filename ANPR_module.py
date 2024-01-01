import requests
import json

#from pprint import pprint #For testing

region = ["qa"] # Change to your country
#filename = '/home/pi/Desktop/Qatari Number Plate Dataset QU/QU Gate Samples/Morning/Wide/Gate 1/D8482359.JPG'
def ANPR(filename):
    with open(filename, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data= dict(region),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token 26c94cdab1f7753317b16a3fad5d93a13c9914f1'}) #Tamim: 26c94...914f1
    result = (response.json())
    #pprint(result)
    detectedPlateCount = len(result["results"]) #Number of detected plates
    for i in range(detectedPlateCount):
        detectedPlate = ((result["results"])[i])["plate"]
        if (len(detectedPlate)>6):
            detectedPlate = detectedPlate[-6:] #Take last 6 chars
        detectedPlate = [str(x) for x in detectedPlate if x.isdigit()]
        detectedPlate = "".join(str(x) for x in detectedPlate)
        print(i+1,") \tDetected plate is: ", detectedPlate)
    return detectedPlate

#ANPR('/home/pi/Desktop/image0.jpg')