"""Compare logged 30-day forecasts with observed 30-day revenue."""
import argparse
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    p=argparse.ArgumentParser(); p.add_argument('--predictions',default='logs/predictions.csv'); p.add_argument('--actuals',required=True,help='CSV with country,target_date,actual_30_day_revenue'); p.add_argument('--output',default='reports/post_production_metrics.csv'); a=p.parse_args()
    pred=pd.read_csv(a.predictions); actual=pd.read_csv(a.actuals)
    merged=pred.merge(actual,on=['country','target_date'],how='inner')
    if merged.empty: raise SystemExit('No matching forecast/actual rows')
    rows=[]
    for country,g in merged.groupby('country'):
        rows.append({'country':country,'n':len(g),'mae':mean_absolute_error(g.actual_30_day_revenue,g.forecast_30_day_revenue),'rmse':mean_squared_error(g.actual_30_day_revenue,g.forecast_30_day_revenue)**.5})
    out=pd.DataFrame(rows); out.to_csv(a.output,index=False); print(out.to_string(index=False))
if __name__=='__main__': main()
