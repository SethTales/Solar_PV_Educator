import urllib.request, json, time, copy

class SolarDataProcessor:
    
    def __init__(self):
        #setting request parameters default values 
        #see https://developer.nrel.gov/docs/solar/pvwatts-v5/ for more details
        #all but elecCost are string, because they are part of pvWattsApiRequestUrl
        #elecCost is float as it is used in calculations in functions below
        self.formInputReceiver = FormInputReceiver()
        self.apiRequestProcessor = ApiRequestProcessor()
        self.apiResponseParser = ApiResponseParser()
        self.costAndRoiCalculator = CostAndRoiCalculator()
        self.elecCost = 0.0 
        self.pvWattsJsonResponse = None
        self.electricityProductionData = []
        self.outputsDict = {}

        #GET response parameters 
        self.ac_monthly = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.ac_annual = "0.0"
        self.station_state = ""
        self.station_city = ""

    def requestProcessor(self, requestParams = []):
        #transfer form data to request parameters for PvWatts
        self.pvWattsRequestParams = self.formInputReceiver.getFormInputValues(requestParams)
        #send request parameters to API requester class
        self.apiRequestProcessor.setPvWattsRequestParams(self.pvWattsRequestParams)
        #send api request and store in a JSON respoonse variable
        self.pvWattsJsonResponse = self.apiRequestProcessor.sendApiRequest()
        #parse response 
        self.electricityProductionData = self.apiResponseParser.parsePvWattsResponse(self.pvWattsJsonResponse)
        self.ac_annual = self.electricityProductionData[0]
        print(self.electricityProductionData[0])
        for i in range (1, 13):
            self.ac_monthly[i - 1] = self.electricityProductionData[i]
            print(i, self.electricityProductionData[i])
        self.outputsDict = copy.deepcopy((self.costAndRoiCalculator.calculateCostsAndRoi(self.ac_annual, self.pvWattsRequestParams)))
        return(self.outputsDict)

class FormInputReceiver:
    def __init__(self):
        self.formInputKeys = ["address", "system_capacity", "azimuth", "tilt", "array_type", "module_type", "losses", "elecCost"]

    def getFormInputValues(self, requestParams = []):
        self.formInputDict = dict(zip(self.formInputKeys, requestParams))
        return(self.formInputDict)

class ApiRequestProcessor:
    def __init__(self):
        self.format = "json"
        self.api_key = "rH3Vxikvbxm5SnbW3Lxgs3c76L4hjbXph0NoQlzw"
        self.pvWattsApiRequestUrl = ""
        self.pvWattsJsonResponse = None

    def setPvWattsRequestParams(self, pvWattsRequestParams = {}):
        print("setPvWattsRequestParams called")
        address = pvWattsRequestParams["address"]
        sys_cap = pvWattsRequestParams["system_capacity"]
        azimuth = pvWattsRequestParams["azimuth"]
        tilt = pvWattsRequestParams["tilt"]
        array_type = pvWattsRequestParams["array_type"]
        module_type = pvWattsRequestParams["module_type"]
        losses = pvWattsRequestParams["losses"]

        #convert text array types from HTML form to index # so they are in proper form for GET request to PvWatts
        if array_type == "Fixed - open-rack":
            array_type = "0"
        elif array_type == "Fixed - roof-mounted":
            array_type = "1"
        elif array_type == "1-axis tracker":
            array_type = "2"
        elif array_type == "1-axis backtracker":
            array_type = "3"
        elif array_type == "2-axis tracker":
            array_type = "4"

        #convert text module types from HTML form to index # so they are in proper form for GET request to PvWatts
        if module_type == "Standard (14-17%)":
            module_type = "0"
        elif module_type == "Premium (18-20%)":
            module_type = "1"
        elif module_type == "Thin-film (~11%)":
            module_type = "2"

        self.pvWattsApiRequestUrl = "https://developer.nrel.gov/api/pvwatts/v5." + self.format + "?" + "api_key=" + self.api_key + "&address=" + address + \
        "&system_capacity=" + sys_cap + "&azimuth=" + azimuth + "&tilt=" + tilt + "&array_type=" + array_type + \
        "&module_type=" + module_type + "&losses=" + losses
        print(self.pvWattsApiRequestUrl)

        #self.pvWattsJsonResponse = self.sendApiRequest()

    def sendApiRequest(self):
        print("sendApiRequest called")
        httpResponse = urllib.request.urlopen(self.pvWattsApiRequestUrl).read().decode('utf8')
        self.pvWattsJsonResponse = json.loads(httpResponse)
        return(self.pvWattsJsonResponse)

