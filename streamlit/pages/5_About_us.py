import streamlit as st


st.set_page_config(
    page_title="About Us")

# st.title("About us", anchor=None)
title_container = st.container()
col1, col2 = st.columns([1, 20])
with title_container:
    with col1:
        st.image('banner.png', width=700)
    with col2:
        st.markdown(
            """
            <div style='padding: 40px; width: 300px;'>
                <h1 style='color: white;text-align: left;'>About us</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <div style='background-color: white; padding: 10px'>
    </div>
    """,
    unsafe_allow_html=True
)


mission = '''Thank you for choosing FlatFinder. <br>

Our team consists of 6 passionate Georgia Tech OMS Analytics students who strive to improve public understanding of the 
HDB resale home market in Singapore, empowering you to make smarter choices when buying or selling a home. <br>

Using HDB resale prices data obtained from [data.gov.sg](https://data.gov.sg/) and 
[OneMap](https://www.onemap.gov.sg/docs/) from 1990 to 2022, we hope to assist users in finding a suitable HDB resale 
flat in SIngapore based on past data and forecasting future price. <br>

Our mission is to make the HDB resale data exploration process simple and straightforward for you. FlatFinder offers 
valuable insights and information to help you navigate this complex world with ease. As we are committed to improving 
your user experience and value your feedback, please take a moment to fill out our feedback form and help us make 
FlatFinder even better. With your support, we can continue to provide value to more users like you.<br>
'''
st.markdown(mission, unsafe_allow_html=True)

link = '<a href="https://docs.google.com/forms/d/e/1FAIpQLSfFoKoZfG2jTo05aiFvH3hYu_e9PRP3SkPs988VCU4UQYD47A/viewform" style="text-decoration:none; color:#0645AD;">Click here to feedback form</a>'
st.markdown(link, unsafe_allow_html=True)




st.markdown("<br>",unsafe_allow_html=True)

st.markdown(
    """
    <div style='background-color: #B7C9E2; padding: 10px'>
    </div>
    """,
    unsafe_allow_html=True
)

