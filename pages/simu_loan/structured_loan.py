import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Structured Loan Simulation", layout="wide")

st.title("Structured Loan Simulation")
st.markdown("Use the tabs to simulate up to 5 structured loans.")
st.divider()

# Define tabs
loan_labels = [f"Loan {i+1}" for i in range(5)]
tabs = st.tabs(loan_labels)

# Store loan data
loans = []

# Each loan tab
for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"Parameters for {loan_labels[i]}")

        is_active = st.checkbox("Activate / Deactivate", key=f"activate_{i}")

        if is_active:
            st.success(f"{loan_labels[i]} is **activated**.")
        else:
            st.warning(f"{loan_labels[i]} is **deactivated**.")

        loan_amount = st.number_input("Loan Amount (€)", min_value=1000, max_value=10_000_000, value=100_000, step=1000, key=f"amount_{i}")
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key=f"rate_{i}")
        
        # Add repayment type selection
        repayment_type = st.selectbox(
            "Repayment Type", 
            options=["Amortizing", "Interest Only", "Bullet"],
            index=0,
            key=f"repayment_type_{i}"
        )
        
        # Duration input toggle
        use_months = st.checkbox("Express Duration in Months", key=f"use_months_{i}")

        if use_months:
            duration_months = st.number_input(
                "Loan Duration (Months)", min_value=1, max_value=600, step=1,
                value=240, key=f"duration_months_{i}"
            )
            duration_years = duration_months / 12
        else:
            duration_years = st.number_input(
                "Loan Duration (Years)", min_value=1, max_value=50, step=1,
                value=20, key=f"duration_years_{i}"
            )
            duration_months = duration_years * 12
        
        start_date = st.date_input("Start Date", key=f"start_{i}")
        assurance = st.number_input("Assurance emprunteur (% du capital)", min_value=0.0, max_value=1.0, value=0.1, step=0.01, key=f"assurance_{i}")
        frais_dossier = st.number_input("Frais de dossier (€)", min_value=0, max_value=5000, value=1000, step=100, key=f"frais_dossier_{i}")
        st.divider()

        # Store loan if activated
        if is_active and loan_amount > 0 and interest_rate > 0:
            # Calculate monthly payment based on repayment type
            monthly_rate = interest_rate / 100 / 12
            
            if repayment_type == "Amortizing":
                # Formula for amortizing loan monthly payment
                if monthly_rate > 0:
                    payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** duration_months) / ((1 + monthly_rate) ** duration_months - 1)
                else:
                    payment = loan_amount / duration_months
            elif repayment_type == "Interest Only":
                payment = loan_amount * monthly_rate
            else:  # Bullet
                payment = loan_amount * monthly_rate
            
            # Calculate assurance monthly payment
            assurance_monthly = loan_amount * assurance / 100 / 12
            total_monthly_payment = payment + assurance_monthly
            
            end_date = start_date + timedelta(days=int(duration_months * 30.4))
            
            loans.append({
                "label": loan_labels[i],
                "amount": loan_amount,
                "rate": interest_rate / 100,
                "duration_years": duration_years,
                "duration_months": duration_months,
                "start_date": start_date,
                "end_date": end_date,
                "assurance": assurance,
                "assurance_monthly": assurance_monthly,
                "frais_dossier": frais_dossier,
                "monthly_payment": payment,
                "total_monthly_payment": total_monthly_payment,
                "repayment_type": repayment_type
            })

# --- FINAL STRUCTURED LOAN PART ---
st.header("Final Structured Loan Summary")

if not loans:
    st.info("No loans are currently activated.")
    
