import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs

df = pd.read_csv('launch_data.csv')

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Extract year from the 'date' column
df['year'] = df['date'].dt.year


st.title('Rocket Launch Data Exploration')
st.markdown('---')  

st.text('My analysis and explanation for each of these visuals can be found on my blog post:') 
st.markdown('[](https://boi-andy.github.io/my-blog/2023/11/14/EDA.html)')

st.text('To find the data I used for this application, visit my Github repository:') 
st.markdown('[](https://github.com/boi-andy/final_project)')

# Plot 1: Line graph of launches per year by provider
st.header('Launches by Provider')

# Sidebar to select service provider
selected_lsp = st.selectbox('Select Service Provider', df['lsp_name'].unique())

# Filter the DataFrame based on the selected service provider
filtered_df = df[df['lsp_name'] == selected_lsp]

# Group data by year for the selected service provider
launches_per_year_lsp = filtered_df.groupby('year').size()

# Plotting
plt.figure(figsize=(12, 8))

bar_width = 0.35
index = np.arange(len(launches_per_year_lsp))

plt.bar(index, launches_per_year_lsp, width=bar_width, label=selected_lsp)

plt.xlabel('Year')
plt.ylabel('Number of Launches')
plt.title(f'Number of Launches per Year for {selected_lsp}')
plt.xticks(index, launches_per_year_lsp.index)
plt.legend()

plt.tight_layout()

# Display the plot in Streamlit app
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

# Calculate the sum of launches for all years
total_launches = launches_per_year_lsp.sum()

# Display the most popular launch location
st.write(f"{selected_lsp} Total Launches: **{total_launches}**")

# Calculate the most popular launch location for the selected service provider
most_popular_location = filtered_df['location'].mode().values[0]

# Plot 2: Bar graph of launch types per year by provider
st.header(f'Launch Types for {selected_lsp}')

# Group by year and mission_type, counting the number of missions per year for each mission_type
missions_per_year_type = filtered_df.groupby(['year', 'mission_type']).size().unstack(fill_value=0)

# Plotting the count of missions per year for each mission type
plt.figure(figsize=(12, 8))

for mission_type in missions_per_year_type.columns:
    plt.plot(missions_per_year_type.index, missions_per_year_type[mission_type], label=mission_type)

plt.xlabel('Year')
plt.ylabel('Number of Missions')
plt.title(f'Mission Types Over Years for {selected_lsp}')
plt.legend(title='Mission Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Display the plot in Streamlit app
st.pyplot()

# Calculate the most popular launch location for the selected service provider
most_popular_type = filtered_df['mission_type'].mode().values[0]

# Display the most popular type location
st.write(f"The most popular type location for {selected_lsp} is: **{most_popular_type}**")

# Display the most popular launch location
st.write(f"Most popular launch location for {selected_lsp} is: **{most_popular_location}**")

# Plot 3: Line graph of launches per year by provider
st.header('Launches Count by Location')

# Sidebar to select location
selected_location = st.selectbox('Select Location', df['location'].unique())

# Filter the DataFrame based on the selected location
filtered_df = df[df['location'] == selected_location]

# Group data by year for the selected location
location_counts = filtered_df.groupby('year').size()

# Plotting
plt.figure(figsize=(12, 8))

# Plot a line chart with years on the x-axis and number of launches on the y-axis
plt.plot(location_counts.index, location_counts.values, marker='o', linestyle='-', label='Launches')

plt.xlabel('Year')
plt.ylabel('Number of Launches')
plt.title(f'Number of Launches per Year for {selected_location}')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()

plt.tight_layout()

# Display the plot in Streamlit app
st.pyplot(plt)

# Calculate the sum of launches for all years
total_launches_location = location_counts.sum()

# Display the most popular launch location
st.write(f"{selected_location} Total Launches: **{total_launches_location}**")

# Get latitude and longitude bounds for the selected location
min_lat, max_lat = filtered_df['Latitude'].min(), filtered_df['Latitude'].max()
min_lon, max_lon = filtered_df['Longitude'].min(), filtered_df['Longitude'].max()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Show a world map background
ax.stock_img()

# Plotting launch pads for the selected location
ax.scatter(filtered_df['Longitude'], filtered_df['Latitude'], color='red', marker='o', transform=ccrs.PlateCarree())

# Customize plot settings
ax.coastlines()
ax.set_title(f'Launch Pads of {selected_location}')

# Display the plot in Streamlit app
st.pyplot(fig)

# Count the distinct launch pads for the selected location
distinct_pads = filtered_df['pad_name'].nunique()

st.write(f"{selected_location} Distinct Launch Pads: **{distinct_pads}**")