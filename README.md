# AAVAIL 30-Day Revenue Forecasting

## Business objective
Forecast revenue over the next 30 days for the ten highest-revenue countries and the combined `all` market. The output supports staffing and budget decisions.

## Hypotheses
1. Recent daily revenue (1, 7, 30, 90 and 365-day lags) contains predictive signal for the next 30 days.
2. Rolling averages and volatility capture level and trend changes.
3. Country-specific models outperform one global model because purchase patterns differ by market.
4. Tree ensembles can capture nonlinear relationships better than a persistence/mean baseline.
5. Revenue peaks may be seasonal; day-of-year and month features can help capture recurring patterns.

## Data requirements
Transaction date, country, line-item price/revenue, invoice identifier, stream identifier and views. Customer identifier is useful for segmentation but is incomplete and should not be required. Transaction data are aggregated to daily country revenue; missing calendar dates are zero-filled after aggregation. Cancelled invoices (invoice IDs beginning with C) are excluded.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_eda.py
python -c "from src.model import train; print(train()['metrics'])"
pytest -q
python -m src.app
```

POST `/predict` JSON: `{"country":"United Kingdom","target_date":"2019-08-01"}`. Country may be one of the ten training leaders or `all`. The date is the first day of the 30-day forecast window and requires at least 365 days of prior history. GET `/logfile` returns prediction logs. POST `/train` retrains models.

## Docker
`docker build -t aavail-forecast . && docker run -p 5000:5000 aavail-forecast`

## Evaluation design
Chronological 80/20 holdout per country; compare Random Forest, Extra Trees and HistGradientBoosting using MAE/RMSE, alongside a trailing-training-mean baseline. The selected estimator is refit on all available training examples. Production JSON files are held out for post-production simulation and must not be mixed into training.

## Limitations
The historical dataset is relatively short. A 365-day lookback limits supervised samples; forecasts are sensitive to unusual invoice batching, returns handling and changes in business model. Validate the exact monetary semantics and compare the forecast with actual 30-day revenue before operational use.
