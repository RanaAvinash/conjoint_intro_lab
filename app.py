import streamlit as st
import pandas as pd

from modules.design_generator import generate_profiles
from modules.rank_conjoint import estimate_rank_utilities
from modules.cbc_conjoint import simulate_choices
from modules.estimation import estimate_mnl
from modules.visualization import plot_utilities

st.title("Conjoint Analysis Teaching Lab")

method = st.sidebar.radio(
"Select Conjoint Method",
["Rank-Based Conjoint","Choice-Based Conjoint"]
)

st.sidebar.header("Define Attributes")

price = st.sidebar.multiselect("Price",["10","15","20"])
brand = st.sidebar.multiselect("Brand",["A","B","C"])
battery = st.sidebar.multiselect("Battery",["8h","12h","20h"])

attributes = {
"Price":price,
"Brand":brand,
"Battery":battery
}

if st.button("Generate Profiles"):

    profiles = generate_profiles(attributes)

    st.subheader("Product Profiles")

    st.dataframe(profiles)

    if method=="Rank-Based Conjoint":

        st.subheader("Rank Profiles")

        ranks=[]

        for i in profiles["Profile"]:

            r=st.number_input(
                f"Rank for Profile {i}",
                min_value=1,
                max_value=len(profiles),
                value=i
            )

            ranks.append(r)

        if st.button("Estimate Utilities"):

            utilities=estimate_rank_utilities(ranks,profiles)

            st.dataframe(utilities)

            fig=plot_utilities(utilities)

            st.plotly_chart(fig)

    if method=="Choice-Based Conjoint":

        respondents=st.slider(
            "Number of Respondents",
            50,500,100
        )

        data=simulate_choices(profiles,respondents)

        st.subheader("Simulated Choice Data")

        st.dataframe(data.head())

        utilities=estimate_mnl(data,profiles)

        st.subheader("Estimated Utilities")

        st.dataframe(utilities)

        fig=plot_utilities(utilities)

        st.plotly_chart(fig)
