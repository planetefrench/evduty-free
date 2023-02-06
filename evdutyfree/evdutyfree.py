"""
Evduty-free class

"""

from datetime import datetime
import json
import requests

class EVdutyFree:
    """API to access EVduty in Python"""   
    LOGIN_TEMPLATE = {
        'device': {
            "id": "A",
            "model": "A",
            "type": "ANDROID"
        },
        "email": "INVALID",
        "password": "INVALID"
    }

    """Create an instance of the API connector for EVduty"""
    def __init__(self, username, password, request_get_timeout = 30, jwt_token_drift = 0):
        self.username = username
        self.password = password
        self._request_get_timeout = request_get_timeout
        self.baseurl = "https://api-evduty.agylev.com/"
        self.jwt_token_drift = jwt_token_drift
        self.jwttoken = ""
        self.jwttoken_ttl = 0
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
        }

    @property
    def request_get_timeout(self):
        """The timeout before the request will return"""
        return self._request_get_timeout

    def authenticate(self):
        """Authenticate to the EVduty api and obtain a bearer token"""
        if self.jwttoken != "" and round(
            (self.jwttoken_ttl / 1000) - self.jwt_token_drift, 0
        ) > datetime.timestamp(datetime.now()):
            return

        jlogin = self.LOGIN_TEMPLATE
        jlogin["email"] = self.username
        jlogin["password"] = self.password

        try:
            response = requests.post(
                f"{self.baseurl}v1/account/login",
                json=jlogin,
                timeout=self._request_get_timeout
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        auto_response = json.loads(response.text)
        self.jwttoken = auto_response["accessToken"]
        self.jwttoken_ttl = auto_response["expiresIn"]
        self.headers["Authorization"] = f"Bearer {self.jwttoken}"

    def get_station_info(self):
        """Return a dict of all of the stations for the account"""
        try:
            response = requests.get(
                f"{self.baseurl}v1/account/stations",
                headers=self.headers,
                timeout=self._request_get_timeout
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        return json.loads(response.text)

    def get_station_ids(self):
        """Returns a list of station ids for the authenticated user"""
        stationids = []

        stations = self.get_station_info()

        for station in stations:
            stationids.append(station["id"])
        return stationids

    def get_terminal_ids(self, stationid):
        """Returns a list of terminals for the given stationId"""
        terminals = []
        stations = self.get_station_info()

        for station in stations:
            if station["id"] == stationid:
                for terminal in station["terminals"]:
                    terminals.append(terminal["id"])

        return terminals

    def get_terminal_info(self, stationid, termninalid):
        """Get all info about a terminal"""
        try:
            terminalinfo = requests.get(
                f"{self.baseurl}v1/account/stations/{stationid}/terminals/{termninalid}",
                headers=self.headers,
                timeout=self._request_get_timeout
            )
            terminalinfo.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        return json.loads(terminalinfo.text)

    def get_max_terminal_charging_current(self, stationid, terminalid):
        """Get the maximum charging current a terminal supports"""
        terminal = self.get_terminal_info(stationid, terminalid)
        return terminal["amperage"]

    def set_max_charging_current(self, stationid, termninalid, current):
        """Set the max charging current for the terminal, if that current is higher than
           the maximum that the terminal supports, the command will fail."""
        terminal = self.get_terminal_info(stationid, termninalid)

        # these values can't be sent back, remove them
        del terminal["cost"]
        del terminal["alternateCost"]

        terminal["chargingProfile"] = {"chargingRate":current, "chargingRateUnit": "A"}

        try:
            response = requests.put(
                f"{self.baseurl}v1/account/stations/{stationid}/terminals/{termninalid}",
                headers=self.headers,
                timeout=self._request_get_timeout,
                json=terminal
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

    def get_max_charging_current(self, stationid, terminalid):
        """Get the maximum charging current set
           TODO: this assumes that the charging profile rate is in amps, fix that"""
        terminal = self.get_terminal_info(stationid, terminalid)

        if "chargingProfile" in terminal:
            return terminal["chargingProfile"]["chargingRate"]

        return terminal["amperage"]
