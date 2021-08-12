import math
import pandas as pd
import streamlit as st

from load_css import local_css

# NOTE :- Must be at the top!
st.set_page_config(
    page_title="All Powerful London Calculator",
    page_icon="🧮",
)

local_css("style.css")

HORIZONTAL_LINE = "---"
BIG_SPACE = "####"

# Description
st.title("🧮 All Powerful London Calculator")
st.markdown("This calculator helps you to estimate your **monthly budget** in London.")

# Income
st.subheader("💷 Source")
with st.container():
    source = st.number_input("Your source of income",
                          value=1045.0,
                          step=100.0,
                          format="%f")

st.write(BIG_SPACE)

# Living Costs
st.subheader("🏃🏻‍♂️ Living Cost") 
with st.container():
    lc_main_col = st.columns([2, 1])
    rent = lc_main_col[0].number_input("🏠 Rent", value=600.0, step=100.0, format="%f")
    bills = lc_main_col[1].number_input("🧾 House bills", value=30.0, step=10.0, format="%f")
    
    lc_sub_col = st.columns(3)
    
    telco = lc_sub_col[0].number_input("📱 Telco", value=12.0, step=5.0, format="%f")
    groceries = lc_sub_col[1].number_input("🛒 Groceries", value=50.0, step=10.0, format="%f")
    
    # Transportation
    transport_cost_dict = {
        '🚇 Tube': 90.0,
        '🚌 Bus': 58.8,
        '🚴🏽 Cycling': 60.0,
        '🚶🏻‍♂️ Walking': 0.0,
    }
    mode = lc_sub_col[2].selectbox(
        label="Mode of transport to uni?",
        options=[key for key in transport_cost_dict.keys()],
        index=0
    )
    transport_cost = transport_cost_dict[mode]
    
    living_cost = rent + bills + telco + groceries + transport_cost
    
    st.markdown(f"Total living cost: *£ {living_cost:.2f}*")

# st.markdown(HORIZONTAL_LINE)
st.write(BIG_SPACE)

# Entertainment
st.subheader("🎈 Entertainment")
with st.container():
    st.text("💡 Tip: A concert ticket ranges from £15 to £100 depending on popularity of the artist.")
    entertainment_cost = st.slider(
        label=r"How much do you want to party?",
        min_value=0.0,
        max_value=float(math.floor(source/3.0 / 100.0)) * 100.0,
        value=30.0,
        step=10.0,
        format="£ %i",
        help="📝 Entertainment can be anything. It definitely include concerts, theatres, Netflix, Spotify, and the like.")
st.write(BIG_SPACE)

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
    st.markdown(f"Savings amount: *£ {savings:.2f}*")

cost = living_cost + entertainment_cost
leftover = source - cost - savings

def float_to_money(val: float):
    return f"{val:.2f}"

def float_to_gbp(val: float):
    return f"£ {float_to_money(val)}"

st.write(HORIZONTAL_LINE)

# Budget summary
st.sidebar.subheader("🤑 Monthly budget summary")

def compute_rating():
    levered_bonus = source - (cost + savings) + 0.6*savings

    if savings > 0:
        levered_bonus_w_punishment = levered_bonus - (savings/source)*entertainment_cost
    else:
        levered_bonus_w_punishment = levered_bonus - 0.6*entertainment_cost

    bi_ratio = levered_bonus_w_punishment / source
        
    rating = None
    color = None
    if bi_ratio < 0 or leftover < 0:
        rating = "F"
        color = "F"
    elif bi_ratio > 0 and bi_ratio <= 0.047847:
        rating = "D"
        color = "D"
    elif bi_ratio > 0.047847 and bi_ratio <= 0.076555:
        rating = "C"
        color = "C"
    elif bi_ratio > 0.076555 and bi_ratio <= 0.105263:
        rating = "B"
        color = "B"
    elif bi_ratio > 0.105263 and bi_ratio <= 0.153111:
        rating = "A"
        color = "A"
    else:
        rating = "A+"
        color = "Aplus"
    
    return rating, color

df = pd.DataFrame({
    'Total cost (without savings)': [float_to_money(cost)],
    'Total cost (with savings)': [float_to_money(cost + savings)],
    'Leftover money': [float_to_money(leftover)],
})

st.sidebar.table(df.assign(dummy_col='£').set_index('dummy_col').T)
# st.subheader(f"Budget indicator: {compute_rating()}")

rating, color = compute_rating()
indicator_text = f"<div>Budget indicator: <span class='indicator highlight bold {color}'>{rating}</div>"
st.sidebar.markdown(indicator_text, unsafe_allow_html=True)