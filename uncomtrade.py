import pandas
import requests
import comtradeapicall

# Your subscription key
subscription_key = "98cf81630d4448ef840bcdff3c2950ad"

#set some variables
from datetime import date
from datetime import timedelta
today = date.today()
yesterday = today - timedelta(days=1)
lastweek = today - timedelta(days=7)


# ASEAN countries' M49 codes
asean_countries = {
    "Brunei": "96",
    "Cambodia": "116",
    "Indonesia": "360",
    "Laos": "418",
    "Malaysia": "458",
    "Myanmar": "104",
    "Philippines": "608",
    "Singapore": "702",
    "Thailand": "764",
    "Vietnam": "704"
}

# Partners: US and China M49 codes
partners = {
    "United States": "842",
    "China": "156"
}

# Initialize a list to collect the results
data_frames = []

# Iterate over ASEAN countries, partners, and years
for country_name, country_code in asean_countries.items():
    for partner_name, partner_code in partners.items():
        for year in range(1990, 2020):
            # Fetch data for the current combination
            try:
                df = comtradeapicall.previewFinalData(
                    typeCode='C',
                    freqCode='A',
                    clCode='HS',
                    period=str(year),
                    reporterCode=country_code,
                    partnerCode=partner_code,
                    partner2Code=None,
                    flowCode=None,  # Can be 'X' for exports or 'M' for imports
                    cmdCode=None,
                    customsCode=None,
                    motCode=None,
                    maxRecords=50000,
                    format_output='JSON',
                    breakdownMode='classic',
                    includeDesc=True
                )
                # Add the results to the list
                if df is not None:
                    df["Reporter"] = country_name
                    df["Partner"] = partner_name
                    df["Year"] = year
                    data_frames.append(df)
            except Exception as e:
                print(f"Failed for {country_name} -> {partner_name} in {year}: {e}")

# Combine all the data into a single DataFrame
final_df = pd.concat(data_frames, ignore_index=True)

# Save the data to a CSV file
final_df.to_csv("raw_data/asean_trade_with_us_and_china_1990_2019.csv", index=False)

print("Data retrieval complete! Saved to asean_trade_with_us_and_china_1990_2019.csv")
