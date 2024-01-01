import uRAD_RP_SDK11        # import uRAD library
import ANPR_module as ANPR  # import ANPR script
import Camera_module as CAM # import Camera script
import SMS_module as sms    # import SMS script
import Firebase_helper as db# import Firebase RTDB handler
import time                 # أشرح عن الوقت؟

from datetime import datetime as DT # For timestamp


# Input parameters
mode = 1                    # doppler mode (Check Datasheet)
f0 = 125                    # output continuous frequency 24.125 GHz
BW = 240					# don't apply in doppler mode (mode = 1)
Ns = 200					# 200 samples
Ntar = 3					# No. of target of interest
Vmax = 34 					# searching along the full velocity range max 75m/s = 270km/h
MTI = 0						# MTI mode disable because we want information of static and moving targets
Mth = 0						# parameter not used because "movement" is not requested
Alpha = 20					# signal has to be 20 dB higher than its surrounding
distance_true = False 		# Request distance information
velocity_true = True		# mode 2 does not provide velocity information
SNR_true = True 			# Signal-to-Noise-Ratio information requested
I_true = False 				# In-Phase Component (RAW data) not requested
Q_true = False 				# Quadrature Component (RAW data) not requested
movement_true = False 		# Not interested in boolean movement detection
maxim= 0.0                  # Maximum velocity
speed = 0                   # Current velocity
speedLimit = 20             # Speed limit grabbed from firebase (initially random to avoid error when init_0)
np = 0                      # Detected number plate

print("Program initiated...") # ==== DEBUG


# Method to correctly turn OFF and close uRAD
def closeProgram():
    # Switch OFF uRAD
    return_code = uRAD_RP_SDK11.turnOFF()
    exit()

# Switch uRAD ON
return_code = uRAD_RP_SDK11.turnON()
if (return_code != 0):
    closeProgram()

# Load Configuration for uRAD
return_code = uRAD_RP_SDK11.loadConfiguration(mode, f0, BW, Ns, Ntar, Vmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true)
if (return_code != 0):
    closeProgram()

# Infinite detection loop
while True:

    # Target detection request
    return_code, results, raw_results = uRAD_RP_SDK11.detection()
    if (return_code != 0):
        closeProgram()

    # Extract results from outputs
    NtarDetected = results[0]
    velocity = results[2]
    SNR = results[3]

    # Iterate through desired targets
    for i in range(NtarDetected):
        # If SNR is big enough too good to be true y3ni
        if (SNR[i] > 0):
            
            ## FOR TESTING: MAX speed ##
            if (abs(velocity[i]*3.6) > maxim):
               maxim = abs(velocity[i]*3.6)
            ##
            # Prints target information
            speed = 1+velocity[i]*3.6 # +1 for avg. bias
            print(abs(speed)) # 3.6 convFactor m/s -> km/h 
            print("Max = %f km/h" %maxim) # Print max speed for comparison
            
            try:
                speedLimit = db.getSpeedLimit()
            except:
                continue
            
            if (speed > speedLimit):
                t = DT.now()
                time.sleep(0.271588)
                CAM.capture(int(speed))
                #time.sleep(5) # ==== DEBUG
                for x in range(1):
                    filename = ('/home/pi/Desktop/image%s.jpg' % x)
                    try:
                        # ANPR:
                        print("=============Working on ANPR...")
                        np=ANPR.ANPR(filename)
                        print("=============Done ANPR")
                                            
                        # Save image to Firebase after renaming to (np_timestamp.jpg)
                        # AND get image public URL
                        print("=============Uploading Data to Firebase RTDB+Storage...")
                        imageURL = db.uploadData(filename, np, speed)
                        print("=============Uploaded")
                        
                        # Grab name + number from Firebase RTDB:
                        print("=============Grabbing Name & Phone...")
                        name, phone = db.getInfo(np)
                        print(name,phone)
                        
                        # Send SMS:                     
                        #print(type(name),type(np),type(phone), type(speed))
                        print("=============Initiating SMS builder...")
                        sms.send(name, np, phone, str(int(speed)),imageURL)
                        print("=============Done SMS")
                        print(DT.now() - t)
                        print("====================================")
                    except:
                        continue