class ApiResponseParser:

    def __init__(self):
        
        self.electricityProductionData = []

    def parsePvWattsResponse(self, pvWattsJsonResponse):
        if len(self.electricityProductionData) >= 1:
            self.electricityProductionData.clear()        

        self.electricityProductionData.append(pvWattsJsonResponse["outputs"]["ac_annual"])

        for i in range (0, 12):
            self.electricityProductionData.append(pvWattsJsonResponse["outputs"]["ac_monthly"][i])
            print(self.electricityProductionData[i])
        return(self.electricityProductionData)

class CostAndRoiCalculator:

    def __init__(self):
        #self.ac_annual = 0.0
        self.systemCapacity = 0.0
        self.elecCostPerKwh = 0.0
        self.highAvgCostPerWatt = 3.75
        self.lowAvgCostPerWatt = 2.75
        self.costAndRoiDict = {"ac_annual":"", "lowCostEstimate":"", "highCostEstimate":"", "lowCostAfterIncentives":"", "highCostAfterIncentives":"", "breakevenYearLow":"", \
        "breakevenYearHigh":"", "tenYearSavingsLow":"", "tenYearSavingsHigh":"", "twentyYearSavingsLow":"", "twentyYearSavingsHigh":""}

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

    def calculateCostsAndRoi(self, ac_annual, requestParams = []):

        self.lowCostEstimate = self.lowAvgCostPerWatt * float(requestParams["system_capacity"]) * 1000
        self.highCostEstimate = self.highAvgCostPerWatt * float(requestParams["system_capacity"]) * 1000      

        self.lowCostAfterIncentives = self.lowCostEstimate * 0.70
        self.highCostAfterIncentives = self.highCostEstimate * 0.70       

        self.breakevenYearLow = self.lowCostAfterIncentives / (float(ac_annual) * float(requestParams["elecCost"]))
        self.breakevenYearHigh = self.highCostAfterIncentives / (float(ac_annual) * float(requestParams["elecCost"]))          

        self.tenYearSavingsLow = (float(ac_annual) * float(requestParams["elecCost"]) * 10) - self.highCostAfterIncentives 
        self.tenYearSavingsHigh = (float(ac_annual) * float(requestParams["elecCost"]) * 10) - self.lowCostAfterIncentives 
        self.twentyYearSavingsLow = (float(ac_annual) * float(requestParams["elecCost"]) * 20) - self.highCostAfterIncentives 
        self.twentyYearSavingsHigh = (float(ac_annual) * float(requestParams["elecCost"]) * 20) - self.lowCostAfterIncentives 

        self.costAndRoiDict["ac_annual"] = "{:.2f}".format(ac_annual)
        self.costAndRoiDict["lowCostEstimate"] = "{:.2f}".format(self.lowCostEstimate)
        self.costAndRoiDict["highCostEstimate"] = "{:.2f}".format(self.highCostEstimate)
        self.costAndRoiDict["lowCostAfterIncentives"] = "{:.2f}".format(self.lowCostAfterIncentives)
        self.costAndRoiDict["highCostAfterIncentives"] = "{:.2f}".format(self.highCostAfterIncentives)
        self.costAndRoiDict["breakevenYearLow"] = int(self.breakevenYearLow)
        self.costAndRoiDict["breakevenYearHigh"] = int(self.breakevenYearHigh)
        self.costAndRoiDict["tenYearSavingsLow"] = "{:.2f}".format(self.tenYearSavingsLow)
        self.costAndRoiDict["tenYearSavingsHigh"] = "{:.2f}".format(self.tenYearSavingsHigh)
        self.costAndRoiDict["twentyYearSavingsLow"] = "{:.2f}".format(self.twentyYearSavingsLow)
        self.costAndRoiDict["twentyYearSavingsHigh"] = "{:.2f}".format(self.twentyYearSavingsHigh)

        return(self.costAndRoiDict)



    


        



