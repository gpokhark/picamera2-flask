import io
from picamera2 import Picamera2
from libcamera import controls
from flask import Flask, Response
import cv2
from telegram import Update
from telegram.ext import Updater, Application, CommandHandler, CallbackContext
import threading
from config import TELEGRAM_BOT_TOKEN

app = Flask(__name__)

piCam = Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888" #opencv wants it in BGR format
piCam.preview_configuration.align() #It helps run faster, it changes the size to the closest std size
piCam.configure("preview") # 3 things for configure, preview, video, still_images
piCam.start()

piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#frame=piCam.capture_array()
#rotated_image = cv2.transpose(frame)
#rotated_image = cv2.flip(rotated_image, flipCode=1)
#frame = rotated_image


def webframes():
    print("Entering live feed")
    global frame, piCam
    
    #piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    #frame=piCam.capture_array()
    #rotated_image = cv2.transpose(frame)
    #rotated_image = cv2.flip(rotated_image, flipCode=1)
    #frame = rotated_image
    #cv2.waitKey(1)
    
    while True:
        #frame = camera.capture_arry("main")
        #cv2.waitKey(1)
        try:
            frame = piCam.capture_array()  # Capture the frame inside the loop
            rotated_image = cv2.transpose(frame)
            rotated_image = cv2.flip(rotated_image, flipCode=1)
            frame = rotated_image
            ret, buffer = cv2.imencode('.jpg', frame)
            webframe = buffer.tobytes()
            yield (b'--webframe\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + webframe + b'\r\n')
        except:
            break




@app.route('/video_feed')
def video_feed():
    return Response(webframes(), mimetype='multipart/x-mixed-replace; boundary=webframe')

async def photo(update: Update, context: CallbackContext):
    frame = piCam.capture_array()
    rotated_image = cv2.transpose(frame)
    rotated_image = cv2.flip(rotated_image, flipCode=1)
    frame = rotated_image
    ret, buffer = cv2.imencode('.jpg', frame)
    io_buff = io.BytesIO(buffer)
    io_buff.seek(0)
    await update.message.reply_photo(photo=io_buff)

def start_bot():
    TOKEN = TELEGRAM_BOT_TOKEN
    application = Application.builder().token(TOKEN).build()

    # Add handler for /photo command
    application.add_handler(CommandHandler('photo',photo))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, threaded=True)
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, threaded=True)).start()
    start_bot()
