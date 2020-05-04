#!/usr/bin/env python
from flask import stream_with_context,Flask, render_template, Response,request,redirect , url_for
# emulated camera
import uuid
import os
from urllib.parse import quote
from camera import Camera
import cv2

app = Flask(__name__)

@app.route('/')
def live():
       return render_template("index.html")

def gen(camera):
    global frame
    """Video streaming generator function."""
    while True:
        try:
         frame = camera.get_frame()
         x = cv2.imencode('.jpg', frame)[1].tobytes()
      
         yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')
        except Exception as e:
         print(e)
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
