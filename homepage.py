from flask import Flask, render_template
from get_current_data import get_todays_data, get_url, get_week_data
#from multipage import MultiPage
from pages import average_demand_past, bihall_past, curr_data, week_data #, bihall_curr_data, day_average_demand, real_time, bihall # import your pages here
import pandas as pd
from datetime import datetime, timedelta
import requests
import io

total_energy = get_todays_data('all')

curr_time = datetime.now()
#yesterday = curr_time - timedelta(days = 1)
url = get_url(curr_time.day, curr_time.month, curr_time.year, 'all')
data = requests.get(url).content
ML_energy= pd.read_csv(io.StringIO(data.decode('utf-8')), skiprows=1)
#print(ML_energy)
#ML_energy = get_todays_data('all')
#print(total_energy)
total_energy.columns = ['datetime', 'location', 'power']

datetimes_as_strings = total_energy['datetime']

#datetimes_replace = datetimes_as_strings.str.replace('T', '-')
datetimes_split = datetimes_as_strings.str.split('T')
datetimes_apply = datetimes_split.apply(pd.Series)
#datetimes_day = datetimes_apply.iloc[:,2]
#datetimes_month = datetimes_apply.iloc[:,1]
#datetimes_year = datetimes_apply.iloc[:,0]
datetimes_time = datetimes_apply.iloc[:,1]
total_energy["Time"] = datetimes_time 

#print('tot')
#print(total_energy)
#print('ml')
#print(ML_energy)
#print(total_energy)

#NOW FOR WEEK BELOW

#print(total_energy)
#print(total_energy_week)


#datetimes_as_strings = total_energy_week['datetime']

#datetimes_replace = datetimes_as_strings.str.replace('T', '-')
#KEEP NEXT TWO
#datetimes_split = datetimes_as_strings.str.split('T')
#datetimes_apply = datetimes_split.apply(pd.Series)
#datetimes_day = datetimes_apply.iloc[:,2]
#datetimes_month = datetimes_apply.iloc[:,1]
#datetimes_year = datetimes_apply.iloc[:,0]
#KEEP NEXT TWO
#datetimes_time = datetimes_apply.iloc[:,1]
#total_energy_week["Time"] = datetimes_time 
#print(total_energy)
#print(total_energy_week[total_energy_week['location'] == 'campus'])
#print('type')
#print(type(total_energy_week['datetime']))
total_energy_week = get_week_data('all')
total_energy_week.columns = ['datetime', 'location', 'power']
total_energy_week["datetime"] = pd.to_datetime(total_energy_week["datetime"])



#also need data from past week...

buildingDict = {
   "bihall": "mbh",
   "davis": "lib",
   "proctor": "prt",
   "campus": "campus",
   "axinn": "axn",
   "atwater dining": "atd",
   "porter": "ptr",
   #"och": "och",
   "75 shannon street": "75s",
   #"sqa": "sqa",
   #"mnf": "mnf",
   #"mkr": "mkr",
   #"emw": "emw",
   #"cen": "cen",
   "virtue field house": "vfh",
   #"mfh": "mfh",
   "natatorium": "nat",
   "kenyon": "kyn",
   "laforce and ross dining": "laf",
   #"97s": "97s",
   #"brk": "brk",
   #"bro": "bro",
   #"plm" : "plm",
   #"pst": "pst",
   "ridgeline": "rvs",
   #"pth": "pth",
   "mahaney arts center": "cfa",
   #sth": "sth",
   #"hdy": "hdy",
   #"mcc": "mcc",
   #"pkn": "pkn",
   #"stewart": "stw",
   "porter": "prt",
   #"hpb": "hpb",
   #"kcc": "kcc",
   #"coffrin": "cff",
   "atwater a": "ata",
   "atwater b": "atb",
   "voter": "vtr",
   #"sdl": "sdl",
   #"pearsons": "prs",
   "munroe": "mnr",
   #"hld": "hld",
   #"freedman international center": "fic",
   #"gifford": "gfd",
   #"frt": "frt",
   #"crh": "crh",
   #"johnson": "jhn",
   #"chateau": "cht",
   "battell": "btl",
   #"allen": "aln",
   "townhouse south": "ths",
   "townhouse north": "thn",
   "townhouse center": "thc",

}


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('homepage.html', title="Welcome to Green Midd")

@app.route('/average_demand')
def avg_demand():
   return average_demand_past.app()

@app.route('/bihall')
def bi_hall():
   return bihall_past.app()

# @app.route('/current_data')
# def currentData():
#    campus_energy = total_energy[total_energy['location'] == 'campus']
#    return curr_data.app(campus_energy, 'Campus')

@app.route('/<building>_current_data')
def current_building_data(building):
   #building = request.form['lid']
   building_space = building.replace('_', ' ')
   building_transfer = buildingDict[building_space]
   building_energy = total_energy[total_energy['location'] == building_transfer]
   return curr_data.app(building_energy, ML_energy.copy(), building_space)


@app.route('/<building>_week_data')
def current_building_data2(building):
   #building = request.form['lid']
   building_space = building.replace('_', ' ')
   building_transfer = buildingDict[building_space]
   building_energy = total_energy_week[total_energy_week['location'] == building_transfer]
   return week_data.app(building_energy, building_space)









if __name__ == '__main__':
   app.run()
