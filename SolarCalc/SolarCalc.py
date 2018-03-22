import os, calendar, jinja2
from flask import Flask, request, session, g, redirect, abort, url_for, render_template, flash
from SolarCalc.model import ElectricityInputs, ElectricityOutputs

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SOLARCALC_SETTINGS', silent=True)

ElecOutputs = ElectricityOutputs()

@app.route('/')
def initMonthTable():
    kwh = ElecOutputs.ac_monthly
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthlyData = []
    for i in range (1, 12):
        a_month = dict(month=month[i], kwhPerMonth=kwh[i])
        monthlyData.append(a_month)
    
    arrType = [ "Fixed - Open Rack", "Fixed - Roof Mounted", "1-Axis Tracker", "1-Axis Backtracker", "2-Axis Tracker"]
    modType = ["Standard (14-17%)", "Premium (18-20%)", "Thin Film (~11%)"]
 
    return render_template('mainLayout.html', monthlyData = monthlyData, arrType = arrType, modType = modType)

if __name__ == "__main__":
    app.run()

#ui = InitializeUI()
#ui.initMonthTable()

