import streamlit as st

st.title("Need Help?")

# Introduction
st.markdown("""
## Frequently Asked Questions

We've compiled answers to some of the most common questions about our loan simulation tools.
If you can't find what you're looking for, please visit our [Contact](contact) page to submit your specific question.
""")

# FAQ Accordion
with st.expander("How do I use the Basic Loan simulator?"):
    st.markdown("""
    The Basic Loan simulator allows you to calculate monthly payments and total interest for a simple loan.
    
    1. Enter the loan amount
    2. Specify the interest rate
    3. Set the loan term in years
    4. Click "Calculate" to see your results
    
    The simulator will show you monthly payment amount, total payment over the life of the loan, and total interest paid.
    """)

with st.expander("What's the difference between the Basic and Advanced Loan simulators?"):
    st.markdown("""
    **Basic Loan Simulator:**
    - Simple inputs: loan amount, interest rate, term
    - Calculates monthly payments and total interest
    - Best for straightforward loans
    
    **Advanced Loan Simulator:**
    - Additional features: down payment, insurance, taxes
    - Variable interest rates
    - Amortization schedule
    - Extra payment calculations
    - Best for mortgages and complex loans
    """)

with st.expander("How accurate are the loan simulations?"):
    st.markdown("""
    Our simulators use standard financial formulas to calculate loan payments and interest. While they provide a good estimate, the actual terms of your loan may vary based on:
    
    - Your credit score
    - The specific lender's policies
    - Additional fees or charges
    - Rounding differences
    
    We recommend using our tools for planning purposes and consulting with a financial advisor for final decisions.
    """)

with st.expander("Can I save or export my simulation results?"):
    st.markdown("""
    Yes! Each simulator has an export option that allows you to:
    
    - Download results as CSV
    - Save amortization schedules as Excel files
    - Generate a PDF summary
    
    Look for the download buttons below the simulation results.
    """)

with st.expander("I found a bug or have a feature request"):
    st.markdown("""
    We're constantly improving our tools based on user feedback. If you've found a bug or have ideas for new features:
    
    1. Visit our [Contact](contact) page
    2. Describe the issue or feature request in detail
    3. Include steps to reproduce any bugs
    4. Submit the form
    
    Our development team reviews all feedback and prioritizes updates based on user needs.
    """)

# Email support explanation
st.header("Email Support")

st.markdown("""
For questions not covered in our FAQ, we provide comprehensive email support. Here's our approach:
""")

st.info("""
### Our Email Support Process

1. **Submit your question** through our [Contact](contact) page

2. **Receive confirmation** immediately that we've received your inquiry

3. **Expert review** - Your question is routed to the appropriate specialist on our team

4. **Thorough research** - We take time to properly understand and research your specific situation

5. **Detailed response** - Within 1-2 business days, you'll receive a comprehensive email addressing your questions

6. **Follow-up support** - If our answer requires clarification or raises new questions, simply reply to continue the conversation

We believe in providing thoughtful, well-researched answers rather than rushed responses. This approach ensures you receive accurate information tailored to your specific situation.
""")

# Video tutorials section
st.header("Video Tutorials")

st.markdown("""
Our video tutorial library provides step-by-step guidance on using each of our loan simulation tools.

- [Basic Loan Simulator Tutorial](#)
- [Advanced Loan Feature Overview](#)
- [Comparing Multiple Loan Options](#)
- [Creating Loan Scenarios](#)

*(Note: In a real implementation, these would be actual links to videos)*
""")

# Contact prompt
st.markdown("""
## Still Have Questions?

If you can't find the answers you need here, please don't hesitate to [contact us](contact). 
Our team is committed to providing personalized assistance for all your loan simulation needs.
""")