from enum import Enum


class ActivityStatus(str, Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"