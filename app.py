import streamlit as st
import pandas as pd

from modules.design_generator import generate_profiles
from modules.cbc_tasks import generate_choice_tasks
from modules.simulator import simulate_choices
from modules.estimation import estimate_mnl
from modules.importance import calculate_importance
from modules.market_simulator import market_share
from modules.visualization import plot_utilities

st.title("Conjoint Analysis Teaching Lab")

st.header("1️⃣ Define Attributes")

n_attr = st.number_input("Number of Attributes",1,5,3)

attributes = {}

for i in range(n_attr):

    attr = st.text_input(f"Attribute {i+1} Name",key=f"a{i}")

    levels = st.text_input(
        f"Levels for {attr} (comma separated)",
        key=f"l{i}"
    )

    if attr and levels:
        attributes[attr] = [x.strip() for x in levels.split(",")]

st.header("2️⃣ Generate Profiles")

if st.button("Generate Profiles"):

    profiles = generate_profiles(attributes)

    st.dataframe(profiles)

    st.header("3️⃣ Choice Tasks")

    tasks = generate_choice_tasks(profiles)

    st.dataframe(tasks)

    choices=[]

    for task in tasks["Task"].unique():

        subset = tasks[tasks["Task"]==task]

        choice = st.radio(
            f"Choose preferred option for Task {task}",
            subset["Profile"].tolist()
        )

        choices.append(choice)
    importance = calculate_importance(utilities)

    st.header("Attribute Importance")

    st.dataframe(importance)
