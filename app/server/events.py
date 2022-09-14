from flask_socketio import emit
from .. import socketio, controller, cam


def receivePingCallback():
    print("Received by user")


def receiveMotorCallback():
    print("Motor update received by user")


def receiveCameraCallback():
    print("Camera update received by user")


@socketio.on('ping')
def handle_ping(data):
    print("received", data)
    socketio.emit('pong', data, broadcast=True)


@socketio.on('motor_update_event')
def motor_u_event(data):

    data = {'xPos': data["xPos"],
            'yPos': data["yPos"],
            'zPos': data["zPos"]}
    emit('motor_update_response', data, broadcast=True)


@socketio.on('camera_update_event')
def camera_u_event(data):
    data = {'camStatus': data}
    emit('camera_update_response', data, broadcast=True)
