import math
import pandas as pd
import streamlit as st

from load_css import local_css
from helpers import float_to_money, compute_rating

# NOTE :- Must be at the top!
st.set_page_config(
    page_title="All Powerful London Calculator",
    page_icon="random",
)

local_css("style.css")

DIVIDER = "---"
BIG_VERTICAL_SPACE = "####"

# Description
st.title("🧮 All Powerful London Calculator")
st.markdown(
    "This calculator helps you to estimate your **_monthly budget_** in London.")

# Income
st.subheader("💷 Source")
with st.container():
    SOURCE = st.number_input("Your source of monthly income",
                             value=1045.0,
                             step=100.0,
                             format="%f")

st.write(BIG_VERTICAL_SPACE)

# Living Costs
st.subheader("🏃🏻‍♂️ Living Cost")
with st.container():
    lc_main_col = st.columns([2, 1])
    rent = lc_main_col[0].number_input(
        "🏠 Rent", value=600.0, step=100.0, format="%f")
    bills = lc_main_col[1].number_input(
        "🧾 House bills", value=30.0, step=10.0, format="%f")

    lc_sub_col = st.columns(3)

    telco = lc_sub_col[0].number_input(
        "📱 Telco", value=12.0, step=5.0, format="%f")
    groceries = lc_sub_col[1].number_input(
        "🛒 Groceries", value=50.0, step=10.0, format="%f")

    # Transportation
    transport_cost_dict = {
        '🚇 Tube': 90.0,
        '🚌 Bus': 58.8,
        '🚴🏽 Cycling': 60.0,
        '🚶🏻‍♂️ Walking': 0.0,
    }
    mode = lc_sub_col[2].selectbox(
        label="Main mode of transport?",
        options=[key for key in transport_cost_dict.keys()],
        index=0
    )
    transport_cost = transport_cost_dict[mode]

    LIVING_COST = rent + bills + telco + groceries + transport_cost

    st.markdown(f"Total living cost: *£ {LIVING_COST:.2f}*")

# st.markdown(DIVIDER)
st.write(BIG_VERTICAL_SPACE)

# Entertainment
st.subheader("🎈 Entertainment")
with st.container():
    st.text("💡 Tip: A concert ticket ranges from £15 to £100 depending on popularity of the artist.")
    ENTERTAINMENT_COST = st.slider(
        label=r"How much do you want to party?",
        min_value=0.0,
        max_value=float(math.floor(SOURCE / 3.0 / 100.0)) * 100.0,
        value=30.0,
        step=10.0,
        format="£ %i",
        help="📝 Entertainment can be anything. It definitely include concerts, theatres, Netflix, Spotify, and the like.")
st.write(BIG_VERTICAL_SPACE)

# Savings estimate
st.subheader("🏦 Savings")

if 'savings_state_is_pct' not in st.session_state:
    st.session_state.savings_state_is_pct = True


def switch_savings_state():
    st.session_state.savings_state_is_pct = not st.session_state.savings_state_is_pct


with st.container():
    savings_state_is_pct = st.session_state.savings_state_is_pct

    if savings_state_is_pct == True:
        savings_perc = st.slider(
            label=r"What % of your income would you like to save?",
            min_value=0.0,
            max_value=40.0,
            value=10.0,
            step=5.0,
            format="%f percent",
            help="The amount of savings in %")

        SAVINGS = savings_perc / 100.0 * SOURCE

        switch_button = st.button(
            "Insert a number instead?", on_click=switch_savings_state)
    else:
        SAVINGS = st.number_input("How many £ would you like to save?",
                                  value=float(math.floor(
                                      0.1 * SOURCE / 100.0)) * 100.0,
                                  step=100.0,
                                  format="%f")

        switch_button = st.button(
            "Calculate based on percentage instead?", on_click=switch_savings_state)

    st.markdown(f"Savings amount: *£ {SAVINGS:.2f}*")

COST = LIVING_COST + ENTERTAINMENT_COST
LEFTOVER = SOURCE - COST - SAVINGS

st.markdown(BIG_VERTICAL_SPACE)
st.text("You can find your monthly budget summary at the sidebar.")

# SIDEBAR <---
st.sidebar.subheader("🤑 Monthly budget summary")

df = pd.DataFrame({
    'Income': [float_to_money(SOURCE)],
    'Living Cost': [f"({float_to_money(LIVING_COST)})"],
    'Entertainment': [f"({float_to_money(ENTERTAINMENT_COST)})"],
    'Savings': [f"({float_to_money(SAVINGS)})"],
    'Leftover': [float_to_money(LEFTOVER)],
})

st.sidebar.table(df.assign(dummy_col='£').set_index('dummy_col').T)

rating, color = compute_rating(
    SOURCE,
    COST,
    SAVINGS,
    ENTERTAINMENT_COST,
    LEFTOVER
)

indicator_text = f'''
<div class="highlight {color}">
    <span class="indicator">budget indicator:</span> <span class="indicator bold">{rating}</span>
</div>
'''

st.sidebar.markdown(indicator_text, unsafe_allow_html=True)
# ---> SIDEBAR

# <--- FOOTER
st.markdown(DIVIDER)
st.caption("Developed with ❤️ by Salman Faris")
# --> FOOTER

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
                  footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
