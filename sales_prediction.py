import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap
# reading usr_data from csv
df = pd.read_csv('user_data.csv')

# Predefined weights for the model
weights = {
    'yoy': 0.2,  # YoY
    'mom': 0.2,  # MoM
    '90_days': 0.1,  # bahaviors in last 90 days
    '60_days': 0.1,  # bahaviors in last 60 days
    '10_days': 0.1,  # bahaviors in last 10 days
    'random': 0.3   # Random factor
}

# Ramdomize
random_factor = np.random.uniform(0.9, 1.1, size=len(df))

# basic version for prediction (without randomness)
category_sales = {
    'Category 1': (
        weights['yoy'] * df['Last Year 7-day Cat1 Purchase Count'] +
        weights['mom'] * df['Last Month 7-day Cat1 Purchase Count'] +
        weights['90_days'] * df['90-day Cat1 Actions'] +
        weights['60_days'] * df['30-day Cat1 Actions'] +  # subsitude 60 days with 30 days when necessary
        weights['10_days'] * df['10-day Cat1 Actions'] +
        weights['random'] * random_factor * df['Last 7-day Cat1 Purchase Count']
    ) / 30,  # prediction for daily sales
    'Category 2': (
        weights['yoy'] * df['Last Year 7-day Cat2 Purchase Count'] +
        weights['mom'] * df['Last Month 7-day Cat2 Purchase Count'] +
        weights['90_days'] * df['90-day Cat2 Actions'] +
        weights['60_days'] * df['30-day Cat2 Actions'] +
        weights['10_days'] * df['10-day Cat2 Actions'] +
        weights['random'] * random_factor * df['Last 7-day Cat2 Purchase Count']
    ) / 30,
    'Category 3': (
        weights['yoy'] * df['Last Year 7-day Cat3 Purchase Count'] +
        weights['mom'] * df['Last Month 7-day Cat3 Purchase Count'] +
        weights['90_days'] * df['90-day Cat3 Actions'] +
        weights['60_days'] * df['30-day Cat3 Actions'] +
        weights['10_days'] * df['10-day Cat3 Actions'] +
        weights['random'] * random_factor * df['Last 7-day Cat3 Purchase Count']
    ) / 30
}


# generate a ranmdom factor for each day over the next 30 days (between 0.5-2.1)
daily_random_factors = np.random.uniform(0.8, 1.2, size=(30, 3))


# generate the daily sales for next 30 days ( with daily random applied)
future_sales = pd.DataFrame({
    f'Day {i+1}': [
        category_sales['Category 1'].sum() * daily_random_factors[i, 0],
        category_sales['Category 2'].sum() * daily_random_factors[i, 1],
        category_sales['Category 3'].sum() * daily_random_factors[i, 2]
    ] for i in range(30)
}, index=['Category 1', 'Category 2', 'Category 3'])


# summarize all cata for the total, daily
total_daily_sales = future_sales.sum(axis=0)

# create the Panel
fig, axes = plt.subplots(1, 2, figsize=(16, 8))


# ---- Chart1: 三个类目未来30天销量趋势图 ---- #
# ---- Chart1: Sales trend for the next 30 days across 3 catagories ---- #
future_sales.T.plot(ax=axes[0], marker='o')
axes[0].set_title('Future 30-day Sales Trend by Category')
axes[0].set_xlabel('Day')
axes[0].set_ylabel('Sales')
axes[0].legend(title='Category') 

# ---- 图表2: 每日销量占比的累积占比图 ---- #
# ---- Chart2: Sales composition for daily sales across 3 catagories ---- #
future_sales.div(total_daily_sales, axis=1).T.plot.area(ax=axes[1], stacked=True, cmap='Set2', alpha=0.7)
axes[1].set_title('Daily Sales Percentage by Category')
axes[1].set_xlabel('Day')
axes[1].set_ylabel('Percentage of Total Sales')
axes[1].legend(title='Category')


# show the charts
plt.tight_layout()
plt.show()
