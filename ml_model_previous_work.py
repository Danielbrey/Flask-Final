#%%
import pandas as pd
from get_current_data import load_day_data
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import adfuller

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

#Gets current data for all of campus
'''
curr_date = datetime.now().date()


all_data = load_day_data("all")
all_data.columns = ['Datetime', 'Location', 'Power']
split = all_data['Datetime'].str.split('T').apply(pd.Series)
dates = split.iloc[:,0]
times = split.iloc[:,1]
all_data["Time"] = times
all_data["Date"] = dates
all_data.to_csv("curr_data.csv")
print("Done")
'''
all_data = pd.read_csv("curr_data.csv")
'''
all_data['Datetime'] = pd.to_datetime(all_data['Datetime'].replace("T"," "))
all_data = all_data.set_index("Datetime")

all_data = all_data.resample('10T').mean()
print(all_data)


def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

plot_df(all_data, x=all_data.index, y=all_data['Power'], title='Time Series Prediction Data') # All Data
'''

all_data = all_data[all_data["Power"] > 100]

train, test = train_test_split(all_data, test_size=0.25, random_state=42, shuffle=False)
'''
#%%
result = adfuller(train["Power"].dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

# So we can see that it is already stationary
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})
# Original Series
fig, axes = plt.subplots(3, 2, sharex=True)
axes[0, 0].plot(train["Power"]); axes[0, 0].set_title('Original Series')
plot_acf(train["Power"], ax=axes[0, 1])

# PACF plot of 1st differenced series
plt.rcParams.update({'figure.figsize':(9,3), 'figure.dpi':120})

fig, axes = plt.subplots(1, 2, sharex=True)
axes[0].plot(train["Power"]); axes[0].set_title('1st Differencing')
axes[1].set(ylim=(0,5))
plot_pacf(train["Power"].dropna(), ax=axes[1])

plt.show()
# %%
# 1,1,2 ARIMA Model
model = ARIMA(train["Power"], order=(1,0,1))
model_fit = model.fit(disp=0)
print(model_fit.summary())
# %%
# Plot residual errors
residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()

# %%
model_fit.plot_predict(dynamic=False)
plt.show()
'''
# Build Model
# model = ARIMA(train, order=(3,2,1))  
#%%
# Forecast
period = 6 * 24 * 7
sarimax_model = SARIMAX(train['Power'],order=(1, 0, 0),seasonal_order=(1,1,1,period))
sarima = sarimax_model.fit()

fc, se, conf = sarima.forecast(1715, alpha=0.1)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc, index=test.index)
lower_series = pd.Series(conf[:, 0], index=test.index)
upper_series = pd.Series(conf[:, 1], index=test.index)

# Plot
plt.figure(figsize=(12,5), dpi=100)
plt.plot(train["Power"], label='training')
plt.plot(test["Power"], label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series, 
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()
# %%
# Plot
fig, axes = plt.subplots(2, 1, figsize=(10,5), dpi=100, sharex=True)
'''
# Usual Differencing
axes[0].plot(train["Power"], label='Original Series')
axes[0].plot(train["Power"].diff(1), label='Usual Differencing')
axes[0].set_title('Usual Differencing')
axes[0].legend(loc='upper left', fontsize=10)


# Seasinal Dei
axes[1].plot(train["Power"], label='Original Series')
axes[1].plot(train["Power"].diff(7), label='Seasonal Differencing', color='green')
axes[1].set_title('Seasonal Differencing')
plt.legend(loc='upper left', fontsize=12)
plt.suptitle('a10 - Drug Sales', fontsize=16)
plt.show()

# %%

import pmdarima as pm
period = 6 * 24 * 7
# Seasonal - fit stepwise auto-ARIMA
smodel = pm.auto_arima(train["Power"], start_p=1, start_q=1,
                         test='adf',
                         max_p=2, max_q=2, m=period,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)

smodel.summary()


#%%
import pmdarima as pm
import statsmodels.api as sm
period = 6 * 24 * 7
model=sm.tsa.statespace.SARIMAX(train['Power'],order=(1, 0, 0),seasonal_order=(1,1,1,period))
results=model.fit()

test["Predicted Power"] = results.predict(start=90,end=103,dynamic=True)

# %%
# ARIMA(1,0,0)(1,1,1)[7]

fitted, confint = smodel.predict(n_periods=period, return_conf_int=True)
index_of_fc = pd.date_range(test["Datetime"][-1], periods = period, freq='10T')

# make series for plotting purpose
fitted_series = pd.Series(fitted, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.plot(train["Power"])
plt.plot(fitted_series, color='darkgreen')
plt.fill_between(lower_series.index, 
                 lower_series, 
                 upper_series, 
                 color='k', alpha=.15)

plt.title("SARIMA - Final Forecast of a10 - Drug Sales")
plt.show()

'''