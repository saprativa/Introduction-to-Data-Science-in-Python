
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    f = open('university_towns.txt', 'r')
    df = pd.DataFrame(columns=["State", "RegionName"])
    state = ''
    city = ''

    for line in f:
        square = line.find('[ed')
        parenthesis = line.find('(')
    
        if(square >= 0):
            state = line[:square].strip()
        else:
            if(parenthesis >= 0):
                city = line[:parenthesis].strip()
            else:
                city = line.strip()
        
            df = df.append({'State' : state, 'RegionName' : city}, ignore_index=True)
 
    f.close()    
    
    return (df)

get_list_of_university_towns()


# In[5]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', usecols=[4, 6], skiprows=219, names=['Quarter', 'Dollars'])
    df = df.set_index('Quarter')
    df['Diff'] = df['Dollars'] - df['Dollars'].shift()
    return ((df[(df['Diff'] < 0) & (df['Diff'].shift(-1) < 0)]).index[0])

get_recession_start()


# In[6]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', usecols=[4, 6], skiprows=219, names=['Quarter', 'Dollars'])
    df = df.set_index('Quarter')
    df['Diff'] = df['Dollars'] - df['Dollars'].shift()
    df = df.loc[get_recession_start():, :]
       
    return ((df[(df['Diff'] > 0) & (df['Diff'].shift(-1) > 0)]).index[1])

get_recession_end()


# In[7]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', usecols=[4, 6], skiprows=219, names=['Quarter', 'Dollars'])
    df = df.set_index('Quarter')
    df['Diff'] = df['Dollars'] - df['Dollars'].shift()
    df = df.loc[get_recession_start(): get_recession_end(), :]
    
    return (df['Dollars'].idxmin())

get_recession_bottom()


# In[8]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv') 
                     
    def lookup(string):
        if string in states:
            return states[string]
        return string

    df.State = df.State.apply(lookup)

    df = df.set_index(['State','RegionName'])

    df = df.iloc[:, 49:]
    
    
    df.columns = pd.to_datetime(df.columns)
    df = df.resample('Q',axis=1).mean()
    df = df.rename(columns=lambda x: str(x.to_period('Q')).lower())
    
    return (df)
 
convert_housing_data_to_quarters()


# In[29]:


from scipy import stats
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    gdp = pd.read_excel('gdplev.xls', usecols=[4, 6], skiprows=219, names=['Quarter', 'Dollars'])
    gdp = gdp.set_index('Quarter')
    
    quarter_before_recession = gdp.index[gdp.index.get_loc(get_recession_start()) - 1]
    recession_bottom = get_recession_bottom()
    
    house = convert_housing_data_to_quarters()
    
    house['PriceRatio'] = house[quarter_before_recession].div(house[recession_bottom])
    
    university_towns = get_list_of_university_towns()
    
    uni_housing = pd.merge(university_towns.set_index(["State", "RegionName"]), house, left_index=True, right_index=True)
    
    non_uni_housing = house[~house.index.isin(university_towns.to_records(index=False).tolist())]
    
    tt = stats.ttest_ind(uni_housing['PriceRatio'], non_uni_housing['PriceRatio'], nan_policy='omit')
    
    p = tt[1]
    
    different  = p < 0.01
    
    better = ''
    
    if(non_uni_housing['PriceRatio'].mean() < uni_housing['PriceRatio'].mean()):
        better = 'non-university town'
    else:
        better = 'university town'
    
    return ((different, p, better))

run_ttest()


# In[ ]:




