import streamlit as st

# NOTE :- Must be at the top!
st.set_page_config(
    page_title="All Powerful London Calculator",
    page_icon="🧮",
)

HORIZONTAL_LINE = '''---'''

# Description
st.title("🧮 All Powerful London Calculator")
st.write("This calculator helps you to estimate your monthly budget in London.")

# Income
st.subheader("💷 Source")
with st.container():
    source = st.number_input("Your source of income",
                          value=1045.0,
                          step=100.0,
                          format="%f")

# Living Costs
st.subheader("🏃🏻‍♂️ Living Cost") 
with st.container():
    lc_colx, lc_coly = st.columns([2, 1])
    rent = lc_colx.number_input("🏠 Rent", value=600.0, step=100.0, format="%f")
    bills = lc_coly.number_input("🧾 House bills", value=30.0, step=10.0, format="%f")
    
    lc_col1, lc_col2, lc_col3 = st.columns(3)
    
    telco = lc_col1.number_input("📱 Telco", value=12.0, step=5.0, format="%f")
    groceries = lc_col2.number_input("🛒 Groceries", value=50.0, step=10.0, format="%f")
    
    # Transportation
    transport_cost_dict = {
        '🚇 Tube': 90.0,
        '🚌 Bus': 58.8,
        '🚴🏽 Cycling': 60.0,
        '🚶🏻‍♂️ Walking': 0.0,
    }
    mode = lc_col3.selectbox(
        label="Mode of transport to uni?",
        options=[key for key in transport_cost_dict.keys()],
        index=0
    )
    transport_cost = transport_cost_dict[mode]
    
    lc_cost = rent + bills + telco + groceries + transport_cost

st.markdown(HORIZONTAL_LINE)

# Entertainment
st.subheader("🎈 Entertainment")
with st.container():
    st.text("A concert ticket ranges from £15 to £100 depending on popularity of the artist.")
    party_cost = st.slider(
        label=r"How much do you want to party?",
        min_value=0.0, 
        max_value=source/3.0, 
        value=30.0, 
        step=10.0, 
        format="£ %i", 
        help="📝 Entertainment can be anything. It definitely include concerts, theatres, subscriptions (e.g. Netflix, Spotify), and the like.")


# Savings estimate
st.subheader("🏦 Savings")
with st.container():
    savings_perc = st.slider(
        label=r"What % of your income would like to save?",
        min_value=0.0, 
        max_value=40.0, 
        value=10.0, 
        step=5.0, 
        format="%f percent", 
        help="The amount of savings in %")
    savings = source * (savings_perc/100.0)

# Sidebar
# st.sidebar.title(f"Account balance: £{source - savings - lc_cost}")
st.sidebar.text(f"Total monthly cost: £{lc_cost + party_cost}")
st.sidebar.text(f"Monthly savings: £{savings}")
st.sidebar.success(f"Budget indicator: A+")