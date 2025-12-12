import io
import threading
import cv2
from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import controls
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN

app = Flask(__name__)

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()
piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})


def webframes():
    while True:
        try:
            frame = piCam.capture_array()
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode(".jpg", frame)
            yield (
                b"--webframe\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )
        except Exception:
            break


@app.route("/")
def index():
    return """
    <html>
    <body>
        <h1>Live Camera</h1>
        <img src="/video_feed">
    </body>
    </html>
    """


@app.route("/video_feed")
def video_feed():
    return Response(
        webframes(),
        mimetype="multipart/x-mixed-replace; boundary=webframe",
    )


async def photo(update: Update, context: CallbackContext):
    frame = piCam.capture_array()
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame, 1)
    _, buffer = cv2.imencode(".jpg", frame)
    bio = io.BytesIO(buffer)
    bio.seek(0)
    await update.message.reply_photo(photo=bio)


def start_bot():
    app_tg = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app_tg.add_handler(CommandHandler("photo", photo))
    app_tg.run_polling()


if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, threaded=True),
        daemon=True,
    ).start()
    start_bot()

