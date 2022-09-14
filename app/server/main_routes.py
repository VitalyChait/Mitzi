#!/usr/bin/env python3
from flask import render_template, Response
from flask_login import login_required

from . import main
from .. import cam, controller
from ..hardware.camera import getCameraGenerator, getCameraFrame


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    data = {'xPos': controller.getXPos(),
            'yPos': controller.getYPos(),
            'zPos': controller.getZPos(),
            "xStepCount": controller.getXStepCount(),
            "yStepCount": controller.getYStepCount(),
            "zStepCount": controller.getZStepCount(),
            'camStatus': cam.isOK()}
    return render_template('profile.html', data=data)


@main.route('/camera/stream')
@login_required
def cameraStream():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(getCameraGenerator(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/camera/frame')
@login_required
def cameraFrame():
    """Image route. Put this in the src attribute of an img tag."""
    return Response(getCameraFrame(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/camera/error')
@login_required
def cameraError():
    return Response(getCameraFrame(cam=None), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/camera/control')
@login_required
def cameraControl():
    data = {"camStatus": cam.isOK()}
    return render_template('cameraControl.html', data=data)


@main.route('/camera/on')
@main.route('/camera/on/<portID>')
@login_required
def cameraOn(portID=None):
    if cam.isOK():
        return "Camera already on"
    if cam.isInit():
        cam.startThread()
        return "Camera resumes action"
    else:
        if portID is not None:
            try:
                portID = int(portID)
            except ValueError:
                portID = None
        cam.reStart(portID=portID)
    if cam.isOK():
        return "Camera turned on"
    return "Error"


@main.route('/camera/off')
@login_required
def cameraOff():
    cam.terminateCamera()
    return "Camera closed"


@main.route('/camera/continue')
@login_required
def cameraContinue():
    if cam.isOK():
        return "Camera already on"
    if cam.isInit():
        cam.startThread()
        return "Camera resumes action"
    else:
        return "Camera is not turned on"


@main.route('/camera/stop')
@login_required
def cameraStop():
    cam.terminateThread()
    return "Thread closed"


@main.route('/camera/reset')
@main.route('/camera/reset/<portID>')
@login_required
def cameraReset(portID=None):
    if portID is not None:
        try:
            portID = int(portID)
        except ValueError:
            portID = None
    cam.reStart(portID=portID)
    if cam.isOK():
        return "Camera Restarted"
    return "Error"


@main.route('/motor/')
@login_required
def motor():
    data = {'xPos': controller.getXPos(),
            'yPos': controller.getYPos(),
            'zPos': controller.getZPos(),
            "xStepCount": controller.getXStepCount(),
            "yStepCount": controller.getYStepCount(),
            "zStepCount": controller.getZStepCount()}
    return render_template('motor.html', data=data)


@main.route('/motor/disable')
@login_required
def motorOff():
    controller.cleanupMotor()
    return "Motor disabled"


@main.route('/motor/init')
@login_required
def motorInit():
    controller.setupMotor()
    return "Motor enabled"


@main.route('/motor/set/x/<value>')
@login_required
def setx(value):
    try:
        value = int(value)
    except ValueError:
        return "Error"
    old_value = controller.getXPos()
    value = value % controller.getXStepCount()
    delta = value - old_value
    if delta != 0:
        if delta > 0:
            controller.xfw(delta)
        elif value < 0:
            controller.xbw(-delta)

    if old_value != controller.getXPos():
        return "Done moving"
    return ""


@main.route('/motor/set/y/<value>')
@login_required
def sety(value):
    try:
        value = int(value)
    except ValueError:
        return "Error"
    old_value = controller.getYPos()
    value = value % controller.getYStepCount()
    delta = value - old_value
    if delta != 0:
        if delta > 0:
            controller.yfw(delta)
        elif value < 0:
            controller.ybw(-delta)

    if old_value != controller.getYPos():
        return "Done moving"
    return ""


@main.route('/motor/set/z/<value>')
@login_required
def setz(value):
    try:
        value = int(value)
    except ValueError:
        return "Error"
    old_value = controller.getZPos()
    value = value % controller.getZStepCount()
    delta = value - old_value
    if delta != 0:
        if delta > 0:
            controller.zfw(delta)
        elif value < 0:
            controller.zbw(-delta)
    if old_value != controller.getZPos():
        return "Done moving"
    return ""
