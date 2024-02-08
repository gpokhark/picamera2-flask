import io
from picamera2 import Picamera2
from libcamera import controls
from flask import Flask, Response
import cv2

app = Flask(__name__)

piCam = Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888" #opencv wants it in BGR format
piCam.preview_configuration.align() #It helps run faster, it changes the size to the closest std size
piCam.configure("preview") # 3 things for configure, preview, video, still_images
piCam.start()

piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
frame=piCam.capture_array()
rotated_image = cv2.transpose(frame)
rotated_image = cv2.flip(rotated_image, flipCode=1)
frame = rotated_image



#fourcc = cv2.VideoWriter_fourcc(*'mp4v') 

#def generate_frames():
#    #with picamera.PiCamera() as camera:
#    with picamera2.Picamera2() as camera:
#        camera.resolution = (640, 480)
#        camera.framerate = 24
#        stream = io.BytesIO()

#        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
#            stream.seek(0)
#            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
#            stream.seek(0)
#            stream.truncate()

def webframes():
    print("Entering live feed")
    global frame
    
    piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    frame=piCam.capture_array()
    rotated_image = cv2.transpose(frame)
    rotated_image = cv2.flip(rotated_image, flipCode=1)
    frame = rotated_image
    cv2.waitKey(1)
    
    while True:
        #frame = camera.capture_arry("main")
        #cv2.waitKey(1)
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            webframe = buffer.tobytes()
            yield (b'--webframe\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + webframe + b'\r\n')
        except:
            break




@app.route('/video_feed')
def video_feed():
    return Response(webframes(), mimetype='multipart/x-mixed-replace; boundary=webframe')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
