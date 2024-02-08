import cv2
from picamera2 import Picamera2
from libcamera import controls
piCam = Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888" #opencv wants it in BGR format
piCam.preview_configuration.align() #It helps run faster, it changes the size to the closest std size
piCam.configure("preview") # 3 things for configure, preview, video, still_images
piCam.start()

while True:
    piCam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    frame=piCam.capture_array()
    rotated_image = cv2.transpose(frame)
    rotated_image = cv2.flip(rotated_image, flipCode=1)
    #cv2.imshow("piCam", frame)
    cv2.imshow("piCam", rotated_image)
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()