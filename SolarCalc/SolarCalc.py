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
    return render_template('mainLayout.html', monthlyData = monthlyData)

if __name__ == "__main__":
    app.run()