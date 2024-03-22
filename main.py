import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

file_path = 'main.csv'
data = pd.read_csv(file_path)

data['log_tech_market_share'] = np.log(data['tech_market_share'])
data['trade_index'] = data['exports'] + data['imports']
data['log_immigrants'] = np.log(data['immigrants'])
data['p1'] = data['p1'] * 100
data['p50'] = data['p50'] * 100

exclude_columns = ['year', 'log_tech_market_share', 'tech_employees', 'tech_market_cap',
                   'log_tech_market_cap', 'exports', 'imports', 'fdi_in',
                   'fdi_out', 'log_immigrants', 'cap_gains', 'inflation', 'unemployment']
describe_columns = [col for col in data.columns if col not in exclude_columns]

data[describe_columns].describe().transpose().apply(lambda s: s.apply('{0:.5f}'.format))


plt.figure(figsize=(10, 6))

# Plotting both p1 and p50
plt.plot(data['year'], data['p1'], label='p1', c='teal')
plt.plot(data['year'], data['p50'], label='p50', c='#5072A7')

plt.title('P1 and P50 income share over the years')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()

plt.grid(True)
plt.show()

# Plotting gini over years
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['gini'], label='Gini Index', c='#66b2b2', marker='o')
plt.title('Gini Index over the years')
plt.xlabel('Year')
plt.ylabel('Gini Index')
plt.legend()
plt.grid(True)
plt.show()

# Plotting tech market cap over years in a separate figure
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['tech_market_cap'], label='Tech Market Cap', c='green', marker='x')
plt.title('Tech Market Cap over Years')
plt.xlabel('Year')
plt.ylabel('Tech Market Cap (Billions)')
plt.legend()
plt.grid(True)
plt.show()

# Plotting log of tech market cap over years
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['tech_market_share'], label='Tech Market Share', c='#915F6D', marker='^')
plt.title('Tech Market Share over the years')
plt.xlabel('Year')
plt.ylabel('Log of Tech Market Share')
plt.legend()
plt.grid(True)
plt.show()

# List of columns to exclude from the plots
exclude_columns = ['p1', 'p50', 'year', 'gini', 'fdi_in', 'fdi_out',
                   'cap_gains', 'tech_employees', 'tech_market_cap', 'exports', 'imports',
                   'immigrants', 'tech_market_share', 'inflation', 'unemployment', 'log_tech_market_cap'
                   ]

# Columns to be plotted
plot_columns = [col for col in data.columns if col not in exclude_columns]

# Initialize the subplot configuration
fig, axs = plt.subplots(len(plot_columns), 1, figsize=(7, 5 * len(plot_columns)))

for i, column in enumerate(plot_columns):
    axs[i].scatter(data[column], data['gini'], c='teal', marker='x')
    axs[i].set_title(f'Gini vs {column}')
    axs[i].set_xlabel(column)
    axs[i].set_ylabel('Gini Index')
    axs[i].grid(True)

plt.tight_layout()
plt.show()

cmap = sns.diverging_palette(145, 300, s=60, as_cmap=True)

correlation_matrix = data[plot_columns].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap=cmap, linewidths=.5)
plt.title('Correlation Heatmap')
plt.xticks(rotation=45)
plt.show()
