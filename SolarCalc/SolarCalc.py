import os, calendar, jinja2
from flask import Flask, request, session, g, redirect, abort, url_for, render_template, flash
from SolarCalc.model import SolarDataProcessor

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SOLARCALC_SETTINGS', silent=True)

solarDataProcessor = SolarDataProcessor()

@app.route('/', methods = ['GET'])
def initMonthTable():
    kwh = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthlyData = []
    for i in range (0, 12):
        a_month = dict(month=month[i], kwhPerMonth=kwh[i])
        monthlyData.append(a_month)
 
    return render_template('mainLayout.html', monthlyData = monthlyData)

if __name__ == "__main__":
    app.run()

@app.route('/results', methods = ['POST'])
def electricityInputData():
    kwh = solarDataProcessor.ac_monthly
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthlyData = []
    for i in range (0, 12):
        a_month = dict(month=month[i], kwhPerMonth=kwh[i])
        monthlyData.append(a_month)
    
    #gets form variables from user input and stores them
    selectArrType = request.form.get('arrTypeDropdown')
    selectModType = request.form.get('modTypeDropdown')
    zipCode = request.form['zip']
    elecCost = request.form['costPerKwh']
    sysCap = request.form['sys_cap']
    tilt = request.form['tilt']
    azimuth = request.form['azimuth']
    losses = request.form['losses']

    #pass variables to model.py to make pvWatts API request
    requestParams = [zipCode, sysCap, azimuth, tilt, selectArrType, selectModType, losses, elecCost]
    outputs = solarDataProcessor.requestProcessor(requestParams)
    for k, v in outputs.items():
        print(k, v)

    monthlyData = resetMonthlyElecData()

    return render_template('results.html', monthlyData = monthlyData, zip = zipCode, \
    costPerKwh = elecCost, sys_cap = sysCap, tilt = tilt, azimuth = azimuth, \
    losses = losses, arrTypeDropdown = selectArrType, modTypeDropdown = selectModType, outputs = outputs)

#sets monthly average electricity production values once pulled from JSON response
def resetMonthlyElecData(kwh = [], month = []):
    kwh = solarDataProcessor.ac_monthly
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthlyData = []
    for i in range (0, 12):
        a_month = dict(month=month[i], kwhPerMonth=kwh[i])
        monthlyData.append(a_month)
    return(monthlyData)
   

