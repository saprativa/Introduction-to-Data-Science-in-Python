import pandas as pd

#Part 1 ------------------------------------------------------------------->

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')

print('\nAnswer Zero:\n')

def answer_zero():
    return df.iloc[0]

print(answer_zero())

print('\nAnswer One:\n')

def answer_one():
    return df.Gold.idxmax()

print(answer_one())

print('\nAnswer Two:\n')

def answer_two():
    return (abs(df['Gold'] - df['Gold.1']).idxmax())

print(answer_two())

print('\nAnswer Three:\n')

def answer_three():
    both_golds = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    return ((both_golds['Gold'] - both_golds['Gold.1'])/both_golds['Gold.2']).idxmax()

print(answer_three())

print('\nAnswer Four:\n')

def answer_four():
    Points = df['Gold.2'] * 3 + df['Silver.2'] * 2 + df['Bronze.2'] * 1
    return (Points)

print(answer_four())



#Part 2 ------------------------------------------------------------------->

census_df = pd.read_csv('census.csv')

census_df = census_df[census_df['SUMLEV'] == 50]

print('\nAnswer Five:\n')

def answer_five():
    return (census_df.set_index(["STNAME", "CTYNAME"]).count(level = "STNAME"))["SUMLEV"].idxmax()

print(answer_five())

print('\nAnswer Six:\n')

def answer_six():
    return (list(census_df.groupby('STNAME')['CENSUS2010POP'].nlargest(3).sum(level = 0).nlargest(3).index))

print(answer_six())

print('\nAnswer Seven:\n')

def answer_seven():
    c = census_df.set_index('CTYNAME').loc[:, ['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']]
    return (abs(c.max(axis=1) - c.min(axis=1)).idxmax())

print (answer_seven())

print('\nAnswer Eight:\n')

def answer_eight():
    return (census_df[((census_df['REGION'] == 1) | (census_df['REGION'] == 2)) & (census_df['CTYNAME'].str.startswith('Washington')) & (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014'])]).loc[:, ['STNAME', 'CTYNAME']]

print(answer_eight())