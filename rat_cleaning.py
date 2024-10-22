import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


df = pd.read_csv("Rat_Sightings_20240917.csv")
# print(df.columns)

# Keep only the necessary columns
df = df[['Created Date', 'Location Type', 'Incident Zip', 'Community Board', 'Borough', 'Latitude', 'Longitude']]
# print(df.columns)
# print(df.head())
# print(df.size) ----------------------------------------- 1772883

unique_location_types = df['Location Type'].unique()
# print(unique_location_types)

# Define mapping for residential categories
residential_mapping = {
    'Single Room Occupancy (SRO)': 'Single',
    '1-2 Family Dwelling': '1-2 Family Apartment',
    '1-2 FamilyDwelling': '1-2 Family Apartment',
    '3+ Family Apt. Building': '3+ Family',
    '3+ Family Apartment Building': '3+ Family',
    '3+ Family Apt.': '3+ Family',
    '3+Family Apt.': '3+ Family',
    '3+ Family Apt': '3+ Family',
    '1-3 Family Dwelling': '1-3 Family Dwelling',
    '1-3 Family Mixed Use Building': '1-3 Family Mixed',
    '1-2 Family Mixed Use Building': '1-2 Family Mixed',
    '3+ Family Mixed Use Building': '3+ Family Mixed',
    'Private House': 'Private House',
    'Apartment': 'Apartment',
    'Residential Property': 'Residential Property'
}

# Apply mapping to the 'Location Type' column for residential data
df['Location Type'] = df['Location Type'].replace(residential_mapping)

# Create the residential and non-residential DataFrames
residential_df = df[df['Location Type'].isin(residential_mapping.values())]
nonresidential_df = df[~df['Location Type'].isin(residential_mapping.values())]
nonresidential_df = nonresidential_df[~nonresidential_df['Location Type'].isin(['Other', 'Other (Explain Below)'])]

# print("Unique entries in residential_df (Location Type):")
# print(residential_df['Location Type'].unique())
# print(residential_df.shape)

# print("\nUnique entries in nonresidential_df (Location Type):")
# print(nonresidential_df['Location Type'].unique())
# print(nonresidential_df.shape)


# Basic Data Exploration - residential vs nonresidential pie chart
residential_count = residential_df.shape[0]
nonresidential_count = nonresidential_df.shape[0]

# Data for the pie chart
labels = ['Residential', 'Non-Residential']
sizes = [residential_count, nonresidential_count]
colors = ['blue', 'purple']

# Pie chart 
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Rat Sightings Proportion: Residential vs Non-Residential Areas')
# Equal aspect ratio ensures that pie chart is drawn as a circle.
plt.axis('equal')
plt.show()

# Convert 'Created Date' to datetime format
df['Created Date'] = pd.to_datetime(df['Created Date'])

# Extract month, week, and day information
df['Month'] = df['Created Date'].dt.month
df['Week'] = df['Created Date'].dt.isocalendar().week
df['Day'] = df['Created Date'].dt.day

# Check the updated dataframe
print(df[['Created Date', 'Month', 'Week', 'Day']].head())

# Check the updated dataframe
print(df[['Created Date', 'Month', 'Week', 'Day']].head())


# Count rat sightings per month
rat_sightings_by_month = df['Month'].value_counts().sort_index()

# Plot the results
plt.figure(figsize=(10, 6))
rat_sightings_by_month.plot(kind='bar')
plt.title('Count of Rat Sightings per Month')
plt.xlabel('Month')
plt.ylabel('Number of Sightings')
plt.xticks(rotation=0)
plt.show()

winter_months = [12, 1, 2]
summer_months = [6, 7, 8]

# Get sightings for winter and summer
winter_sightings = df[df['Month'].isin(winter_months)]['Month'].count()
summer_sightings = df[df['Month'].isin(summer_months)]['Month'].count()

# Filter the data for winter and summer months
winter_data = df[df['Month'].isin([12, 1, 2])]
summer_data = df[df['Month'].isin([6, 7, 8])]

# Check the length of data for both groups
print("Winter sightings count:", len(winter_data))
print("Summer sightings count:", len(summer_data))

# Check for NaN values in these groups
print("NaN in winter data:", winter_data.isna().sum())
print("NaN in summer data:", summer_data.isna().sum())

# Drop rows with missing values in 'Incident Zip', 'Latitude', or 'Longitude'
winter_data_clean = winter_data.dropna(subset=['Incident Zip', 'Latitude', 'Longitude'])
summer_data_clean = summer_data.dropna(subset=['Incident Zip', 'Latitude', 'Longitude'])

# Check cleaned data
print("Cleaned winter data count:", len(winter_data_clean))
print("Cleaned summer data count:", len(summer_data_clean))


# Count the number of sightings per day in both seasons
winter_sightings_per_day = winter_data_clean['Created Date'].dt.date.value_counts()
summer_sightings_per_day = summer_data_clean['Created Date'].dt.date.value_counts()

# Perform the t-test comparing the number of sightings per day in winter vs summer
t_stat, p_value = stats.ttest_ind(winter_sightings_per_day, summer_sightings_per_day, equal_var=False)

print(f'T-statistic: {t_stat}, P-value: {p_value}')



#########################################################################
# Borough and Community Board

import pandas as pd
import scipy.stats as stats


unique_zip_codes = df['Incident Zip'].unique()
unique_community_boards = df['Community Board'].unique()

# print("Unique Zip Codes:")
# print(unique_zip_codes)

# print("\nUnique Community Boards:")
# print(unique_community_boards)

# Count of rat sightings by Zip Code and Community Board
zip_code_counts = df['Incident Zip'].value_counts()
community_board_counts = df['Community Board'].value_counts()

# Plot: Number of rat sightings per zip code
plt.figure(figsize=(10, 6))

zip_code_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Rat Sightings per Zip Code')
plt.xlabel('Zip Code')
plt.ylabel('Number of Rat Sightings')
plt.xticks(rotation=90)
plt.show()


# Group by Borough and Community Board and count the number of sightings
borough_community_group = df.groupby(['Borough', 'Community Board']).size().unstack(fill_value=0)

# Plot the stacked bar chart
borough_community_group.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')

plt.title('Number of Rat Sightings per Borough, Stacked by Community Board')
plt.xlabel('Borough')
plt.ylabel('Number of Rat Sightings')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Community Board', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

df = pd.read_csv("Rat_Sightings_20240917.csv")

# Create a contingency table for Borough and Rat Sightings (count by borough)
contingency_table = pd.crosstab(df['Borough'], df['Community Board'])  # Adjust column names as necessary

# Perform Chi-Square Test of Independence
chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2_stat:.4f}")
print(f"P-Value: {p_val:.4f}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected Frequencies: \n{pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)}")

alpha = 0.05  

if p_val < alpha:
    print("Reject the Null Hypothesis (H₀): The number of rat sightings depends on the borough.")
else:
    print("Fail to Reject the Null Hypothesis (H₀): The number of rat sightings is independent of the borough.")