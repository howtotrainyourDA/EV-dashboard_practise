import streamlit as st
from project_files.python.utils import load_sales_data, load_charging_data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("EV Sales")
st.subheader("EV Sales by Region")


sales_df = load_sales_data()
charging_df = load_charging_data()




st.title("Unit Sales by Vehicle Type")

# Add region selector
selected_region = st.selectbox(
    "Select Region",
    options=sorted(sales_df['region'].unique())
)

# Filter data for selected region and group by year and vehicle type
region_sales_by_type = sales_df[sales_df['region'] == selected_region].groupby(['year', 'powertrain'])['value'].sum().reset_index()

# Create a Streamlit figure
fig, ax = plt.subplots(figsize=(12, 6))

# Get unique powertrains and years for the selected region
powertrains = region_sales_by_type['powertrain'].unique()
years = sorted(region_sales_by_type['year'].unique())

# Create arrays for plotting
plot_data = np.zeros((len(powertrains), len(years)))
for i, powertrain in enumerate(powertrains):
    for j, year in enumerate(years):
        mask = (region_sales_by_type['powertrain'] == powertrain) & (region_sales_by_type['year'] == year)
        if mask.any():
            plot_data[i,j] = region_sales_by_type[mask]['value'].iloc[0]

# Create the stacked bar plot
bottom = np.zeros(len(years))
for i, powertrain in enumerate(powertrains):
    plt.bar(years, plot_data[i], bottom=bottom, label=powertrain)
    bottom += plot_data[i]

# Customize the plot
ax.set_title(f'EV Sales by Vehicle Type in {selected_region}', fontsize=14, pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Units Sold', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add thousand separator to y-axis
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

# Move legend to the right of the plot
plt.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("---")


st.subheader("Top Sales by Country")

# Create selectbox for year selection
selected_year_country = st.selectbox(
    "Select Year for Country Analysis",
    options=sorted(sales_df['year'].unique(), reverse=True),
    key='country_year_select'
)

# Filter data for selected year and group by country
country_sales = sales_df[sales_df['year'] == selected_year_country].groupby('region')['value'].sum().reset_index()

# Sort countries by sales value and get top 10
top_countries = country_sales.nlargest(10, 'value')

# Create two columns for pie chart and dataframe
col1, col2 = st.columns([3, 2])

with col1:
    # Create pie chart
    fig_pie, ax_pie = plt.subplots(figsize=(10, 8))
    plt.pie(top_countries['value'], labels=top_countries['region'], autopct='%1.1f%%')
    plt.title(f'Top 10 Countries by EV Sales Share ({selected_year_country})')

    # Add legend
    plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout
    plt.tight_layout()

    # Display the plot
    st.pyplot(fig_pie)

with col2:
    # Format the values with thousand separators
    top_countries['value'] = top_countries['value'].apply(lambda x: f"{int(x):,}")
    
    # Rename columns for display
    top_countries_display = top_countries.rename(columns={
        'region': 'Country',
        'value': 'Sales'
    })
    
    # Display the dataframe
    st.dataframe(top_countries_display, use_container_width=True)



st.markdown("---")

    
st.subheader("Sales Trends by Country")

# Create filters
col1, col2 = st.columns([2,1])

with col1:
    # Multi-select for countries
    countries = sorted(sales_df['region'].unique())
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=countries,
        default=countries[:3]  # Default to first 3 countries
    )

with col2:
    # Filter for powertrain type
    powertrains = sorted(sales_df['powertrain'].unique())
    selected_powertrain = st.selectbox(
        "Select Powertrain Type",
        options=powertrains
    )

# Filter data based on selections
filtered_df = sales_df[
    (sales_df['region'].isin(selected_countries)) &
    (sales_df['powertrain'] == selected_powertrain)
]

# Create line plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot line for each country
for country in selected_countries:
    country_data = filtered_df[filtered_df['region'] == country]
    plt.plot(country_data['year'], country_data['value'], marker='o', label=country)

# Customize the plot
plt.title(f'{selected_powertrain} Sales Trends by Country', fontsize=14, pad=15)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Units Sold', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')

# Format y-axis with thousand separators
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

# Rotate x-axis labels
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()

# Display the plot
st.pyplot(fig)



