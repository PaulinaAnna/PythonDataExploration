import csv

import pandas as pd

df = pd.read_csv('owid-covid-data.csv')

#checking if all data types are in right format

print('\033[1m' + "\n 1. Check if my data are in right formats\n"+ '\033[0m')

print ('Data in my file:')
print(df.dtypes)
print('My data are in right formats')

# creating new file with filtered data

cols =['iso_code','continent', 'location','date','human_development_index','median_age','excess_mortality_cumulative_per_million']

subset = ['2021-10-31']
df_f = df.loc[df['date'].isin(subset)]
df_f[cols].to_csv('filtered_owid-covid-data.csv', index = False)

#few statistics

print('\033[1m' + "\n 2. Basic statistical information\n"+ '\033[0m')

df_f = pd.read_csv('filtered_owid-covid-data.csv')

df_f.describe()
print('\033[1m' + "\n 4. Statistical despription of data\n"+ '\033[0m')
print(df_f.describe())
df_f[cols].describe().to_csv('./summary.csv')

# adding addtional information if data meet the criteria

print('\033[1m' + "\n 3. New column in our setaset \n"+ '\033[0m')

for index, row in df_f.iterrows():
    if row['excess_mortality_cumulative_per_million'] > 3302.91:
        df_f.loc[index,'desc_mort'] = 'hight mortality'
    elif row['excess_mortality_cumulative_per_million'] > 1831.36:
        df_f.loc[index,'desc_mort'] = 'medium mortality'
    elif row['excess_mortality_cumulative_per_million'] > 0.00:
        df_f.loc[index, 'desc_mort'] = 'mortality a little bit higher'
    elif row['excess_mortality_cumulative_per_million'] < 0.00:
        df_f.loc[index, 'desc_mort'] = 'mortality is lower'
    else:
        df_f.loc[index, 'desc_mort'] = 'nd'

print(df_f)
df_f.to_csv('filtered_owid-covid-data.csv',index=False)

print('\033[1m' + "\n 4. Pivot summary \n"+ '\033[0m')

table = pd.pivot_table(df_f,index=['continent'],values=['human_development_index','median_age','excess_mortality_cumulative_per_million'],aggfunc='mean')
print(table)

# Comparing data from different continets we can observe that:
#- Europe is much older that than other continents, the quality of life is much higher
#- The hihest level of additional ortality we have in South America, we relaitely young popuulation
# - In Oceania deth toll was even a bit lower than before the pandemic

table.to_csv('./pivot.csv')

subset = ['hight mortality']
df_hm = df_f.loc[df_f['desc_mort'].isin(subset)]
df_hm.to_csv('./high_mort.csv', index = False)

df_hm.describe()
df_hm.describe().to_csv('./summary_hm.csv')

#Comparing data summaries for countires with high mortality to the general data we can observe that both median age
# and quality of life are higher.

#wrting data to excel


#saving data to excel
df_f.to_excel('./project.xls', sheet_name = 'filtered_owid_data', index = False)

# Import libraries

import pycountry
import plotly.express as px

df_f = pd.read_csv('filtered_owid-covid-data.csv')

list_countries = df_f['location'].unique().tolist()

# print list of countries

print( list_countries )

d_country_code = {}
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('\ncould not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

# print country ISO codes

print('\033[1m' + "\n List of ISO country codes:\n"+ '\033[0m')

print(d_country_code)

# create a new column iso_alpha in the df and fill it with  iso 3 code
for k, v in d_country_code.items():
    df_f.loc[(df_f.location == k), 'iso_alpha'] = v

# print(df_f.head) to check ISO code added

print(df_f.head)

# Graph

fig = px.choropleth(data_frame = df_f,
                    locations= "iso_alpha",
                    color= 'excess_mortality_cumulative_per_million',  # value in column determines color
                    hover_name= "location",
                    color_continuous_scale= 'RdYlGn_r',  #  color scale red, yellow green
                    animation_frame= "date")

fig.update_layout(
    title_text = 'Excess mortality as of October 31, 2021',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
        projection_type = 'equirectangular'
    )
)
fig.show()