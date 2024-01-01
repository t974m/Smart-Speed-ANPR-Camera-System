from picamera import PiCamera, Color
from datetime import datetime as DT # For timestamp
import time

camera = PiCamera() #Camera Object

#Day
camera.resolution = (1640, 922)
camera.framerate = 30
camera.shutter_speed = 1050
#Night:
# camera.framerate = 6
# camea.shutter_speed = 45000
camera.exposure_mode = 'off'
#camera.awb_mode='off'
#camera.iso = 200

#camera.start_preview()
#camera.capture(10)
def capture(speed): #Arg:Speed from uRAD
    #Black text on White background
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    #Timestamp+speed
    camera.annotate_text_size = 78
    camera.annotate_text = (DT.now().strftime('%Y/%m/%d %H:%M:%S') + " %s km/h" % speed)
    #Capture 5 flash consec. images
    #t = DT.now()
    camera.capture_sequence([
        '/home/pi/Desktop/image%s.jpg'
        %i for i in range(1)], use_video_port=True) #range can be the number of pictures n
    #print(DT.now() - t)

#capture(100)