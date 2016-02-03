import logging
import json
import random
import datetime

logger = logging.getLogger("restsense")

class SensorDataCollector(object):
    """
    This is a dummy data collector interface that will currently generate
    random sensor data.
    """

    __singleton = None # the one, true Singleton

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
        #if not cls.__singleton:
            cls.__singleton = super(SensorDataCollector, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self, cfg):
        self.cfg = cfg
        self.poll_frequency = self.cfg.get("sensors", "poll_frequency")
        self.alarms = list()

    def get_snapshot(self):
        d = dict()
        d["sensors"] = {}
        d["sensors"]["living_room_temperature"] = {"status" : "OK", "value": str(random.randrange(20, 30)), "unit" : "degree c"}
        d["sensors"]["perimeter_security"] = {"status" : "OK", "value": "armed", "unit" : "boolean"}
        return d

    def get_alarms(self):
        if random.random() > 0.5:
            self.alarms.append("Perimeter breach detected at %s" % datetime.datetime.strftime(
                datetime.datetime.now(),
                "%Y-%m-%d %H:%M:%S"))

        if len(self.alarms) > 0:
            return {"alarms": self.alarms}
        else:
            return {"alarms": 0}

    def reset_alarms(self):
        del self.alarms[:]
        return {"msg": "All alarms are reset"}