else:
    # Weighted averages
    total_amount = sum(loan['amount'] for loan in loans)
    avg_rate = sum(loan['amount'] * loan['rate'] for loan in loans) / total_amount
    avg_duration = sum(loan['amount'] * loan['duration_years'] for loan in loans) / total_amount
    max_rate = max(loan['rate'] for loan in loans)
    min_rate = min(loan['rate'] for loan in loans)
    
    # Find max horizon (end date)
    end_dates = [loan['end_date'] for loan in loans]
    max_horizon = max(end_dates)
    min_horizon = min(loan['start_date'] for loan in loans)
    avg_horizon = min_horizon + timedelta(days=int(avg_duration * 365.25))
    
    # Find total cost of all loans
    total_cost = sum(loan['monthly_payment'] * loan['duration_months'] for loan in loans)
    total_interest = total_cost - total_amount
    
    st.subheader("🏦 Loan Profile")
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Loan Amount", f"{total_amount:,.0f} €")
        st.metric("Weighted Average Rate", f"{avg_rate * 100:.2f}%")
        st.metric("Min/Max Interest Rate", f"{min_rate * 100:.2f}% / {max_rate * 100:.2f}%")
    
    with col2:
        st.metric("Weighted Average Duration", f"{avg_duration:.2f} years")
        st.metric("Loan Start", min_horizon.strftime("%Y-%m-%d"))
        st.metric("Maximum Horizon", max_horizon.strftime("%Y-%m-%d"))
    
    with col3:
        st.metric("Total Interest Cost", f"{total_interest:,.0f} €")
        st.metric("Total Cost (Incl. Principal)", f"{total_cost:,.0f} €")
        st.metric("Total Cost Ratio", f"{total_cost/total_amount:.2f}x")

    # Create amortization tables and combine
    all_amortization = pd.DataFrame()
    loan_summaries = []
    
    # Generate a date range covering all loans
    all_dates = pd.date_range(start=min_horizon, end=max_horizon, freq='MS')  # 'MS' = month start

    for loan in loans:
        months = int(loan['duration_months'])
        monthly_rate = loan['rate'] / 12
        start = loan['start_date']
        payment = loan['monthly_payment']

        # Create date range for this loan
        loan_dates = pd.date_range(start=start, periods=months, freq='MS')
        
        # Initialize remaining balance
        remaining_balance = loan['amount']
        amortization_data = []
        
        for i, date in enumerate(loan_dates):
            interest_payment = remaining_balance * monthly_rate
            
            if loan['repayment_type'] == "Amortizing":
                principal_payment = payment - interest_payment
                remaining_balance -= principal_payment
            elif loan['repayment_type'] == "Interest Only":
                principal_payment = 0
                # No change to remaining balance
            else:  # Bullet
                if i == months - 1:  # Last payment
                    principal_payment = loan['amount']
                    remaining_balance = 0
                else:
                    principal_payment = 0
                    # No change to remaining balance
            
            total_payment = principal_payment + interest_payment + loan['assurance_monthly']
            
            amortization_data.append({
                "Date": date,
                "Loan": loan['label'],
                "Monthly Payment": payment,
                "Principal": principal_payment,
                "Interest": interest_payment,
                "Assurance": loan['assurance_monthly'],
                "Total Payment": total_payment,
                "Remaining Balance": remaining_balance
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(amortization_data)
        all_amortization = pd.concat([all_amortization, df], ignore_index=True)

        # Create loan summary
        loan_summaries.append({
            "Loan": loan['label'],
            "Monthly Payment": loan['monthly_payment'],
            "Total Principal": loan['amount'],
            "Total Interest": loan['monthly_payment'] * months - (loan['amount'] if loan['repayment_type'] != "Interest Only" and loan['repayment_type'] != "Bullet" else 0),
            "Total Assurance": loan['assurance_monthly'] * months,
            "Total Cost": loan['monthly_payment'] * months + loan['assurance_monthly'] * months + loan['frais_dossier'],
            "Cost Ratio": (loan['monthly_payment'] * months + loan['assurance_monthly'] * months + loan['frais_dossier']) / loan['amount'],
            "Repayment Type": loan['repayment_type'],
            "Start Date": loan['start_date'].strftime("%Y-%m-%d"),
            "End Date": loan['end_date'].strftime("%Y-%m-%d")
        })

    # Show individual summaries
    st.subheader("📈 Individual Loan Summaries")
    summary_df = pd.DataFrame(loan_summaries).round(2)
    st.dataframe(summary_df, use_container_width=True)

    # Show aggregate payments (grouped by date)
    st.subheader("📅 Monthly Payment Distribution")
    
    # Group by date to see aggregate payments over time
    grouped = all_amortization.groupby("Date").agg({
        "Monthly Payment": "sum",
        "Principal": "sum",
        "Interest": "sum",
        "Assurance": "sum",
        "Total Payment": "sum",
        "Remaining Balance": "sum"
    }).reset_index()
    
    # Calculate the weighted average interest rate for each month
    # This is more complex since we need to consider the remaining balance of each loan
    weighted_rates = []
    
    for date in all_dates:
        # Get loans active on this date
        active_loans = all_amortization[all_amortization["Date"] == date]
        
        if not active_loans.empty:
            # Calculate weighted average rate based on remaining balances
            total_balance = active_loans["Remaining Balance"].sum()
            if total_balance > 0:
                # Get original loan data for rates
                loan_rates = {loan['label']: loan['rate'] for loan in loans}
                weighted_rate = sum(active_loans["Remaining Balance"] * active_loans["Loan"].map(loan_rates)) / total_balance
            else:
                weighted_rate = 0
        else:
            weighted_rate = 0
            
        weighted_rates.append({
            "Date": date,
            "Weighted Rate": weighted_rate * 100  # Convert to percentage
        })
    
    weighted_rates_df = pd.DataFrame(weighted_rates)
    
    # Create tabs for different visualizations
    viz_tabs = st.tabs(["Payment Breakdown", "Interest Rates", "Remaining Balance", "Annual View"])
    
    with viz_tabs[0]:
        # Create a stacked area chart for payment components
        fig = px.area(
            grouped, 
            x="Date", 
            y=["Principal", "Interest", "Assurance"],
            title="Monthly Payment Breakdown",
            labels={"value": "Amount (€)", "variable": "Component"},
            color_discrete_map={
                "Principal": "#2E86C1",
                "Interest": "#E74C3C", 
                "Assurance": "#F39C12"
            }
        )
        fig.update_layout(height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
        
    with viz_tabs[1]:
        # Weighted average interest rate over time
        fig = px.line(
            weighted_rates_df,
            x="Date",
            y="Weighted Rate",
            title="Weighted Average Interest Rate Over Time",
            labels={"Weighted Rate": "Rate (%)", "Date": ""},
            line_shape="spline"
        )
        fig.update_layout(height=500)
        
        # Add min and max lines
        fig.add_hline(y=min_rate * 100, line_dash="dash", line_color="green", annotation_text=f"Min: {min_rate * 100:.2f}%")
        fig.add_hline(y=max_rate * 100, line_dash="dash", line_color="red", annotation_text=f"Max: {max_rate * 100:.2f}%")
        fig.add_hline(y=avg_rate * 100, line_dash="dash", line_color="blue", annotation_text=f"Avg: {avg_rate * 100:.2f}%")
        
        st.plotly_chart(fig, use_container_width=True)
        
    with viz_tabs[2]:
        # Remaining balance over time
        fig = px.line(
            grouped,
            x="Date",
            y="Remaining Balance",
            title="Total Remaining Balance Over Time",
            labels={"Remaining Balance": "Amount (€)", "Date": ""}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    with viz_tabs[3]:
        # Group by year to get annual view
        grouped['Year'] = grouped['Date'].dt.year
        annual = grouped.groupby('Year').agg({
            "Principal": "sum",
            "Interest": "sum",
            "Assurance": "sum",
            "Total Payment": "sum"
        }).reset_index()
        
        # Create bar chart for annual payments
        fig = px.bar(
            annual,
            x="Year",
            y=["Principal", "Interest", "Assurance"],
            title="Annual Payment Breakdown",
            labels={"value": "Amount (€)", "variable": "Component"},
            color_discrete_map={
                "Principal": "#2E86C1",
                "Interest": "#E74C3C", 
                "Assurance": "#F39C12"
            }
        )
        fig.update_layout(height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
        
        # Show annual data table
        st.subheader("Annual Payment Summary")
        st.dataframe(annual.round(2), use_container_width=True)

    # Detailed amortization table
    st.subheader("Amortization Details")
    with st.expander("📋 View Full Amortization Table"):
        st.dataframe(grouped.drop('Year', axis=1).round(2), use_container_width=True)

    # Final indicators
    st.subheader("Final Indicators")
    total_interest = grouped["Interest"].sum()
    total_assurance = grouped["Assurance"].sum()
    total_paid = grouped["Total Payment"].sum()
    avg_monthly_payment = grouped["Total Payment"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Interest Paid", f"{total_interest:,.0f} €")
    col2.metric("Total Assurance Paid", f"{total_assurance:,.0f} €")
    col3.metric("Total Paid Over Life", f"{total_paid:,.0f} €")
    col4.metric("Average Monthly Payment", f"{avg_monthly_payment:,.0f} €")