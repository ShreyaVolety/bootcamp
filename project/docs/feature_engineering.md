# Feature Engineering for Oil Risk Regime Project

## 1. CL=F Returns
- Log return  
- Measures daily price changes in front-month oil.  
- Captures immediate market movements; large returns may indicate shifts in risk regime.  
- High magnitude returns may signal heightened risk or volatility periods.

## 2. Rolling Volatility (5-day & 21-day)
- Standard deviation of log returns over a rolling window  
- Captures short- and medium-term price fluctuations.  
- Volatility spikes often correspond to regime shifts (e.g., supply shocks, geopolitical events).  
- Useful for identifying high-risk periods and tail events.

## 3. Momentum / Trend Features (5-day & 21-day moving averages)
- Rolling mean of returns  
- Measures short- and medium-term directional trends.  
- Persistent upward or downward trends may indicate emerging regimes.  
- Helps regression model identify directional signals beyond daily noise.


## 4. Cross-Asset Lagged Returns
-`UUP` (USD Index), `GLD` (Gold), `^VIX` (Equity volatility)  
- Incorporates previous-day signals from correlated markets.  
- USD, gold, and volatility indices are known to influence oil pricing.  
- Enhances model predictive power by capturing broader market risk dynamics.

