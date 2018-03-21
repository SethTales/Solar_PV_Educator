import urllib.request, json

class ElectricityInputs:
    
    def __init__(self):
        #GET request parameters for solar pv electricity production
        self.format = "json"
        self.api_key = "rH3Vxikvbxm5SnbW3Lxgs3c76L4hjbXph0NoQlzw"
        self.sys_cap = 0.0
        self.module_type = 0
        self.losses = 14.0
        self.array_type = 1
        self.tilt = 0.0
        self.azimuth = 0.0
        self.address = "#####" 
        self.apiRequestUrl = "https://developer.nrel.gov/api/pvwatts/v5." + self.format + "?" + "api_key=" + self.api_key + "&address=" + self.address + \
        "&system_capacity=" + str(self.sys_cap) + "&azimuth=" + str(self.azimuth) + "&tilt=" + str(self.tilt) + "&array_type=" + str(self.array_type) + \
        "&module_type=" + str(self.module_type) + "&losses=" + str(self.losses)

    def makeApiRequest(self):
        response = urllib.request.urlopen(self.apiRequestUrl)
        data = json.loads(response)
        print(data)
        return(data)

class ElectricityOutputs:
    
    def __init__(self):
        #GET request response for solar pv electricity production
        self.ac_monthly = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.ac_annual = None
        self.capacity_factor = None
        self.station_state = None
        self.station_city = None

