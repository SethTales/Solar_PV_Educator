import urllib.request, json, time

class SolarDataProcessor:
    
    def __init__(self):
        #GET request parameters for solar pv electricity production
        self.format = "json"
        self.api_key = "rH3Vxikvbxm5SnbW3Lxgs3c76L4hjbXph0NoQlzw"
        self.sys_cap = "0.0"
        self.module_type = "0"
        self.losses = "14"
        self.array_type = "1"
        self.tilt = "0.0"
        self.azimuth = "0.0"
        self.address = "#####"
        self.elecCost = 0.0 
        self.pvWattsRequestParams = []
        self.pvWattsApiRequestUrl = "https://developer.nrel.gov/api/pvwatts/v5." + self.format + "?" + "api_key=" + self.api_key + "&address=" + self.address + \
        "&system_capacity=" + self.sys_cap + "&azimuth=" + self.azimuth + "&tilt=" + self.tilt + "&array_type=" + self.array_type + \
        "&module_type=" + self.module_type + "&losses=" + self.losses
        self.pvWattsJsonResponse = None

        #GET response parameters 
        self.ac_monthly = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0   ]
        self.ac_annual = None
        self.capacity_factor = None
        self.station_state = ""
        self.station_city = None

        #GET request parameters for open_pv
        self.minsize = ""
        self.maxsize = ""
        self.mindate = ""
        self.openPvApiRequestUrl = "https://developer.nrel.gov/api/solar/open_pv/installs/summaries?api_key=" + self.api_key + "&state=" + self.station_state \
        + "&minsize=" + self.minsize + "&maxsize=" + self.maxsize + "&mindate=" + self.mindate
        self.openPvJsonResponse = None

        #GET response parameters for open_pv
        self.highAvgCostPerWatt = 3.75
        self.lowAvgCostPerWatt = 2.75

        self.lowCostEstimate = 0
        self.highCostEstimate = 0
        self.lowCostAfterIncentives = 0
        self.highCostAfterIncentives = 0
        self.breakevenYearLow = 0
        self.breakevenYearHigh = 0
        self.tenYearSavingsLow = 0
        self.tenYearSavingsHigh = 0
        self.twentyYearSavingsLow = 0
        self.twentyYearSavingsHigh = 0  
     

    def calculateRequestProcessor(self, _requestParams = []):
        self.pvWattsRequestParams = list(_requestParams)
        print(self.pvWattsRequestParams)
        self.setPvWattsRequestParams()
        self.pvWattsJsonResponse = self.sendApiRequest(self.pvWattsApiRequestUrl)
        self.parsePvWattsResponse()
        #self.setOpenPVRequestParams()
        #self.openPvJsonResponse = self.sendApiRequest(self.openPvApiRequestUrl)
        #self.parsOpenPvResponse()
        self.calculateCostsAndRoi()
    
    def setPvWattsRequestParams(self):
        self.address = self.pvWattsRequestParams[0]
        self.sys_cap = self.pvWattsRequestParams[1]
        self.azimuth = self.pvWattsRequestParams[2]
        self.tilt = self.pvWattsRequestParams[3]
        self.array_type = self.pvWattsRequestParams[4]
        self.module_type = self.pvWattsRequestParams[5]
        self.losses = self.pvWattsRequestParams[6]
        self.elecCost = self.pvWattsRequestParams[7]

        if self.array_type == "Fixed - open-rack":
            self.array_type = "0"
        elif self.array_type == "Fixed - roof-mounted":
            self.array_type = "1"
        elif self.array_type == "1-axis tracker":
            self.array_type = "2"
        elif self.array_type == "1-axis backtracker":
            self.array_type = "3"
        elif self.array_type == "2-axis tracker":
            self.array_type = "4"

        if self.module_type == "Standard (14-17%)":
            self.module_type = "0"
        elif self.module_type == "Premium (18-20%)":
            self.module_type = "1"
        elif self.module_type == "Thin-film (~11%)":
            self.module_type = "2"

        self.pvWattsApiRequestUrl = "https://developer.nrel.gov/api/pvwatts/v5." + self.format + "?" + "api_key=" + self.api_key + "&address=" + self.address + \
        "&system_capacity=" + self.sys_cap + "&azimuth=" + self.azimuth + "&tilt=" + self.tilt + "&array_type=" + self.array_type + \
        "&module_type=" + self.module_type + "&losses=" + self.losses

    def sendApiRequest(self, urlStr):
        httpResponse = urllib.request.urlopen(urlStr).read().decode('utf8')
        jsonResponse = json.loads(httpResponse)
        print(jsonResponse)
        return(jsonResponse)
    
    def parsePvWattsResponse(self):
        #
        # tempList = []
        for i in range (0, 12):
            #tempList.append((self.pvWattsJsonResponse["outputs"]["ac_monthly"][i]))
            #self.ac_monthly[i] = (['{0:.2f}'.format(tempList[i])])
            self.ac_monthly[i] = (self.pvWattsJsonResponse["outputs"]["ac_monthly"][i])
        print(self.ac_monthly)
        self.ac_annual = (self.pvWattsJsonResponse["outputs"]["ac_annual"])
        print(self.ac_annual)
        self.capacity_factor = (self.pvWattsJsonResponse["outputs"]["capacity_factor"])
        print(self.capacity_factor)
        self.station_city = (self.pvWattsJsonResponse["station_info"]["city"])
        print(self.station_city)
        self.station_state = (self.pvWattsJsonResponse["station_info"]["state"])
        print(self.station_state)

    def calculateCostsAndRoi(self):
        self.lowCostEstimate = self.lowAvgCostPerWatt * float(self.sys_cap) * 1000
        self.highCostEstimate = self.highAvgCostPerWatt * float(self.sys_cap) * 1000      

        self.lowCostAfterIncentives = self.lowCostEstimate * 0.70
        self.highCostAfterIncentives = self.highCostEstimate * 0.70       

        self.breakevenYearLow = self.lowCostAfterIncentives / (float(self.ac_annual) * float(self.elecCost))
        self.breakevenYearHigh = self.highCostAfterIncentives / (float(self.ac_annual) * float(self.elecCost))          

        self.tenYearSavingsLow = (float(self.ac_annual) * float(self.elecCost) * 10) - self.highCostAfterIncentives 
        self.tenYearSavingsHigh = (float(self.ac_annual) * float(self.elecCost) * 10) - self.lowCostAfterIncentives 
        self.twentyYearSavingsLow = (float(self.ac_annual) * float(self.elecCost) * 20) - self.highCostAfterIncentives 
        self.twentyYearSavingsHigh = (float(self.ac_annual) * float(self.elecCost) * 20) - self.lowCostAfterIncentives 

        self.ac_annual = "{:.2f}".format(self.ac_annual)
        self.lowCostEstimate = "{:.2f}".format(self.lowCostEstimate)
        self.highCostEstimate = "{:.2f}".format(self.highCostEstimate)
        self.lowCostAfterIncentives = "{:.2f}".format(self.lowCostAfterIncentives)
        self.highCostAfterIncentives = "{:.2f}".format(self.highCostAfterIncentives)
        self.breakevenYearLow = int(self.breakevenYearLow)
        self.breakevenYearHigh = int(self.breakevenYearHigh)
        self.tenYearSavingsLow = "{:.2f}".format(self.tenYearSavingsLow)
        self.tenYearSavingsHigh = "{:.2f}".format(self.tenYearSavingsHigh)
        self.twentyYearSavingsLow = "{:.2f}".format(self.twentyYearSavingsLow)
        self.twentyYearSavingsHigh = "{:.2f}".format(self.twentyYearSavingsHigh)

        print(self.lowCostEstimate)
        print(self.highCostEstimate)
        print(self.lowCostAfterIncentives)
        print(self.highCostAfterIncentives)
        print(self.breakevenYearLow)
        print(self.breakevenYearHigh)
        print(self.tenYearSavingsLow)
        print(self.tenYearSavingsHigh)
        print(self.twentyYearSavingsLow)
        print(self.twentyYearSavingsHigh)

        #self.breakevenYearLow = float(self.averageCostEstimate) / (float(self.ac_annual) * float(self.elecCost))
        #print(self.breakevenYear) 

    def getOutputs(self):
        outputsDict = {'anKwh': self.ac_annual, 'lcEst': str(self.lowCostEstimate), 'hcEst': str(self.highCostEstimate), \
        'lcEstIncentives': str(self.lowCostAfterIncentives), 'hcEstIncentives': str(self.highCostAfterIncentives), \
        'brkYearLow': str(self.breakevenYearLow), 'brkYearHigh': str(self.breakevenYearHigh), '10yrSvgsLow': str(self.tenYearSavingsLow), \
        '10yrSvgsHigh': str(self.tenYearSavingsHigh), '20yrSvgsLow': str(self.twentyYearSavingsLow), '20yrSvgsHigh': str(self.twentyYearSavingsHigh) }

        return(outputsDict)



