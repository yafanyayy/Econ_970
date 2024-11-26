import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '../CEPII.csv'
data = pd.read_csv(file_path)

# Define the list of allowed values
allowed_countries = ['CHN', 'SGP', 'HKG', 'USA', 'IDN', 'MYS', 'PHL', 'THA', 'VNM', 'BRN', 'MMR', 'KHM', 'LAO']
# Include ASEAN countries

# Filter rows where both 'country_id_o' and 'country_id_d' are in the allowed list
filtered_data = data[(data['country_id_o'].isin(allowed_countries)) & 
                     (data['country_id_d'].isin(allowed_countries)) &
                     (data['country_id_o'] != data['country_id_d'])]

# Filter rows where 'year' is between 1990 and 2019
filtered_data = filtered_data[(filtered_data['year'] >= 1990)]

# Select only the specified columns
selected_columns = ['year', 'country_id_o', 'country_id_d', 'gdp_o', 'gdp_d', 'pop_o', 'pop_d', 'distw_harmonic',
                    'tradeflow_comtrade_o', 'tradeflow_comtrade_d', 'comlang_off', 'contig']

# Filter the data to include only the selected columns
filtered_data = filtered_data[selected_columns]
filtered_data = filtered_data.dropna()

print(filtered_data)
# Save the updated data to a new file, if needed
filtered_data.to_excel('../../derived/visualisation/filtered_for_visualisation.xlsx', index=False)
