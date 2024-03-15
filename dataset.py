import pandas as pd
import matplotlib.pyplot as plt

# Process the Gini data
gini_df = pd.read_csv('unprocessed/gini.csv')
gini_df = gini_df.dropna(subset=['Country Name']).replace("..", pd.NA).dropna(subset=['Series Name'])
years = [f"{year} [YR{year}]" for year in range(1973, 2023)]
melted_gini_df = gini_df.melt(id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
                              value_vars=years, var_name="year", value_name="gini")
melted_gini_df['year'] = pd.to_numeric(melted_gini_df['year'].apply(lambda x: x.split(' ')[0]))
melted_gini_df = melted_gini_df[(melted_gini_df['year'] < 2010) & (melted_gini_df['year'] >= 1980) & melted_gini_df['gini'].notna()]

# Process the employment data and merge
revs_df = pd.read_csv('unprocessed/emps.csv')
revs_df['datadate'] = pd.to_datetime(revs_df['datadate'])
revs_df['year'] = revs_df['datadate'].dt.year
revs_df_tech = revs_df[revs_df['naics'].astype(str).str.match(r'^(51|54)')]
employees_by_year_tech = revs_df_tech.groupby('year')['emps'].sum().reset_index()
employees_by_year_tech.rename(columns={'emps': 'tech_employees'}, inplace=True)

# Merge with Gini data
merged_df = pd.merge(melted_gini_df, employees_by_year_tech, on='year', how='left')

# Process the stock data
stocks_df = pd.read_csv('unprocessed/stocks.csv')
stocks_df = stocks_df[stocks_df['ALTPRC'] >= 0]
stocks_df['year'] = pd.to_datetime(stocks_df['date']).dt.year
stocks_df = stocks_df[stocks_df['year'] < 2010]
stocks_df['market_cap'] = stocks_df['ALTPRC'] * stocks_df['SHROUT'] / 1000000
total_market_cap_by_year = stocks_df.groupby('year')['market_cap'].sum().reset_index()
stocks_df['SICCD'] = stocks_df['SICCD'].astype(str)

# Specific SIC codes for tech companies
specific_sic_codes = [
    '3571', '3572', '3575', '3576', '3651', '3652', '3661', '3663', '3669',
    '3670', '3672', '3674', '3677', '3678', '3679', '3690', '3695', '3844',
    '3577', '7370', '7371', '7372', '7373', '7374', '7377'
]

condition1 = stocks_df['SICCD'].str.startswith('48')
condition2 = stocks_df['SICCD'].isin(specific_sic_codes)
tech_condition = condition1 | condition2

tech_stocks_df = stocks_df[tech_condition]
tech_market_cap_by_year = tech_stocks_df.groupby('year')['market_cap'].sum().reset_index()
tech_market_cap_by_year.rename(columns={'market_cap': 'tech_market_cap'}, inplace=True)
final_df = pd.merge(merged_df, tech_market_cap_by_year, on='year', how='left')
final_df = pd.merge(final_df, total_market_cap_by_year, on='year', how='left', suffixes=('', '_total'))

final_df['tech_market_share'] = (final_df['tech_market_cap'] / final_df['market_cap']) * 100

# Drop unnecessary columns
final_df.drop(['Country Name', 'Country Code', 'Series Name', 'Series Code', 'market_cap'], axis=1, inplace=True)

# Saving the final DataFrame to main.csv
final_df.to_csv('main.csv', index=False)

