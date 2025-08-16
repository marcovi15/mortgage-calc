
def calculate_monthly_payment(loan, duration_years, int_rate_perc):
    """
    Calculates the monthly payment during fixed term
    :param loan: Total loan amount in absolute terms
    :param duration_years: Total duration of mortgage
    :param int_rate_perc: Annual interest rate, expressed as a percentage
    :return: Fixed amount to be paid every month
    """

    duration_months = duration_years * 12
    r_factor = 1 + (int_rate_perc / 100 / 12)

    factor_one = loan * r_factor**duration_months
    factor_two = (r_factor**duration_months - 1)
    monthly_pay = factor_one / factor_two * (r_factor - 1)

    return monthly_pay


def calculate_interest_paid(loan, int_rate_perc, monthly_pay, target_term_years):
    """
    Calculates the interest paid during a given fixed term.
    :param loan: Total loan amount in absolute terms
    :param int_rate_perc: Annual interest rate, expressed as a percentage
    :param monthly_pay: Fixed amount to be paid every month
    :param target_term_years: Term during which interest rate is fixed, in years
    :return: Total amount of interest paid during the fixed term
    """

    target_term_months = target_term_years * 12
    int_rate_month = int_rate_perc / 100 / 12

    gross_interest = (loan * int_rate_month) - monthly_pay
    compound_factor = ((1 + int_rate_month)**target_term_months - 1) / int_rate_month
    paid_in_term = monthly_pay * target_term_months

    interest_paid = gross_interest * compound_factor + paid_in_term

    return interest_paid


def create_wrapper_for_interest_calc(loan, monthly_pay, target_term_months):
    """

    :param loan:
    :param monthly_pay:
    :param target_term_months:
    :return:
    """

    def wrapper_for_interest_calc(int_rate):
        return calculate_interest_paid(loan, int_rate, monthly_pay, target_term_months)

    return wrapper_for_interest_calc


def solve_by_interest_paid(interest_func, interest_target,
                           r_low=0.01, r_high=10,
                           tol_f=1e-9, tol_r=1e-12, max_iter=200):

    def eval_error(r):
        return interest_func(r) - interest_target

    f_low, f_high = eval_error(r_low), eval_error(r_high)
    # Expand the upper bound until it brackets the root (or give up)
    while f_low * f_high > 0 and r_high < 10:
        r_high *= 2
        f_high = eval_error(r_high)

    if f_low * f_high > 0:
        raise ValueError("Could not bracket a root. Check inputs/monotonicity.")

    for _ in range(max_iter):
        mid = 0.5 * (r_low + r_high)
        f_mid = eval_error(mid)
        if abs(f_mid) < tol_f or (r_high - r_low) < tol_r:
            return mid
        if f_low * f_mid <= 0:
            r_high, f_high = mid, f_mid
        else:
            r_low, f_low = mid, f_mid
    return 0.5 * (r_low + r_high)


def calculate_rate_with_broker(broker_fee, loan, duration_years, target_term_years, baseline_int_rate_perc):
    """

    :param broker_fee:
    :param loan:
    :param duration_years:
    :param target_term_years:
    :param baseline_int_rate_perc: Interest rate you could definitely get without a broker
    :return:
    """

    monthly_pay = calculate_monthly_payment(loan, duration_years, baseline_int_rate_perc)
    interest_paid_without_broker = calculate_interest_paid(loan, baseline_int_rate_perc, monthly_pay, target_term_years)

    interest_paid_with_broker = interest_paid_without_broker - broker_fee

    fixed_int_function = create_wrapper_for_interest_calc(loan, monthly_pay, target_term_years)

    max_int_rate_with_broker = solve_by_interest_paid(fixed_int_function, interest_paid_with_broker)

    return max_int_rate_with_broker
