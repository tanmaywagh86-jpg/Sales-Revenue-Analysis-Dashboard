import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

data = pd.read_csv("SuperMarket Analysis.csv")
data['Date'] = pd.to_datetime(data['Date'])

data['Day'] = data['Date'].dt.day_name()
day_sales = data.groupby('Day')['Sales'].sum().sort_values(ascending=False)

day_sales.plot(kind='bar', color='skyblue')

del data['Invoice ID']

mostselled_products = data.groupby('Product line')['Sales'].sum().sort_values(ascending=False)
MostSelled_Quantity = data.groupby('Product line')['Quantity'].sum().sort_values(ascending=False)

product_day_sales = data.groupby(['Product line', 'Day'])['Sales'].sum().unstack()
best_product_perDay = product_day_sales.idxmax(axis=1)

payment = data.groupby('Payment')['Sales'].sum().sort_values(ascending=False)

gender_sales = data.groupby('Gender')['Sales'].sum().sort_values(ascending=False)

data['Time'] = pd.to_datetime(data['Time'], format='%I:%M:%S %p')

def Get_time_period(time):
    hour = time.hour
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour <17:
        return "Afternoon"
    elif 17 <= hour <21:
        return "Evening"
    else:
        "Night"

data['Time_period'] = data['Time'].apply(Get_time_period)
timesales = data.groupby('Time_period')['Sales'].sum().sort_values(ascending=False)

average_bskt_size = data['Sales'].mean()
print(f"The average basker size : {average_bskt_size}")

bskt_by_customerType = data.groupby("Customer type")["Sales"].mean()
print(bskt_by_customerType)

city_lvl = data.groupby('City')['Sales'].sum().sort_values(ascending=False)
print(city_lvl)

branch_lvl = data.groupby('Branch')['Sales'].sum().sort_values(ascending=False)
print(branch_lvl)

# Chart 1: Sales by Day
st.subheader("📆 Total Sales by Day")
fig1, ax1 = plt.subplots()
day_sales.plot(kind='bar', ax=ax1, color='skyblue')
plt.xticks(rotation=45)
st.pyplot(fig1)

# Chart 2: Top-Selling Products by Revenue
st.subheader("💰 Top-Selling Products by Revenue")
fig2, ax2 = plt.subplots()
mostselled_products.plot(kind='bar', ax=ax2, color='orange')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Chart 3: Top-Selling Products by Quantity
st.subheader("📦 Top-Selling Products by Quantity")
fig3, ax3 = plt.subplots()
MostSelled_Quantity.plot(kind='bar', ax=ax3, color='green')
plt.xticks(rotation=45)
st.pyplot(fig3)

# Chart 4: Heatmap - Product Sales by Day
st.subheader("🔥 Product Sales by Day (Heatmap)")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(product_day_sales, annot=True, fmt=".0f", cmap='YlGnBu', ax=ax4)
st.pyplot(fig4)

# Chart 5: Sales by Time Period
st.subheader("🕒 Sales by Time Period")
fig5, ax5 = plt.subplots()
timesales.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax5)
ax5.set_ylabel('')
st.pyplot(fig5)

