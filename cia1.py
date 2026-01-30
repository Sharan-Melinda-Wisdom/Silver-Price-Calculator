import geopandas as gpd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("Silver Price Calculator")
data_hist=pd.read_csv("historical_silver_price.csv")
data_sales=pd.read_csv("state_wise_silver_purchased_kg.csv")

st.header("Silver Price Calculator")

weight=st.number_input("Enter weight of silver in grams:") 

unit=st.selectbox("Select unit:",["Grams","Kilograms"])
grams = weight * 1000 if unit == "Kilograms" else weight
price=st.number_input("Enter current price per gram (INR):")

cost_inr = grams * price
cost_usd = cost_inr / 84.0  # Assumed 1 USD = 84 INR


st.subheader(f"Total INR Cost:  {cost_inr:,.2f}")
st.write(f"(USD:  {cost_usd:,.2f})")

st.write("Historical Price Chart")
filter_opt = st.selectbox("Filter Price Range", ["All", "<= 20k", "20k - 30k", ">= 30k"])

df_chart = data_hist.copy()
if filter_opt == "<= 20k":
    df_chart = df_chart[df_chart['Silver_Price_INR_per_kg'] <= 20000]
elif filter_opt == "20k - 30k":
    df_chart = df_chart[(df_chart['Silver_Price_INR_per_kg'] > 20000) & (df_chart['Silver_Price_INR_per_kg'] < 30000)]
elif filter_opt == ">= 30k":
    df_chart = df_chart[df_chart['Silver_Price_INR_per_kg'] >= 30000]


st.line_chart(df_chart.set_index('Year')['Silver_Price_INR_per_kg']) 

st.header("Sales Dashboard")

st.subheader("Top 5 States by Sales")
top5 = data_sales.groupby('State')['Silver_Purchased_kg'].sum().nlargest(5)
st.bar_chart(top5)



st.subheader("January sales only")
january_sales = data_hist[data_hist['Month'] == "Jan"]
st.line_chart(january_sales.set_index('Year')['Silver_Price_INR_per_kg'])



st.subheader("State-wise Sales Map")
try:
  
    url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
    india_map = gpd.read_file(url)
    
    india_map['Sales'] = np.random.randint(100, 1000, size=len(india_map))
    
    fig, ax = plt.subplots(figsize=(10, 10))
    india_map.plot(column='Sales', cmap='Blues', legend=True, ax=ax)
    ax.axis('off')
    st.pyplot(fig)
    
except Exception as e:
    st.error("Could not load map")
    
    
    


