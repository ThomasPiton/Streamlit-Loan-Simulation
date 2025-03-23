# # import streamlit as st
# from computation import Loan

# st.title("Basic Loan Calculator")

# principal = st.number_input("Loan Amount", min_value=1000, value=100000, step=1000)
# annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=5.0, step=0.1)
# term_years = st.number_input("Loan Term (years)", min_value=1, value=20, step=1)
# grace_period = st.number_input("Grace Period (months)", min_value=0, value=6, step=1)

# loan = Loan(principal, annual_rate, term_years, grace_period)
# schedule = loan.generate_amortization_schedule()

# st.subheader("Amortization Schedule")
# st.dataframe(schedule)
# st.line_chart(schedule.set_index("Month")["Balance"])
