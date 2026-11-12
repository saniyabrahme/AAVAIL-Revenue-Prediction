from src.data import load_transactions,daily_revenue
import matplotlib.pyplot as plt
from pathlib import Path
Path('reports/figures').mkdir(parents=True,exist_ok=True)
df=load_transactions('cs-train'); daily,top=daily_revenue(df)
daily.to_csv('reports/daily_revenue.csv',index=False)
all_data=daily[daily.country=='all'].set_index('date')
fig,ax=plt.subplots(figsize=(12,5)); all_data.revenue.plot(ax=ax,title='Daily AAVAIL revenue (training data)'); ax.set_ylabel('Revenue'); fig.tight_layout(); fig.savefig('reports/figures/daily_revenue.png'); plt.close(fig)
monthly=all_data.revenue.resample('MS').sum(); fig,ax=plt.subplots(figsize=(12,5)); monthly.plot(kind='bar',ax=ax,title='Monthly revenue'); ax.set_ylabel('Revenue'); fig.tight_layout(); fig.savefig('reports/figures/monthly_revenue.png'); plt.close(fig)
country=df.groupby('country').revenue.sum().nlargest(10).sort_values(); fig,ax=plt.subplots(figsize=(9,6)); country.plot(kind='barh',ax=ax,title='Top 10 countries by revenue'); ax.set_xlabel('Revenue'); fig.tight_layout(); fig.savefig('reports/figures/top_countries.png'); plt.close(fig)
print('Rows:',len(df),'Date range:',df.date.min(),df.date.max(),'Top countries:',top)
