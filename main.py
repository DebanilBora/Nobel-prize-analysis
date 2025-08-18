# Day 79: Nobel Prize Data Analysis

import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============== SETUP ==============
# Create plots directory if not exists
os.makedirs("plots", exist_ok=True)

# Helper function to save plots
def save_plot(filename):
    plt.savefig(f"plots/{filename}", dpi=200, bbox_inches="tight")
    plt.close()


# ============== LOAD DATA ==============
df_data = pd.read_csv("nobel_prize_data.csv")

# Basic exploration
print(df_data.shape)
print(df_data.columns)
print(df_data.head())
print(df_data.tail())

# First and last years
print(df_data.year.min(), df_data.year.max())

# Check for duplicates and NaNs
print(df_data.duplicated().values.any())
print(df_data.isna().sum())

# Convert birth_date to datetime
df_data.birth_date = pd.to_datetime(df_data.birth_date)

# Add share_pct column
split_share = df_data.prize_share.str.split('/', expand=True)
df_data['share_pct'] = pd.to_numeric(split_share[0]) / pd.to_numeric(split_share[1])


# ============== PLOTLY INTERACTIVE CHARTS ==============
# Donut chart: Men vs Women
sex_counts = df_data.sex.value_counts()
fig = px.pie(names=sex_counts.index, values=sex_counts.values,
             title="Male vs Female Winners", hole=0.4)
fig.update_traces(textposition='inside', textinfo='percent')
fig.show()

# First 3 female winners
print(df_data[df_data.sex == 'Female'].sort_values('year').head(3))

# Repeat winners
repeat_winners = df_data[df_data.duplicated(subset=['full_name'], keep=False)]
print(repeat_winners.full_name.nunique())
print(repeat_winners[['year', 'category', 'laureate_type', 'full_name']])

# Bar chart: Prizes by category
category_counts = df_data.category.value_counts()
fig = px.bar(x=category_counts.index, y=category_counts.values,
             color=category_counts.values, color_continuous_scale='Aggrnyl')
fig.update_layout(title="Number of Prizes per Category",
                  xaxis_title="Category", yaxis_title="Number of Prizes",
                  coloraxis_showscale=False)
fig.show()

# First Economics prize
econ_first = df_data[df_data.category == 'Economics'].sort_values('year').head(1)
print(econ_first)

# Gender split by category
gender_split = df_data.groupby(['category', 'sex']).agg({'prize': 'count'}).reset_index()
fig = px.bar(gender_split, x='category', y='prize', color='sex',
             title="Prizes per Category Split by Gender")
fig.update_layout(xaxis_title="Category", yaxis_title="Number of Prizes")
fig.show()

# Top 20 countries
top_countries = df_data.groupby('birth_country_current').agg({'prize': 'count'}).reset_index()
top20 = top_countries.sort_values('prize', ascending=False).head(20)
fig = px.bar(top20, x='prize', y='birth_country_current',
             orientation='h', color='prize', color_continuous_scale='Viridis')
fig.update_layout(title='Top 20 Countries by Number of Prizes',
                  xaxis_title='Number of Prizes', yaxis_title='Country',
                  coloraxis_showscale=False)
fig.show()

# Choropleth map
map_data = df_data.groupby(['birth_country_current', 'ISO']).agg({'prize': 'count'}).reset_index()
fig = px.choropleth(map_data, locations='ISO', color='prize',
                    hover_name='birth_country_current',
                    color_continuous_scale=px.colors.sequential.matter)
fig.update_layout(title='Nobel Prizes by Country')
fig.show()

# Country breakdown by category
country_category = df_data.groupby(['birth_country_current', 'category']).agg({'prize': 'count'}).reset_index()
merged = pd.merge(country_category, top20[['birth_country_current']], on='birth_country_current')
fig = px.bar(merged, x='prize', y='birth_country_current', color='category',
             orientation='h', title='Top 20 Countries by Category')
fig.update_layout(xaxis_title='Number of Prizes', yaxis_title='Country')
fig.show()

# Cumulative country prizes over time
yearly_country = df_data.groupby(['birth_country_current', 'year']).agg({'prize': 'count'}).reset_index()
yearly_country['cumsum'] = yearly_country.groupby('birth_country_current')['prize'].cumsum()
fig = px.line(yearly_country, x='year', y='cumsum', color='birth_country_current')
fig.update_layout(title='Cumulative Nobel Prizes by Country Over Time',
                  xaxis_title='Year', yaxis_title='Cumulative Prizes')
fig.show()

