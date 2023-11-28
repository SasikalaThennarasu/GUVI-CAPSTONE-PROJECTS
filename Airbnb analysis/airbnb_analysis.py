#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORTING REQUIRED LIBRARIES
import pandas as pd
import numpy as np
import pymongo
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt


# In[33]:


client = pymongo.MongoClient("mongodb+srv://tsasionmail:wqqQTvp92YLTtKJh@cluster0.uffoaac.mongodb.net/")
db = client.sample_airbnb
col = db.listingsAndReviews


# #  Establishing connection with mongodb atlas

# In[3]:


rel_data = []
for i in col.find():
    data = dict(Id = i['_id'],
                Listing_url = i['listing_url'],
                Name = i.get('name'),
                Description = i['description'],
                House_rules = i.get('house_rules'),
                Property_type = i['property_type'],
                Room_type = i['room_type'],
                Bed_type = i['bed_type'],
                Min_nights = int(i['minimum_nights']),
                Max_nights = int(i['maximum_nights']),
                Cancellation_policy = i['cancellation_policy'],
                Accomodates = i['accommodates'],
                Total_bedrooms = i.get('bedrooms'),
                Total_beds = i.get('beds'),
                Availability_365 = i['availability']['availability_365'],
                Price = i['price'],
                Security_deposit = i.get('security_deposit'),
                Cleaning_fee = i.get('cleaning_fee'),
                Extra_people = i['extra_people'],
                Guests_included= i['guests_included'],
                No_of_reviews = i['number_of_reviews'],
                Review_scores = i['review_scores'].get('review_scores_rating'),
                Amenities = ', '.join(i['amenities']),
                Host_id = i['host']['host_id'],
                Host_name = i['host']['host_name'],
                Street = i['address']['street'],
                Country = i['address']['country'],
                Country_code = i['address']['country_code'],
                Location_type = i['address']['location']['type'],
                Longitude = i['address']['location']['coordinates'][0],
                Latitude = i['address']['location']['coordinates'][1],
                Is_location_exact = i['address']['location']['is_location_exact']
    )
    rel_data.append(data)


# In[4]:


df = pd.DataFrame(rel_data)


# In[5]:


df


# In[6]:


df.info()


# In[7]:


# The below features are in Decimal128 type hence changing it to relevant data types
df.Price = df.Price.astype(str).astype(float)
df.Security_deposit = df.Security_deposit[~df.Security_deposit.isna()].astype(str).astype(float)
df.Cleaning_fee = df.Cleaning_fee[~df.Cleaning_fee.isna()].astype(str).astype(float)
df.Extra_people = df.Extra_people.astype(str).astype(float)
df.Guests_included = df.Guests_included.astype(str).astype(float)
df.Review_scores = df.Review_scores.astype('Int64')


# ## FILLING NULL VALUES
# 

# In[8]:


df.isna().sum()


# In[9]:


# Filling Total bedrooms with mode
df.Total_bedrooms.fillna(df.Total_bedrooms.mode()[0],inplace=True)


# In[10]:


# Filling Total beds with median 
df.Total_beds.fillna(df.Total_beds.median(),inplace=True)


# In[11]:


#Filling Security_deposit,Review_scores,Cleaning_fee with median
df.Security_deposit.fillna(df.Security_deposit.median(),inplace=True)
df.Cleaning_fee.fillna(df.Cleaning_fee.median(),inplace=True)
df.Review_scores.fillna(df.Review_scores.median(),inplace=True)


# In[12]:


# Filling Empty values in Description and House rules columns
df.Description.replace(to_replace='',value='No Description Provided',inplace=True)
df.House_rules.replace(to_replace='',value='No House rules Provided',inplace=True)
df.Amenities.replace(to_replace='',value='Not Available',inplace=True)


# In[13]:


df.isna().sum()


# In[14]:


# Name Column has empty values and some duplicates hence dropping them
df.drop(labels=list(df[df.Name.duplicated(keep=False)].index),inplace=True)


# In[15]:


df.reset_index(drop=True,inplace=True)


# In[16]:


# Converting dataframe to csv file and saving it
df.to_csv('Airbnb_data.csv',index=False)


# #  EXPLORATARY DATA ANALYSIS

# In[19]:


#what are the top 10 property types available?
plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,y=df.Property_type.values,order=df.Property_type.value_counts().index[:10])
ax.set_title("Top 10 Property Types available")


# In[20]:


#Total listings in each Roomtype
plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,x=df.Room_type)
ax.set_title("Total Listings in each Room Type")


# In[21]:


# top 10 Hosts with Highest number of listings
df.Host_name.value_counts()


# In[22]:


plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,y=df.Host_name,order=df.Host_name.value_counts().index[:10])
ax.set_title("Top 10 Hosts with Highest number of Listings")


# In[24]:


country_df = df.groupby('Country',as_index=False)['Price'].mean()


# In[25]:


#Average listing price in each country
fig = px.scatter(data_frame=country_df,
           x='Country',y='Price',
           color='Country',
           size='Price',
           opacity=1,
           size_max=35,
           title='Avg Listing Price in each Countries')
fig.show()


# In[26]:


price_location=df.groupby(['Country_code'])['Price'].mean().reset_index().sort_values(by='Price',ascending=False)[0:10]
price_location


# In[27]:


plt.figure(figsize=(14,5))
sns.lineplot(x='Country_code',y='Price',data=price_location)
plt.xticks(rotation=60)

for i,data in enumerate(price_location['Price']):
    plt.text(x=i,y=data+29,s=f'{data}',ha='center',va='bottom')

plt.title('CountryCode and Price')
plt.show()


# In[28]:


# Group by 'Country' and 'Property_type' and count the occurrences
grouped_df = df.groupby(['Country', 'Property_type']).size().reset_index(name='CountProperty')

# Create the bar chart using Plotly Express
fig = px.bar(grouped_df,
             title='Property Type Counts by Country',
             x='CountProperty',
             y='Property_type',
             orientation='h',
             color='Country',
             color_continuous_scale=px.colors.sequential.Agsunset)

# Show the chart
fig.show()


# In[29]:


import pandas as pd
import plotly.express as px

# Assuming you have a DataFrame 'df2' with your data

# Group by 'Property_type' and count the occurrences
grouped_df = df.groupby('Property_type').size().reset_index(name='Number')

# Sort by Number in descending order and get the top 10
top_property_types = grouped_df.sort_values(by='Number', ascending=False).head(10)

# Create a pie chart using Plotly Express
fig = px.pie(top_property_types,
             names='Property_type',
             values='Number',
             title='Top 10 Property Types by Number of Listings')

# Show the chart
fig.show()


# In[30]:


# Group by 'Room_type' and calculate the average price for each room type
grouped_df = df.groupby('Room_type')['Price'].mean().reset_index()

# Create a sunburst chart using Plotly Express
fig = px.sunburst(grouped_df,
                 path=['Room_type'],
                 values='Price',
                 title='Room Type and  Price Sunburst Chart')

# Show the chart
fig.show()


# In[31]:


# Group the data by 'Review_Scores' and calculate the average price for each group
grouped_df = df.groupby('Review_scores')['Price'].mean().reset_index()

x = grouped_df['Review_scores']
y = grouped_df['Price']

plt.scatter(x, y)
plt.xlabel('Review_scores')
plt.ylabel('Average Price')
plt.title('Scatter Plot of Review_Scores vs Average Price')

# Show the plot
plt.show()


# In[ ]:




