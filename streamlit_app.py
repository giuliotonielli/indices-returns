import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("# Stock Market Returns")

"""
The crucial question many investors ask themselves is whether the stock market really returns an average of 7/8% per year. The scope of this short article is to try to provide an answer to that question. Of course, the answer won't be a precise percentage, as stock market returns may depend on the time period and index composition (tech stocks vs value stocks, developed countries stocks vs emerging countries stocks etc.).

A frequency distribution graph of 3 different indices will be provided, so that the reader can understand what returns to expect from the market. My initial idea was to provide a comparison with their correspondant ETFs as well. However, the main problem I encountered was the fact that most ETFs are relatively new. The only ETF that has a track record long enough is $SPY, which was created in 1993. ETFs tracking countries outside of the US are, at most, 15 years old (not enough data in my opinion). 

The only three differences in returns that we can expect between an index and an ETF are:
- dividends being reinvested if the ETF decides to follow an accumulation strategy
- a tracking error
- the Total Expense Ratio of the ETF 

I will analyze three indices and one of their correspondant ETFs:
- S&P500 index - $SPY etf for the US market
- Nikkei 225 (Japan)
- Ftse 100 (United Kingdom)

I chose those indices for the following reasons:
- Medium to long history
- Inflation data available (most developing countries, such as China, have a relatively short inflation track record, and they may even fake some of the data :0)

And now, let's get started!
"""
# UNITED KINGDOM
# NOTA IMPO: PER DIVIDENDI VECCHI, NON TROVABILI ONINE, SI è USATA LA MEDIA DI QUELLI + RECENTI

st.write("# FTSE 100 (United Kingdom) Stats:")
st.write()
st.write("Important: missing dividend yield values have been filled with the average of available values")

# Read return data from the first txt file
return_data = pd.read_csv("ftse.txt", sep=" ", names=["Year", "Return"], skiprows=1)

# DIVIDENDS
dividend_yield_data = pd.read_csv("dividends_ftse.txt", sep="\t", header=None, usecols=[0,1], names=["Year", "Dividend_Yield_1"])
dividend_yield_data["Dividend_Yield_1"] = dividend_yield_data["Dividend_Yield_1"].str.rstrip('%').astype(float)
merged_data = return_data.merge(dividend_yield_data, left_on="Year", right_on="Year", how="left")

# Fill missing dividend yield values with the average of available values
dividend_mean = dividend_yield_data["Dividend_Yield_1"].mean()
merged_data["Dividend_Yield_1"] = merged_data["Dividend_Yield_1"].fillna(dividend_mean)

merged_data["Return_Adjusted_to_Dividends"] = merged_data["Return"] + merged_data["Dividend_Yield_1"]

# INFLATION
inflation_data = pd.read_csv("UK_inflation.txt", sep="\t", header=None, usecols=[0,1], names=["Year", "Inflation"])
inflation_data["Inflation"] = inflation_data["Inflation"].str.rstrip('%').astype(float)
merged_data = merged_data.merge(inflation_data, left_on="Year", right_on="Year", how="left")

merged_data["Return_Adjusted_to_Inflation"] = merged_data["Return"] - merged_data["Inflation"]

# BOTH
merged_data["Return_Adjusted_to_Both"] = merged_data["Return"]  + merged_data["Dividend_Yield_1"] - merged_data["Inflation"]

plt.figure(figsize=(16, 6))

# Plot return distribution with inflation adjustment
plt.subplot(1, 2, 1)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Inflation"], bins=25, color='darkred', alpha=0.5, label='With Inflation')
plt.title('Return Distribution With Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

# Plot return distribution with dividends and inflation adjusted
plt.subplot(1, 2, 2)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Both"], bins=25, color='blue', alpha=0.5, label='With Dividends and Inflation')
plt.title('Return Distribution With Dividends and Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

stats_pure = merged_data["Return"].describe()
stats_both = merged_data["Return_Adjusted_to_Both"].describe()

st.write(merged_data)
st.write()
st.write("Statistics for pure Returns:")
st.write(round(stats_pure,2))
st.write()
st.write("Statistics for Returns with Dividends and Inflation Adjustment:")
st.write(round(stats_both,2))

plt.tight_layout()
st.pyplot(plt.gcf())

# JAPAN
st.write("# Nikkei 225 (Japan) Stats:")
st.write()
st.write("Important: no dividend yield historical data has been found, average dividend yield of the last 30 years has been used (1.4%)")

# IMPORTANTE: DATI SUI DIVIDENDI ANNO PER ANNO INTROVABILI, NEL CONSIDERARLI USO LA % MEDIA DEGLI ULTIMI 30 ANNI:
avg_dividend = 1.4

# Read return data from the Nikkei file
return_data_nikkei = pd.read_csv("nikkei.txt", sep="\t", header=None, usecols=[0,1], names=["Year", "Return"])
return_data_nikkei["Return"] = return_data_nikkei["Return"].str.rstrip('%').astype(float)

# INFLATION
inflation_data = pd.read_csv("Japan_inflation.txt", sep="\t", header=None, usecols=[0,1], names=["Year", "Inflation"])
inflation_data["Inflation"] = inflation_data["Inflation"].str.rstrip('%').astype(float)
merged_data = return_data_nikkei.merge(inflation_data, left_on="Year", right_on="Year", how="left")

merged_data["Return_Adjusted_to_Inflation"] = merged_data["Return"] - merged_data["Inflation"]

# BOTH
merged_data["Return_Adjusted_to_Both"] = merged_data["Return_Adjusted_to_Inflation"] + avg_dividend 


plt.figure(figsize=(16, 6))

# Plot return distribution with inflation adjustment
plt.subplot(1, 2, 1)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Inflation"], bins=25, color='darkred', alpha=0.5, label='With Inflation')
plt.title('Return Distribution With Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

# Plot return distribution with dividends and inflation adjusted
plt.subplot(1, 2, 2)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Both"], bins=25, color='blue', alpha=0.5, label='With Dividends and Inflation')
plt.title('Return Distribution With Dividends and Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

stats_pure = merged_data["Return"].describe()
stats_both = merged_data["Return_Adjusted_to_Both"].describe()

st.write(merged_data)
st.write()
st.write("Statistics for pure Returns:")
st.write(round(stats_pure,2))
st.write()
st.write("Statistics for Returns with Dividends and Inflation Adjustment:")
st.write(round(stats_both,2))

plt.tight_layout()
st.pyplot(plt.gcf())

# UNITED STATES

st.write("# S&P 500 (United States) Stats:")
st.write()
st.write("Important: missing dividend yield values have been filled with the average of available values")

# NOTA IMPO: PER DIVIDENDI VECCHI, NON TROVABILI ONINE, SI è USATA LA MEDIA DI QUELLI + RECENTI

# Read return data from the first txt file
return_data = pd.read_csv("sp500.txt", sep=",", names=["Year", "Return"], skiprows=1)

# DIVIDENDS
dividend_yield_data = pd.read_csv("sp500_dividends.txt", sep="\t", header=None, usecols=[0,2], names=["Year", "Dividend_Yield"])
dividend_yield_data["Dividend_Yield"] = dividend_yield_data["Dividend_Yield"].str.rstrip('%').astype(float)

merged_data = return_data.merge(dividend_yield_data, left_on="Year", right_on="Year", how="left")

# Fill missing dividend yield values with the average of available values
dividend_mean = dividend_yield_data["Dividend_Yield"].mean()
merged_data["Dividend_Yield"] = merged_data["Dividend_Yield"].fillna(dividend_mean)

merged_data["Return_Adjusted_to_Dividends"] = merged_data["Return"] + merged_data["Dividend_Yield"]

# INFLATION
inflation_data = pd.read_csv("US_inflation.txt", sep="\t", header=None, usecols=[0,1], names=["Year", "Inflation"])
#inflation_data["Inflation"] = inflation_data["Inflation"].astype(float)
merged_data = merged_data.merge(inflation_data, left_on="Year", right_on="Year", how="left")

merged_data["Return_Adjusted_to_Inflation"] = merged_data["Return"] - merged_data["Inflation"]

# BOTH
merged_data["Return_Adjusted_to_Both"] = merged_data["Return"]  + merged_data["Dividend_Yield"] - merged_data["Inflation"]

plt.figure(figsize=(16, 6))

# Plot return distribution with inflation adjustment
plt.subplot(1, 2, 1)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Inflation"], bins=25, color='darkred', alpha=0.5, label='With Inflation')
plt.title('Return Distribution With Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

# Plot return distribution with dividends and inflation adjusted
plt.subplot(1, 2, 2)
plt.hist(merged_data["Return"], bins=25, color='gray', alpha=0.5, label='No Adjustments')
plt.hist(merged_data["Return_Adjusted_to_Both"], bins=25, color='blue', alpha=0.5, label='With Dividends and Inflation')
plt.title('Return Distribution With Dividends and Inflation Adjustment')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()

stats_pure = merged_data["Return"].describe()
stats_both = merged_data["Return_Adjusted_to_Both"].describe()

st.write(merged_data)
st.write()
st.write("Statistics for pure Returns:")
st.write(round(stats_pure,2))
st.write()
st.write("Statistics for Returns with Dividends and Inflation Adjustment:")
st.write(round(stats_both,2))

plt.tight_layout()
st.pyplot(plt.gcf())