# Top 20 institutions
top_orgs = df_data.organization_name.value_counts().head(20).sort_values(ascending=True)
fig = px.bar(x=top_orgs.values, y=top_orgs.index, orientation='h',
             color=top_orgs.values, color_continuous_scale='haline')
fig.update_layout(title='Top 20 Research Institutions',
                  xaxis_title='Number of Prizes', yaxis_title='Institution',
                  coloraxis_showscale=False)
fig.show()

# Top 20 research cities
top_cities = df_data.organization_city.value_counts().head(20).sort_values(ascending=True)
fig = px.bar(x=top_cities.values, y=top_cities.index, orientation='h',
             color=top_cities.values, color_continuous_scale='Plasma')
fig.update_layout(title='Top Research Cities',
                  xaxis_title='Number of Prizes', yaxis_title='City',
                  coloraxis_showscale=False)
fig.show()

# Top 20 birth cities
top_birth = df_data.birth_city.value_counts().head(20).sort_values(ascending=True)
fig = px.bar(x=top_birth.values, y=top_birth.index, orientation='h',
             color=top_birth.values, color_continuous_scale='Plasma')
fig.update_layout(title='Top Birth Cities of Laureates',
                  xaxis_title='Number of Prizes', yaxis_title='City',
                  coloraxis_showscale=False)
fig.show()

# Sunburst chart
org_group = df_data.groupby(['organization_country', 'organization_city', 'organization_name']).agg({'prize': 'count'}).reset_index()
fig = px.sunburst(org_group, path=['organization_country', 'organization_city', 'organization_name'], values='prize')
fig.update_layout(title='Research Location Breakdown')
fig.show()


# ============== MATPLOTLIB / SEABORN (SAVED) ==============
# Prizes per year + rolling avg
prizes_per_year = df_data.groupby('year').prize.count()
rolling_avg = prizes_per_year.rolling(window=5).mean()
plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes per Year')
plt.xticks(ticks=np.arange(1900, 2021, step=5), rotation=45)
plt.scatter(prizes_per_year.index, prizes_per_year.values, c='dodgerblue', s=100, alpha=0.6)
plt.plot(rolling_avg.index, rolling_avg.values, c='crimson', linewidth=3)
save_plot("prizes_per_year.png")

# Rolling average of share_pct
yearly_share_avg = df_data.groupby('year').agg({'share_pct': 'mean'})
share_rolling_avg = yearly_share_avg.rolling(window=5).mean()
plt.figure(figsize=(16,8), dpi=200)
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.scatter(prizes_per_year.index, prizes_per_year.values, c='dodgerblue', s=100, alpha=0.6)
ax1.plot(rolling_avg.index, rolling_avg.values, c='crimson', linewidth=3)
ax2.plot(share_rolling_avg.index, share_rolling_avg.values, c='grey', linewidth=3)
ax2.invert_yaxis()
plt.title('Nobel Prizes & Laureate Share Over Time')
save_plot("prizes_and_share.png")

# Calculate winning age
birth_year = df_data.birth_date.dt.year
df_data['winning_age'] = df_data.year - birth_year

# Age distribution
plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data, x='winning_age', bins=30)
plt.title('Distribution of Winning Age')
save_plot("age_distribution.png")

# Age trend over time
plt.figure(figsize=(8,4), dpi=200)
sns.regplot(data=df_data, x='year', y='winning_age', lowess=True,
            scatter_kws={'alpha': 0.5}, line_kws={'color': 'black'})
plt.title('Age at Time of Award Over Time')
save_plot("age_trend.png")

# Boxplot by category
plt.figure(figsize=(8,4), dpi=200)
sns.boxplot(data=df_data, x='category', y='winning_age')
plt.title('Winning Age by Prize Category')
save_plot("age_by_category.png")

# lmplot by category
sns.lmplot(data=df_data, x='year', y='winning_age', row='category',
           lowess=True, aspect=2,
           scatter_kws={'alpha': 0.4}, line_kws={'color': 'black'})
plt.savefig("plots/lmplot_by_category.png", dpi=200, bbox_inches="tight")
plt.close()

# Combined lmplot
sns.lmplot(data=df_data, x='year', y='winning_age', hue='category',
           lowess=True, aspect=2,
           scatter_kws={'alpha': 0.5}, line_kws={'linewidth': 3})
plt.title('Age by Year for Each Prize Category')
plt.savefig("plots/lmplot_combined.png", dpi=200, bbox_inches="tight")
plt.close()

print("✅ All Matplotlib/Seaborn plots saved in 'plots/' folder.")
