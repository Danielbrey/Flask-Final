from flask import Flask, render_template

from multipage import MultiPage
from pages import average_demand, bihall, curr_data, bihall_curr_data


app = Flask(__name__)

@app.route('/')
def base():
   return render_template('homepage.html', title="Welcome to Green Midd")

@app.route('/home')
def home():
   return render_template('homepage.html', title="Welcome to Green Midd")

@app.route('/average_demand')
def avg_demand():
   return average_demand.app()

@app.route('/bihall')
def bi_hall():
   return bihall.app()

@app.route('/current_data')
def currentData():
   return curr_data.app()

@app.route('/bihall_current_data')
def current_Bihall_Data():
   return bihall_curr_data.app()








if __name__ == '__main__':
   app.run()
