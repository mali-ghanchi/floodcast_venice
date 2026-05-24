import pandas as pd #used pandas to manage my table
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression #for machine learning
import numpy as np

graph = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
graph.columns = ['year', 'sea_level_mm', 'flag', 'quality'] #providing the headers here

graph = graph[graph['sea_level_mm'] != -99999] #apparently psmsl displays missing values using this specific notation.
# now obviously missing values are not relevant, so I lowkey just exclude them. 
graph['sea_level_cm'] = graph['sea_level_mm'] / 10
X = graph[['year']]
y = graph [['sea_level_cm']]
model = LinearRegression()
model.fit(X, y)
future_years = np.arange(2000, 2101).reshape(-1, 1)
predicted_levels = model.predict(future_years)

# Quick check
print(graph.head())
print(f"Data from {graph['year'].min()} to {graph['year'].max()}")

# Plot it
plt.plot(graph['year'], graph['sea_level_cm'], label='Historical Data')
plt.plot(future_years, predicted_levels, label='Our Prediction', 
         linestyle='--',
         color='red')
plt.title('Venice Sea Level 1909-2100')
plt.xlabel('Year')
plt.ylabel('Sea Level (cm)')
plt.legend()  # shows the labels we defined above
plt.show()