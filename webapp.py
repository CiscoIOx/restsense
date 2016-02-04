import requests
from bottle import Bottle


class WebApp(Bottle):
    """
    Open a HTTP/TCP Port and spit out json response.
    """
    def __init__(self, sdc, cfg):
        self.sdc = sdc
        self.weather_server_ip = cfg.get("weather", "server")
        self.weather_server_port = cfg.get("weather", "port")
        self.weather_api_key = cfg.get("weather", "apikey")
        self.zipcode = cfg.get("weather", "zipcode")
        Bottle.__init__(self)
        self.route("/", callback=self.index)
        self.route("/alarms", callback=self.alarms)
        self.route("/reset", callback=self.reset_alarms)
        self.route("/weather", callback=self.weather)
        self.route("/hello", callback=self.hello)
    
    def hello(self):
        return {"msg": "hello"}

    def index(self):
        return self.sdc.get_snapshot()

    def alarms(self):
        return self.sdc.get_alarms()

    def reset_alarms(self):
        return self.sdc.reset_alarms()

    def weather(self):
        url = "{SERVER}:{PORT}/api/{APIKEY}/conditions/q/{ZIPCODE}.json".format(
            SERVER=self.weather_server_ip,
            PORT=self.weather_server_port,
            APIKEY=self.weather_api_key,
            ZIPCODE=self.zipcode
        )

        r = requests.get(url)
        if r.ok:
            if r.headers["content-type"] == "application/json":
                return r.json()
            return r.text
        else:
            raise Exception("Error reading weather data. Upstream server returned %s" % r.status_code)

