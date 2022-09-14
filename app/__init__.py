#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO


DUMMY = True


def init_video_port():
    if not DUMMY:
        from .hardware.camera import checkVideoPort
        return checkVideoPort()
    else:
        from .hardware.camera import DummyVideoPort
        return DummyVideoPort()


def init_video_camera():
    camPort = init_video_port()
    if not DUMMY:
        from .hardware.camera import VideoCameraCV
        return VideoCameraCV(camPort)
    else:
        from .hardware.camera import DummyVideoCamera
        return DummyVideoCamera(camPort)


def init_controller():
    if not DUMMY:
        from .hardware.motorcontroller import MotorController
        motor_settings = {"x": True,
                          "y": True,
                          "z": True,
                          "xStepCount": 50,
                          "yStepCount": 50,
                          "zStepCount": 200}
        return MotorController(**motor_settings)
    else:
        from .hardware.motorcontroller import DummyMotorController
        motor_settings = {"x": True,
                          "y": True,
                          "z": True,
                          "xStepCount": 50,
                          "yStepCount": 50,
                          "zStepCount": 200}
        return DummyMotorController(**motor_settings)


# socketIO
socketio = SocketIO(async_mode="threading")
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
# Init Camera Hardware
cam = init_video_camera()
# Init Motor Hardware
controller = init_controller()


def create_app(debug=False):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Ch!na2022'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = debug
    app.config['THREADED'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .server.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .server.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .server.main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)

    return app
