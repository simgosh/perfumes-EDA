#importing relatable libraries 

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

#loading datasets 

men = pd.read_csv("ebay_mens_perfume.csv")
women = pd.read_csv("ebay_womens_perfume.csv")

print(men.head())
print(women.head())

men["sex"] = "men"
women["sex"] = "women"

#concated 2 datasets
df = pd.concat([men, women], ignore_index=True)
print(df.head())
print(df.shape)

#check out missing values and filling 
print(df.isnull().sum())

df = df.fillna({
    "brand":"Unknown",
    "type":"Unknown",
    "available":0,
    "availableText":"Not Available",
    "sold":0,
    "lastUpdated":"Unknown"
})

print(df.isnull().sum())
print(df.info())

df["currency"] = "US"
print(df.columns)
df.drop("priceWithCurrency", axis=1,  inplace=True)
print(df.columns)
print(df.head())

#move to currency from last column to fourth column (next to price column)
fourth = df.pop('currency') 
df.insert(4, 'currency', fourth)
print(df.columns) 
print(df[["price", "sold"]])

#move to sold from last column to fifth column (next to currency column)
fifth = df.pop('sold') 
df.insert(5, 'sold', fifth)
print(df.columns) 

#calculate total revenue
df["revenue"] = df["price"] * df["sold"]
print(df.head())

#move to revenue from last column to sixth column (next to price column)
sixth = df.pop('revenue') 
df.insert(6, 'revenue', sixth)
print(df.columns) 

#top brands barplot
top_brands = df["brand"].value_counts().nlargest(15)
print(top_brands)
#palette = sns.color_palette("tab10")
#ax = sns.barplot(x=top_brands, y=top_brands.index, legend="auto", palette=palette, saturation=0.75)
#for i in ax.containers:
#    ax.bar_label(i,)
#plt.title("Top Brands for Perfume")
#plt.xlabel("Number of Listing")
#plt.ylabel("Brands Name")
#plt.show()

print(df["lastUpdated"])

#last updated column convert to datetime
df["lastUpdated"] = pd.to_datetime(df["lastUpdated"], format="mixed", errors="coerce")
print(df.info())
print(df["lastUpdated"].head())

#sns.lineplot(data=df, x="lastUpdated", y=df.index)
#plt.title("Time Plot")
#plt.xlabel("Timezone")
#plt.show()

#the most usable itemlocation 
top_location = df["itemLocation"].value_counts().nlargest(15)
print(top_location)

plt.figure(figsize=(15,4))
palette = sns.color_palette("husl", 8)
sns.barplot(x=top_location, y=top_location.index, palette=palette)
plt.title("Top Locations")
plt.xlabel("Number of Listing")
plt.ylabel("Locations")
#plt.show()

#correlation matrix fro numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64', "number"]).columns
corr = df[numeric_columns].corr()
print(corr)

#plt.figure(figsize=(12,4))
#sns.heatmap(corr, cmap='viridis', annot=True, fmt='.2f')
#plt.title('Correlation Matrix Heatmap')
#plt.show()


#sales for brand
sales_top_brand=df.groupby("brand")["revenue"].sum().sort_values(ascending=False).nlargest(15)
#fig = px.bar(sales_top_brand, color="value", 
#              title="Revenue for Top Brand",
#              labels={"brand":"Perfume Top Brand", "value":"Values"})
#fig.show()

sales_least_brand=df.groupby("brand")["revenue"].sum().sort_values(ascending=True).head(10)
#fig1 = px.bar(sales_least_brand, color="value", 
#              title="Revenue for Least Brand",
#              labels={"brand":"Perfume Least Brand", "value":"$"})
#fig1.show()

#Available vs. Sold perfumes
#fig3 = px.scatter(df, x="available", y="sold",
#                  hover_data="revenue",
#                  color = "revenue",
#                  color_continuous_scale=px.colors.sequential.Viridis)
#fig3.show()


#Lineplot for timeseries
fig4 = px.line(df, x="lastUpdated", y="revenue",
               hover_data="type",
               color="brand",
               color_discrete_sequence=px.colors.qualitative.G10,
               title="Last Updated for Brands",
               labels={"lastUpdated":"Timezone", "revenue":"Revenue"})
#fig4.show()


df["sex"] = df["sex"].astype("category")
print(df.info())

#comparison price for men vs women
fig5 = px.box(df, x="sex", y="price", hover_data="brand",
              color="sex",
              color_discrete_sequence=["goldenrod", "magenta"],
              title="Price Comparison for Men vs Women ",
              labels={"sex":"Gender", "price":"Price (USD)"})
#fig5.show()


availability_for_brand = df.groupby(["brand", "itemLocation"])["available"].sum().sort_values(ascending=False).nlargest(15)
print(availability_for_brand)

#Lineplot sales for timeseries
fig6 = px.line(df, x="lastUpdated", y="sold",
               hover_data="type",
               color="brand",
               color_discrete_sequence=px.colors.qualitative.G10_r,
               title="Last Updated Sold for Brands",
               labels={"lastUpdated":"Timezone", "sold":"Sold"})
fig6.show()
