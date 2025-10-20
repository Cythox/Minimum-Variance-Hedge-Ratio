Minimum-Variance-Hedge-Ratio

A Python program to calculate the minimum variance hedge ratio and the optimal number of futures contracts using data from Yahoo Finance.

Requirements

This Python code requires the following packages:

streamlit

yfinance

pandas

numpy

matplotlib

You can install any missing packages with:

pip install streamlit yfinance pandas numpy matplotlib

Once installed, run the program with: 

streamlit run minimum_variance_hedge_ratio_5.py

It will automatically open a browser tab where you can enter the ticker symbols of the two chosen assets.
You can optionally use the Optimal Number of Futures Contracts function.
The results are displayed both numerically and graphically.

To stop the script, close the browser tab and press CTRL + C in the terminal.

----------------------------------

I came up with this project while reading chapter 3 of the book Options, Futures, and Other Derivates from John C. Hull because using Excel to calculate the minimum variance hedge ratio wasn't a satisfying solution. Firstly, I would need to prepare the data sets for usage in Excel and secondly handling many bigger data sets is quite annoying. To solve these two problems, I decided to start my first coding project — or more precisely, my first prompt-coding project.
