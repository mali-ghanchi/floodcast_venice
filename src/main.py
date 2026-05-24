import pandas as pd #used pandas to manage my table
import matplotlib.pyplot as plt 

graph = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
graph.columns = ['year', 'sea_level_mm', 'flag', 'quality'] #providing the headers here

graph = graph[graph['sea_level_mm'] != -99999] #apparently psmsl displays missing values using this specific notation.
# now obviously missing values are not relevant, so I lowkey just exclude them. 

graph['sea_level_cm'] = graph['sea_level_mm'] / 10 #Tbh it's easier to read it this way

# Quick check
print(graph.head())
print(f"Data from {graph['year'].min()} to {graph['year'].max()}")

# Plot it
plt.plot(graph['year'], graph['sea_level_cm'])
plt.title('Venice Sea Level 1909-2000')
plt.xlabel('Year')
plt.ylabel('Sea Level (cm)')
plt.show()