
import os
import pandas as pd
import matplotlib.pyplot as plt
file_path = 'filtered_for_visualisation.xlsx'
filtered_data= pd.read_excel(file_path)

# Define the country groupings
asean_countries = ['SGP', 'IDN', 'MYS', 'PHL', 'THA', 'VNM', 'BRN', 'MMR', 'KHM', 'LAO']
china_related = ['CHN', 'HKG']
us_related = ['USA']

# Create output directory if it doesn't exist
output_dir = '../../output/visualisation'
# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

for country in asean_countries:
    # Filter data for exports (origin country is the ASEAN country)
    export_data = filtered_data[filtered_data['country_id_o'] == country]
    
    # Group by year and destination country, summing trade flows
    export_grouped = export_data.groupby(['year', 'country_id_d'])['tradeflow_comtrade_o'].sum().unstack(fill_value=0)

    # Separate trade flows to China, HK, and the USA
    export_to_china = export_grouped['CHN'] if 'CHN' in export_grouped else 0
    export_to_hk = export_grouped['HKG'] if 'HKG' in export_grouped else 0
    export_to_usa = export_grouped['USA'] if 'USA' in export_grouped else 0

    # Combine trade flows to China and HK
    export_to_china_hk = export_to_china + export_to_hk

    # Create the bar plot
    plt.figure(figsize=(12, 7))
    plt.bar(export_grouped.index, export_to_china_hk, label='Exports to China/HK', color='blue')
    plt.bar(export_grouped.index, export_to_usa, bottom=export_to_china_hk, label='Exports to USA', color='orange')
    
    # Add titles and labels
    plt.title(f'Exports from {country} (1990-2019)')
    plt.xlabel('Year')
    plt.ylabel('Trade Value (Sum of Exports)')
    plt.legend()

    # Save the plot to the output directory
    export_filepath = os.path.join(output_dir, f'{country}_exports.png')
    plt.tight_layout()
    plt.savefig(export_filepath)
    plt.close()

    print(f"Export graph for {country} saved at: {export_filepath}")

