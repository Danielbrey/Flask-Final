import pandas as pd
from flask import render_template

#from shared import get_energy_dataframe, pie_chart
from get_current_data import get_metrics_data


def app():
  #print('test')
  total_energy = pd.read_csv('bihall_past.csv')
  return render_template('average_demand.html', title = 'Bihall', data = total_energy, times = total_energy["Date"], values = total_energy["power"])


#CAN DELETE (plus the csv)