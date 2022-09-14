#!/usr/bin/env python3
import atexit
from app import create_app, socketio, cam, controller
import eventlet


app = create_app()

if __name__ == '__main__':
    socketio.run(app, port=5000, host='0.0.0.0')


# EXIT
@atexit.register
def closing():
    controller.cleanupMotor()
    cam.terminateCamera()
