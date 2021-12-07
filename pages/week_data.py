import pandas as pd
from flask import render_template

def app(total_energy, location):
    return render_template('week_demand.html', title = 'Current Data for ' + location.title(), data = total_energy, times = total_energy["datetime"], values = total_energy["power"])