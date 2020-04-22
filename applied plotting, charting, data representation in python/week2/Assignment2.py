
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

# import matplotlib.pyplot as plt
# import mplleaflet
# import pandas as pd

# def leaflet_plot_stations(binsize, hashid):

#     df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

#     station_locations_by_hash = df[df['hash'] == hashid]

#     lons = station_locations_by_hash['LONGITUDE'].tolist()
#     lats = station_locations_by_hash['LATITUDE'].tolist()

#     plt.figure(figsize=(8,8))

#     plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

#     return mplleaflet.display()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[16]:

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

get_ipython().magic('matplotlib notebook')

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

df = df.sort_values(by='Date')

df.head()


# In[34]:

df1 = df.copy()

df1['year'], df1['month-day'] = zip(*df1['Date'].apply(lambda x: (x[:4], x[5:])))

df1.head()


# In[35]:

df1 = df1[df1['month-day'] != '02-29']


# In[48]:

tmin = df1[(df1['Element'] == 'TMIN') & (df1['year'] != '2015')].groupby('month-day').aggregate({'Data_Value':np.min})


# In[50]:

tmin.head()


# In[51]:

tmax = df1[(df1['Element'] == 'TMAX') & (df1['year'] != '2015')].groupby('month-day').aggregate({'Data_Value':np.max})


# In[53]:

tmax.head()


# In[54]:

tmin_2015 = df1[(df1['Element'] == 'TMIN') & (df1['year'] == '2015')].groupby('month-day').aggregate({'Data_Value':np.min})
tmin_2015.head()


# In[56]:

tmax_2015 = df1[(df1['Element'] == 'TMAX') & (df1['year'] == '2015')].groupby('month-day').aggregate({'Data_Value':np.max})
tmax_2015.head()


# In[63]:

err_min = np.where(tmin_2015['Data_Value'] < tmin['Data_Value'])[0]

err_max = np.where(tmax_2015['Data_Value'] > tmax['Data_Value'])[0]


# In[92]:

plt.figure(figsize=(10, 8))

plt.plot(tmin.values, 'g', label='Record low temperature by day of the year over the period 2005-2014')
plt.plot(tmax.values, 'r', label='Record high temperature by day of the year over the period 2005-2014')

plt.scatter(err_min, tmin_2015.iloc[err_min], c='blue', label='High record for 2015')
plt.scatter(err_max, tmax_2015.iloc[err_max], c='black', label='Low record for 2015')

plt.gca().fill_between(range(len(tmin)),
                    tmin['Data_Value'], 
                    tmax['Data_Value'],
                    facecolor='blue',
                    alpha=0.3)

plt.xlabel("Day of the year")
plt.ylabel('Temperature in C')
plt.title('Record high and record low temperatures by day of the year over the period 2005-2014')
plt.legend()

plt.gca().spines['right'].set_visible(False)


# In[ ]:



