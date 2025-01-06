import streamlit as st
from project_files.python.utils import load_charging_data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Charging Points")
st.subheader("Charging Infrastructure by Region")

charging_df = load_charging_data()

# Add region selector
selected_region = st.selectbox(
    "Select Region",
    options=sorted(charging_df['region'].unique())
)

# Filter data for selected region
region_charging = charging_df[charging_df['region'] == selected_region]

# Create a Streamlit figure
fig, ax = plt.subplots(figsize=(12, 6))

# Create the bar plot
sns.barplot(data=region_charging, x='year', y='value', ax=ax)

# Customize the plot
ax.set_title(f'Charging Points Evolution in {selected_region}', fontsize=14, pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Charging Points', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add thousand separator to y-axis
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("---")

st.subheader("Top Countries by Charging Infrastructure")

# Create selectbox for year selection
selected_year = st.selectbox(
    "Select Year for Country Analysis",
    options=sorted(charging_df['year'].unique(), reverse=True),
    key='country_year_select'
)

# Filter data for selected year and group by country
country_charging = charging_df[charging_df['year'] == selected_year].groupby('region')['value'].sum().reset_index()

# Sort countries by charging points and get top 10
top_countries = country_charging.nlargest(10, 'value')

# Create two columns for pie chart and dataframe
col1, col2 = st.columns([3, 2])

with col1:
    # Create pie chart
    fig_pie, ax_pie = plt.subplots(figsize=(10, 8))
    plt.pie(top_countries['value'], labels=top_countries['region'], autopct='%1.1f%%')
    plt.title(f'Top 10 Countries by Charging Infrastructure Share ({selected_year})')

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
        'value': 'Charging Points'
    })
    
    # Display the dataframe
    st.dataframe(top_countries_display, use_container_width=True)

st.markdown("---")

st.subheader("Charging Infrastructure Trends by Country")

# Create filters
col1, col2 = st.columns([1,1])

with col1:
    # Multi-select for countries
    countries = sorted(charging_df['region'].unique())
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=countries,
        default=countries[:3]  # Default to first 3 countries
    )

# Filter data based on selections
filtered_df = charging_df[charging_df['region'].isin(selected_countries)]

# Create line plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot line for each country
for country in selected_countries:
    country_data = filtered_df[filtered_df['region'] == country]
    plt.plot(country_data['year'], country_data['value'], marker='o', label=country)

# Customize the plot
plt.title('Charging Infrastructure Development by Country', fontsize=14, pad=15)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Charging Points', fontsize=12)
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
