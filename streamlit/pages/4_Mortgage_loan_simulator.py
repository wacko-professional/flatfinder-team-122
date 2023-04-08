# import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Mortgage Loan Simulator")


st.markdown("<h1 style='color: black;'>Calculate mortgage loan</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='background-color: white; padding: 10px'>
    </div>
    """,
    unsafe_allow_html=True
)

col1, mid, col2 = st.columns([2,0.5, 3])


############# Input values ###################

# Use default values to prevent float division by zero
# https://discuss.streamlit.io/t/zerodivisionerror-float-division-by-zero-for-mathematical-calculation/16347

with col1:
    st.subheader("Loan amount")
    #loan_amount = st.number_input("Enter your loan amount($): ", format='%f', value=100000.00)
    loan_amount = st.number_input("Enter your loan amount($): ", value=100000)
    
    st.subheader("Loan tenure (Years)")
    # payment_years = st.number_input("Enter your target loan tenure (years): ", format='%d', value=30)
    payment_years = st.slider("",1 ,50, 30)
       # Loan tenure (years): 
    # min and max amount
    st.subheader("Annual Interest Rate")
    # interest_rate_annual = st.number_input("Enter your annual loan interest rate(%): ", format='%f',value=3.5)
    interest_rate_annual = st.slider("Annual loan interest rate(%): ", 0.1,10.0 ,3.5)

########### Intermediate calculations #####################
payment_months = payment_years*12
interest_rate_monthly = (interest_rate_annual / 100) / 12
upper = interest_rate_monthly*(1+interest_rate_monthly)**(payment_months)
lower = ((1+interest_rate_monthly)**(payment_months)) - 1


########### Output ###################
monthly_payment = loan_amount*(upper/lower)
total_interest = (monthly_payment * payment_months) - loan_amount

total_amount = monthly_payment * payment_months

with col2:
    st.markdown("<h3 style='color: #0066cc;'>Mortgage Payment Breakdown</h3>", unsafe_allow_html=True)
    st.subheader("**Your monthly payment:**")
    st.markdown(f"<p style='color:#0066cc; font-size: 30px;'>${round(monthly_payment, 2)}</p>",unsafe_allow_html=True)

   # st.subheader("**Your monthly payment:**\n" + "$" + (monthly_payment, format='{:,d}'))
    st.subheader("**Total interest paid:**")
    st.markdown(f"<p style='color:#0066cc; font-size: 30px;'>${round(total_interest, 2)}</p>", unsafe_allow_html=True)

    st.subheader("**Total amount you pay in " + str(payment_months) + " payments :**" )
    st.markdown(f"<p style='color:#0066cc; font-size: 30px;'>${round(total_amount, 2)}</p>", unsafe_allow_html=True)

# https://www.appsloveworld.com/coding/python3x/182/is-there-a-way-for-streamlit-user-input-to-be-formatted-automatically-as-currency