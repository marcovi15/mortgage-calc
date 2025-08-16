# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from src.interest_utils import calculate_rate_with_broker

st.title("Is a mortgage broker worth it?")

home_price = st.number_input("Home Price (£)", value=300000, step=500)
deposit = st.number_input("Deposit (£)", value=30000, step=1)
mortgage_duration_years = st.number_input("Mortgage term (years)", value=25, step=1)
interest_rate_perc = st.number_input("Interest rate you could get on your own (%)", value=4.5, step=0.01)
fixed_term_duration = st.number_input("Duration of fixed rate term (Years)", value=5, step=1)
broker_fee = st.number_input("Broker's fee (£)", value=500, step=1)


if st.button("Calculate"):
    loan_amount = home_price - deposit

    if loan_amount <= 0:
        st.error("Deposit must be less than the home price.")
    else:

        rate_with_broker = calculate_rate_with_broker(broker_fee,
                                                      loan_amount,
                                                      mortgage_duration_years,
                                                      fixed_term_duration,
                                                      interest_rate_perc)

        st.success(f"Interest rate a broker should get you to balance the fee: **{rate_with_broker:,.2f}%**")