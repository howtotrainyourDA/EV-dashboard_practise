import streamlit as st
from project_files.python.utils import load_sales_data, load_charging_data

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


sales_df = load_sales_data()
charging_df = load_charging_data()

st.title("Global EV Data Explorer")


st.subheader("Explore and download the full data behind the Global EV Outlook")

# 4. Text
st.markdown("""
    The Global EV Outlook is an annual publication that identifies and discusses recent developments 
    in electric mobility across the globe. It is developed with the support of the members of the 
    Electric Vehicles Initiative (EVI).

    Combining historical analysis with projections to 2030, the report examines key areas of interest such as:
    - Electric vehicle deployment
    - Charging infrastructure deployment  
    - Energy use
    - CO2 emissions
    - Battery demand
    - Related policy developments

    The report includes policy recommendations that incorporate lessons learned from leading markets
    to inform policy makers and stakeholders with regard to policy frameworks and market systems
    for electric vehicle adoption.
""")


st.markdown("---")

# Calculate yearly totals
yearly_sales = sales_df.groupby('year')['value'].sum().reset_index()
yearly_charging = charging_df.groupby('year')['value'].sum().reset_index()

# Create selectbox for year selection
selected_year = st.selectbox(
    "Select Year",
    options=sorted(yearly_sales['year'].unique(), reverse=True)
)

# Calculate metrics for both sales and charging points
col1, col2 = st.columns(2)

with col1:
    st.subheader("EV Sales")
    current_year_sales = yearly_sales[yearly_sales['year'] == selected_year]['value'].iloc[0]
    if selected_year - 1 in yearly_sales['year'].values:
        previous_year_sales = yearly_sales[yearly_sales['year'] == (selected_year - 1)]['value'].iloc[0]
        sales_delta = current_year_sales - previous_year_sales
        sales_delta_percent = (sales_delta / previous_year_sales) * 100
        st.metric(
            label=f"Global EV Sales in {selected_year}",
            value=f"{int(current_year_sales):,}",
            delta=f"{sales_delta_percent:.1f}%"
        )
    else:
        st.metric(
            label=f"Global EV Sales in {selected_year}",
            value=f"{int(current_year_sales):,}"
        )

with col2:
    st.subheader("Charging Points")
    if selected_year in yearly_charging['year'].values:
        current_year_charging = yearly_charging[yearly_charging['year'] == selected_year]['value'].iloc[0]
        if selected_year - 1 in yearly_charging['year'].values:
            previous_year_charging = yearly_charging[yearly_charging['year'] == (selected_year - 1)]['value'].iloc[0]
            charging_delta = current_year_charging - previous_year_charging
            charging_delta_percent = (charging_delta / previous_year_charging) * 100
            st.metric(
                label=f"Global Charging Points in {selected_year}",
                value=f"{int(current_year_charging):,}",
                delta=f"{charging_delta_percent:.1f}%"
            )
        else:
            st.metric(
                label=f"Global Charging Points in {selected_year}",
                value=f"{int(current_year_charging):,}"
            )
    else:
        st.metric(
            label=f"Global Charging Points in {selected_year}",
            value="No data available"
        )

st.markdown("---")


st.title("Unit Sales by Vehicle Type")

# Group the data by year and vehicle type
yearly_sales_by_type = sales_df.groupby(['year', 'powertrain'])['value'].sum().reset_index()

# Create a Streamlit figure
fig, ax = plt.subplots(figsize=(12, 6))

# Get unique powertrains and years
powertrains = yearly_sales_by_type['powertrain'].unique()
years = yearly_sales_by_type['year'].unique()

# Create the stacked bar plot
bottom = np.zeros(len(years))
for powertrain in powertrains:
    mask = yearly_sales_by_type['powertrain'] == powertrain
    values = yearly_sales_by_type[mask]['value'].values
    plt.bar(years, values, bottom=bottom, label=powertrain)
    bottom += values

# Customize the plot
ax.set_title('Global EV Sales by Vehicle Type', fontsize=14, pad=15)
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
