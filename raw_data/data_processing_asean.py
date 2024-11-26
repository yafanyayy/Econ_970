import pandas as pd

# Load the data
file_path = 'raw_data/CEPII.csv'
data = pd.read_csv(file_path)

# Define the list of allowed values
allowed_countries = ['CHN', 'SGP', 'HKG', 'USA', 'IDN', 'MYS', 'PHL', 'THA', 'VNM', 'BRN', 'MMR', 'KHM', 'LAO']
# Include ASEAN countries

# Filter rows where both 'country_id_o' and 'country_id_d' are in the allowed list
filtered_data = data[(data['country_id_o'].isin(allowed_countries)) & 
                     (data['country_id_d'].isin(allowed_countries)) &
                     (data['country_id_o'] != data['country_id_d'])]

# Filter rows where 'year' is between 1990 and 2019
filtered_data = filtered_data[(filtered_data['year'] >= 1990) & (filtered_data['year'] <= 2019)]

# Select only the specified columns
selected_columns = ['year', 'country_id_o', 'country_id_d', 'gdp_o', 'gdp_d', 'pop_o', 'pop_d', 'distw_harmonic',
                    'tradeflow_comtrade_o', 'tradeflow_comtrade_d', 'comlang_off', 'contig']

# Filter the data to include only the selected columns
filtered_data = filtered_data[selected_columns]

# Save the filtered data to a new Excel file
filtered_data.to_excel('derived/CEPII_filtered.xlsx', index=False)
print("Filtered data saved to 'CEPII_filtered.xlsx'")

# Define the country groupings
asean_related = ['SGP', 'IDN', 'MYS', 'PHL', 'THA', 'VNM', 'BRN', 'MMR', 'KHM', 'LAO']
china_related = ['CHN', 'HKG']
us_related = ['USA']

# Create the binary variables based on the conditions outlined

# FTA1_ijt: Takes a value of 1 when country_id_o is in ASEAN and country_id_d is USA, or vice versa, after 2006
filtered_data['FTA1_ijt'] = ((filtered_data['country_id_o'].isin(asean_related) & filtered_data['country_id_d'].isin(us_related)) |
                             (filtered_data['country_id_o'].isin(us_related) & filtered_data['country_id_d'].isin(asean_related))) & \
                            (filtered_data['year'] > 2006)
filtered_data['FTA1_ijt'] = filtered_data['FTA1_ijt'].astype(int)  # Convert boolean to integer (0 or 1)

# FTA2_ict: Takes a value of 1 if country_id_o is in ASEAN or USA, and country_id_d is China or Hong Kong, after 2006
filtered_data['FTA2_ict'] = ((filtered_data['country_id_o'].isin(asean_related + us_related)) & 
                             (filtered_data['country_id_d'].isin(china_related))) & \
                            (filtered_data['year'] > 2006)
filtered_data['FTA2_ict'] = filtered_data['FTA2_ict'].astype(int)  # Convert boolean to integer (0 or 1)

# FTA3_cjt: Takes a value of 1 if country_id_o is China or Hong Kong, and country_id_d is in ASEAN or USA, after 2006
filtered_data['FTA3_cjt'] = ((filtered_data['country_id_o'].isin(china_related)) & 
                             (filtered_data['country_id_d'].isin(asean_related + us_related))) & \
                            (filtered_data['year'] > 2006)
filtered_data['FTA3_cjt'] = filtered_data['FTA3_cjt'].astype(int)  # Convert boolean to integer (0 or 1)

# Display the first few rows to verify the new columns
print(filtered_data[['country_id_o', 'country_id_d', 'year', 'FTA1_ijt', 'FTA2_ict', 'FTA3_cjt']].head())

# Save the updated data to a new file, if needed
filtered_data.to_excel('derived/filtered_with_FTA_columns_asean.xlsx', index=False)
print("Filtered data with new FTA columns saved to 'filtered_with_FTA_columns_asean.xlsx'")
