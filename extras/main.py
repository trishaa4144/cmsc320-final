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

# Get unique values in 'Location Type'
unique_location_types = df['Location Type'].unique()
print(unique_location_types)

# Filter out rows with 'Location Type' that are not related to households/family
household_types = ['1-2 Family Dwelling', '3+ Family Apt. Building', '3+ Family Mixed Use Building', 'Mixed Use Building', '1-2 Family Mixed Use Building', '3+ Family Apartment Building', '1-3 Family Dwelling', 'Apartment', 'Residential Property', 'Private House', '1-3 Family Mixed Use Building', '3+ Family Apt.' '1-2 FamilyDwelling', '3+Family Apt.', '3+ Family Apt' ]
df = df[df['Location Type'].isin(household_types)]
# print(df.head())
# print(df.size) # 1073513

# Count rat sightings per zip code
rat_sightings_by_zip = df['Incident Zip'].value_counts()

# Plot the results
plt.figure(figsize=(10, 6))
rat_sightings_by_zip.plot(kind='bar')
plt.title('Count of Rat Sightings per Zip Code')
plt.xlabel('Zip Code')
plt.ylabel('Number of Sightings')
plt.xticks(rotation=45)
plt.show()


# Convert 'Created Date' to datetime format
df['Created Date'] = pd.to_datetime(df['Created Date'])

# Extract month, week, and day information
df['Month'] = df['Created Date'].dt.month
df['Week'] = df['Created Date'].dt.isocalendar().week
df['Day'] = df['Created Date'].dt.day

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

# Example: Compare rat sightings between Winter (Dec-Feb) and Summer (Jun-Aug)
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



