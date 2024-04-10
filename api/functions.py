from suncalc import get_position, get_times
from datetime import datetime
from stepper import main


def fetch_position(lat=63.41846640168483, longt=10.399527757670084):

    now = datetime.now()

    position = get_position(lat=lat, lng=longt, date=now)
    return position


def move_model(pitch: float, yaw: float, oldPitch: float, oldYaw: float):
    response = main(yaw, pitch, oldYaw, oldPitch)
    return {
        "message": f"Model successfully moved to pitch: {pitch} & yaw {yaw}, from pitch: {oldPitch} & yaw {oldYaw}",
        "z_steps": response["z_steps"],
        "y_steps": response["y_steps"],
    }


# move_model(200.0, -150.0, 100, 50)
