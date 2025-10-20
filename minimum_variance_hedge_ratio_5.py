import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Minimum Variance Hedge Ratio", layout="centered")

st.title("📊 Minimum Variance Hedge Ratio Calculator (Percentage Changes)")

st.markdown("""
This tool computes the **minimum variance hedge ratio** (ĥ) using **percentage changes**  
and the **optimal number of futures contracts** (N*) for hedging a position.

#### Formulae:

- ĥ = $\hat{ρ}$ × ($\hat{σ}_S$ / $\hat{σ}_F$)  
- N* = (ĥ × $V_A$) / $V_F$  
  where  
  • $V_A$ = Value of the position being hedged  
  • $V_F$ = Futures price × Size of one contract  
""")

# --- User Inputs ---
col1, col2 = st.columns(2)
spot_ticker = col1.text_input("Spot Ticker (e.g. PSX)", value="PSX")
futures_ticker = col2.text_input("Futures / Correlated Asset (e.g. CL=F)", value="CL=F")

col3, col4 = st.columns(2)
start_date = col3.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = col4.date_input("End Date", pd.to_datetime("2025-10-01"))

st.divider()

# --- Inputs for futures contract calculations ---
st.subheader("📦 Optional: Optimal Number of Futures Contracts (N*)")
st.markdown("Enter these values to calculate N* (leave blank if not needed):")

col_va, col_fp, col_size = st.columns(3)
value_position = col_va.number_input("Value of Position ($V_A$)", value=None, placeholder="e.g. 1,000,000")
futures_price = col_fp.number_input("Futures Price (from market)", value=None, placeholder="e.g. 80.0")
contract_size = col_size.number_input("Size of One Futures Contract", value=None, placeholder="e.g. 1000")

st.divider()

# --- Main Calculation ---
if st.button("Calculate Hedge Ratio"):
    try:
        # Fetch data function
        def fetch_price(ticker):
            df = yf.download(ticker, start=start_date, end=end_date)
            if df.empty:
                st.error(f"No data found for {ticker}. Check spelling or date range.")
                return None
            return df["Adj Close"] if "Adj Close" in df.columns else df["Close"]

        spot = fetch_price(spot_ticker)
        futures = fetch_price(futures_ticker)

        if spot is not None and futures is not None:
            data = pd.concat([spot, futures], axis=1)
            data.columns = ["Spot", "Futures"]
            data.dropna(inplace=True)
            data["rS"] = data["Spot"].pct_change() * 100
            data["rF"] = data["Futures"].pct_change() * 100
            data.dropna(inplace=True)

            # Correlation and volatilities
            corr = np.corrcoef(data["rS"], data["rF"])[0, 1]
            sigma_s = data["rS"].std()
            sigma_f = data["rF"].std()
            h_hat = corr * (sigma_s / sigma_f)  # ĥ

            # --- Optional N* Calculation ---
            N_star = None
            if value_position and futures_price and contract_size:
                V_F = futures_price * contract_size
                N_star = (h_hat * value_position) / V_F

            # --- Display Results ---
            st.subheader("📈 Results")
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Correlation ($\hat{ρ}$)", f"{corr:.3f}")
            col_b.metric("$\hat{σ}_S$ (%)", f"{sigma_s:.3f}")
            col_c.metric("$\hat{σ}_F$ (%)", f"{sigma_f:.3f}")
            col_d.metric("ĥ (Hedge Ratio)", f"{h_hat:.3f}")

            if N_star is not None:
                st.metric("N* (Optimal # of Futures)", f"{N_star:,.2f}")

            # --- Visualization ---
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.scatter(data["rF"], data["rS"], alpha=0.6, label="Daily % Returns", s=30)
            x_vals = np.linspace(data["rF"].min(), data["rS"].max(), 100)
            ax.plot(x_vals, h_hat * x_vals, color="red", lw=2, label=f"Hedge Line (ĥ={h_hat:.3f})")
            ax.set_title(f"{spot_ticker} vs {futures_ticker} — Hedge Ratio Visualization")
            ax.set_xlabel("$\hat{r}_F$ (% Change in Futures)")
            ax.set_ylabel("$\hat{r}_S$ (% Change in Spot)")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.6)
            st.pyplot(fig)

            # --- Data Preview ---
            with st.expander("Show Recent Data"):
                st.dataframe(data.tail(10))

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
