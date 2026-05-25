import pandas as pd #used pandas to manage my table
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression #for machine learning
import numpy as np

graph = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
graph.columns = ['year', 'sea_level_mm', 'flag', 'quality'] #providing the headers here
graph = graph[graph['sea_level_mm'] != -99999] #apparently psmsl displays missing values using this specific notation.
# now obviously missing values are not relevant, so I lowkey just exclude them. 
graph['sea_level_cm'] = graph['sea_level_mm'] / 10

#Training
X = graph[['year']]
y = graph [['sea_level_cm']]
model = LinearRegression()
model.fit(X, y)
hist_trend = model.predict(X) #just predicting over historical values
future_years = np.arange(2000, 2101).reshape(-1, 1)
predicted_levels = model.predict(future_years) #predicting for future years

#obviously there is always an uncertainty range
uncertainty = np.array([(i - 2000) * 0.05 for i in range(2000, 2101)])
upper_bound = predicted_levels.flatten() + uncertainty
lower_bound = predicted_levels.flatten() - uncertainty

# Quick check
print(graph.head())
print(f"Data from {graph['year'].min()} to {graph['year'].max()}")

# Plot historical raw data
plt.plot(graph['year'], graph['sea_level_cm'], 
         color='steelblue', label='Historical Data', alpha=0.6)

# Plot trend line over historical data
plt.plot(graph['year'], hist_trend, 
         color='orange', linewidth=2, label='Historical Trend')

# Plot future prediction
plt.plot(future_years, predicted_levels, 
         color='red', linestyle='--', linewidth=2, label='Our Prediction')

# Add shaded uncertainty band around prediction
plt.fill_between(future_years.flatten(), lower_bound, upper_bound, 
                 color='red', alpha=0.15, label='Uncertainty Range')

plt.title('Venice Sea Level 1909-2100')
plt.xlabel('Year')
plt.ylabel('Sea Level (cm)')
plt.legend()
plt.show()