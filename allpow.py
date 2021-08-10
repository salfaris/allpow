import streamlit as st

st.title("🧮 All Powerful London Calculator")

st.write("This calculator helps you to estimate your monthly budget in London.")

# Income
st.subheader("💷 Source")
with st.container():
    source = st.number_input("Your source of income",
                          value=1045.0,
                          step=100.0,
                          format="%f")
    if st.button("Add source"):
        new_source = st.number_input("New source")

# Living Costs
st.subheader("🏃🏻‍♂️ Living Cost") 
with st.container():
    lc_col1, lc_col2 = st.columns(2)
    rent = lc_col1.number_input("🏠 Rent", value=600.0, step=100.0, format="%f")
    bills = lc_col2.number_input("🧾 House bills", value=30.0, step=10.0, format="%f")
    
    lc_col3, lc_col4, lc_col5, lc_col6 = st.columns(4)

    telco = lc_col3.number_input("📱 Telco", value=12.0, step=5.0, format="%f")
    groceries = lc_col4.number_input("🛒 Groceries", value=50.0, step=10.0, format="%f")
    travel = lc_col5.number_input("🚇 Transport", value=90.0, step=10.0, format="%f")
    dining = lc_col6.number_input("🍽 Dining", value=0.0, step=10.0, format="%f")
    
    lc_cost = rent + bills + telco + groceries + travel + dining

# Entertainment
st.subheader("🎈 Entertainment")
with st.container():
    st.write("A concert ticket ranges from £15 to £100 depending on popularity of the artist.")
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
        max_value=100.0, 
        value=10.0, 
        step=10.0, 
        format="%f percent", 
        help="The amount of savings in %")
    savings = source * (savings_perc/100.0)

# Sidebar
# st.sidebar.title(f"Account balance: £{source - savings - lc_cost}")
st.sidebar.subheader(f"Total monthly cost: £{lc_cost + party_cost}")
st.sidebar.subheader(f"Savings: £{savings}")
st.sidebar.success(f"Budget indicator: A+")