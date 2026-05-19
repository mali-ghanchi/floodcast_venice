import pandas as pd
import matplotlib.pyplot as plt

# Load historical tide gauge data
df = pd.read_csv('../data/venice_data.txt', sep=';', header=None)
df.columns = ['year', 'sea_level_mm', 'flag', 'quality']

# Clean missing values
df = df[df['sea_level_mm'] != -99999]

# Convert mm to cm
df['sea_level_cm'] = df['sea_level_mm'] / 10

# Quick check
print(df.head())
print(f"Data from {df['year'].min()} to {df['year'].max()}")

# Plot it
plt.plot(df['year'], df['sea_level_cm'])
plt.title('Venice Sea Level 1909-2000')
plt.xlabel('Year')
plt.ylabel('Sea Level (cm)')
plt.show()