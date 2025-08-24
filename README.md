🏅 Nobel Prize Data Analysis

An end-to-end data analysis project exploring Nobel Prize winners from 1901 to 2020.
The project uses pandas, Plotly, seaborn, and matplotlib to uncover trends in gender, geography, research institutions, and the age of Nobel laureates.

Interactive Plotly charts provide an engaging way to explore the dataset, while static seaborn/matplotlib plots are saved for reporting.

🚀 Features

Data Cleaning & Preparation

Handled missing values and duplicates.

Extracted prize share percentage from fractional values (e.g., 1/2, 1/3).

Converted birth dates to datetime format.

Exploratory Data Analysis (EDA)

First and last years of Nobel awards.

Gender split of laureates.

Repeat winners across years and categories.

First prize in Economics (added in 1969).

Interactive Plotly Visualizations

🍩 Donut chart: Male vs Female winners.

📊 Bar charts: Prizes by category, gender split per category, top countries, cities, and institutions.

🌍 Choropleth map: Global distribution of Nobel Prizes.

🌞 Sunburst chart: Research institutions grouped by country & city.

📈 Cumulative country performance over time.

Static Seaborn & Matplotlib Plots (saved to /plots)

Prizes per year + rolling average.

Nobel Prizes vs. average prize share percentage.

📉 Age trends over time.

📦 Distribution & boxplots of winning age by category.

🔬 Regression plots (per category & combined).

🛠️ Tech Stack

Python 🐍

pandas – Data cleaning & manipulation

numpy – Numerical calculations

plotly.express – Interactive visualizations

matplotlib & seaborn – Statistical plots

▶️ How to Run

Clone this repo:

git clone https://github.com/DebanilBora/Nobel-prize-analysis.git
cd nobel-prize-analysis


Install dependencies:

pip install pandas numpy matplotlib seaborn plotly


Run the script:

python main.py


Interactive charts will open in your browser.

Static plots will be saved in the plots/ folder.

📌 Key Insights

Only ~6% of Nobel Prizes have been awarded to women.

The United States leads in Nobel Prizes, followed by the UK and Germany.

Top institutions include Harvard, Stanford, and Cambridge.

Average age of laureates has increased over time.

Most Economics winners are older compared to Physics or Chemistry laureates.

🔖 Tags

#DataAnalysis #DataVisualization #Plotly #Seaborn #Matplotlib #NobelPrize #Python
