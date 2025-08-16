"""
How much better a deal does a mortgage broker need to get to justify their fee?
"""

from src.interest_utils import *

# 1. Calculator

# 2. Sensitivity analysis
#   * vs mortgage size
#   * vs fixed term



if __name__ == '__main__':

    LOAN_AMOUNT = 137_000
    MORTGAGE_DURATION_YEARS = 20
    INTEREST_RATE_PERC = 4.2

    TARGET_FIXED_TERM_YEARS = 3
    BROKER_FEE = 500

    int_rate_broker = (
        calculate_rate_with_broker(BROKER_FEE,
                                   LOAN_AMOUNT,
                                   MORTGAGE_DURATION_YEARS,
                                   TARGET_FIXED_TERM_YEARS,
                                   INTEREST_RATE_PERC))

    print(f"The broker should provide you with a maximum interest rate of: {round(int_rate_broker, 2)}%.")
