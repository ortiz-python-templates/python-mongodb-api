from enum import Enum


class ActivityStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"