from suncalc import get_position, get_times
from datetime import datetime


def fetch_position():
    lat = 63.41846640168483
    longt = 10.399527757670084

    now = datetime.now()

    position = get_position(lat=lat, lng=longt, date=now)
    return position


def move_model(angle: int):
    return {"message": f"Model successfully moved to angle: {angle}"}
