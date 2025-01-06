import pandas as pd

def load_sales_data():
    sales_url = "https://api.iea.org/evs?parameters=EV%20sales&category=Historical&mode=Cars&csv=true"
    sales_df = pd.read_csv(sales_url)
    cleaned_sales_df = sales_df[sales_df["parameter"] == "EV sales"]
    cleaned_sales_df.drop(['mode', 'parameter', 'category', "unit"], axis=1, inplace=True)
    return cleaned_sales_df

    #alt: cols_to_keep = ['region', 'year', 'value']
    #cleaned_sales_df = cleaned_sales_df[cols_to_keep]


def load_charging_data():
    charging_url = "https://api.iea.org/evs?parameters=EV%20charging%20points&category=Historical&mode=EV&csv=true"
    charging_df = pd.read_csv(charging_url)
    # Sum both slow and fast charging points
    cleaned_charging_df = charging_df.groupby(['region', 'year'])['value'].sum().reset_index()
    return cleaned_charging_df

