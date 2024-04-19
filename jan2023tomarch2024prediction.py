import pandas as pd
import yfinance as yf
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"

# Define the tickers for Apple and Google
apple_ticker = 'AAPL'
google_ticker = 'GOOGL'

# Define starting and ending dates
start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2024-03-31')

# Loop through each quarter
for quarter in pd.date_range(start_date, end_date, freq='QS'):
  # Define quarter specific dates
  quarter_start = quarter
  quarter_end = quarter + pd.DateOffset(months=2, days=31)  # Adjust for max days in a month

  # Fetch historical stock price data using yfinance
  apple_data = yf.download(apple_ticker, start=quarter_start, end=quarter_end)
  google_data = yf.download(google_ticker, start=quarter_start, end=quarter_end)

  # Calculate daily returns
  apple_data['Daily_Return'] = apple_data['Adj Close'].pct_change()
  google_data['Daily_Return'] = google_data['Adj Close'].pct_change()

  # Create figures for Daily Returns, Cumulative Returns, and Volatility

  # Daily Returns
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=apple_data.index, y=apple_data['Daily_Return'],
                          mode='lines', name='Apple', line=dict(color='blue')))
  fig.add_trace(go.Scatter(x=google_data.index, y=google_data['Daily_Return'],
                          mode='lines', name='Google', line=dict(color='green')))

  fig.update_layout(title=f'Daily Returns for Apple and Google ({quarter_start.strftime("%Y-%m-%d")} - {quarter_end.strftime("%Y-%m-%d")})',
                    xaxis_title='Date', yaxis_title='Daily Return',
                    legend=dict(x=0.02, y=0.95))
  # Display the figure (replace with your preferred saving method)
  fig.show()  # Use fig.show() to display the figure

 # Cumulative Returns
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=apple_data.index, y=(apple_data['Adj Close'] / apple_data['Adj Close'].iloc[0]) - 1,
                          mode='lines', name='Apple (Cumulative)', line=dict(color='blue')))
  fig.add_trace(go.Scatter(x=google_data.index, y=(google_data['Adj Close'] / google_data['Adj Close'].iloc[0]) - 1,
                          mode='lines', name='Google (Cumulative)', line=dict(color='green')))

  fig.update_layout(title=f'Cumulative Returns for Apple and Google ({quarter_start.strftime("%Y-%m-%d")} - {quarter_end.strftime("%Y-%m-%d")})',
                    xaxis_title='Date', yaxis_title='Cumulative Return (%',
                    legend=dict(x=0.02, y=0.95))
  fig.show()  # Display the Cumulative Returns figure

  # Volatility
  fig1 = go.Figure()
  fig1.add_bar(x=['Apple', 'Google'], y=[apple_data['Daily_Return'].std(), google_data['Daily_Return'].std()],
                text=[f'{apple_data["Daily_Return"].std():.4f}', f'{google_data["Daily_Return"].std():.4f}'],
                textposition='auto', marker=dict(color=['blue', 'green']))
  fig1.update_layout(title=f'Volatility Comparison ({quarter_start.strftime("%Y-%m-%d")} - {quarter_end.strftime("%Y-%m-%d")})',
                    xaxis_title='Stock', yaxis_title='Volatility (Standard Deviation)',
                    bargap=0.5)
  fig1.show()  # Use fig.show() to display the figure

  # Market Benchmark
  market_data = yf.download('^GSPC', start=quarter_start, end=quarter_end)

  # Calculate daily returns for all
  apple_data['Daily_Return'] = apple_data['Adj Close'].pct_change()
  google_data['Daily_Return'] = google_data['Adj Close'].pct_change()
  market_data['Daily_Return'] = market_data['Adj Close'].pct_change()

  # Calculate Beta for Apple and Google
  cov_apple = apple_data['Daily_Return'].cov(market_data['Daily_Return'])
  var_market = market_data['Daily_Return'].var()
  beta_apple = cov_apple / var_market

  cov_google = google_data['Daily_Return'].cov(market_data['Daily_Return'])
  beta_google = cov_google / var_market

  # Print Beta for this quarter
  print(f"Beta for Apple ({quarter_start.strftime('%Y-%m-%d')} - {quarter_end.strftime('%Y-%m-%d')}):", beta_apple)
  print(f"Beta for Google ({quarter_start.strftime('%Y-%m-%d')} - {quarter_end.strftime('%Y-%m-%d')}):", beta_google)
  print("-" * 20)  # Optional separator for clarity

