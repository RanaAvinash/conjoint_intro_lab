import streamlit as st
import pandas as pd

from modules.design_generator import generate_profiles
from modules.cbc_tasks import generate_choice_tasks
from modules.simulator import simulate_choices
from modules.estimation import estimate_mnl
from modules.importance import calculate_importance
from modules.market_simulator import market_share
from modules.visualization import plot_utilities
from modules.rank_conjoint import estimate_rank_utilities
from modules.rank_simulator import simulate_rank_data

st.title("Conjoint Analysis Teaching Lab")

# ------------------------------------------------
# Select Method
# ------------------------------------------------

st.sidebar.header("Conjoint Method")

method = st.sidebar.radio(
    "Select Conjoint Method",
    ["Choice Based Conjoint (CBC)", "Rank Based Conjoint"]
)

# ------------------------------------------------
# ATTRIBUTE BUILDER
# ------------------------------------------------

st.header("1️⃣ Define Attributes")

if "attributes" not in st.session_state:
    st.session_state.attributes = {}

attr_name = st.text_input("Attribute Name")

levels = st.text_input("Levels (comma separated)")

if st.button("Add Attribute"):
    if attr_name and levels:
        st.session_state.attributes[attr_name] = [
            l.strip() for l in levels.split(",")
        ]

attributes = st.session_state.attributes

st.subheader("Current Attributes")

st.write(attributes)

# ------------------------------------------------
# PROFILE GENERATION
# ------------------------------------------------

st.header("2️⃣ Generate Profiles")

if st.button("Generate Profiles") and attributes:

    profiles = generate_profiles(attributes)

    st.session_state["profiles"] = profiles

    st.subheader("Generated Profiles")

    st.dataframe(profiles)

# ------------------------------------------------
# RANK BASED CONJOINT
# ------------------------------------------------

if method == "Rank Based Conjoint":

    st.header("3️⃣ Rank Based Conjoint")

    if "profiles" in st.session_state:

        profiles = st.session_state["profiles"]

        st.subheader("Product Profiles")

        st.dataframe(profiles)

        # ------------------------------
        # Rank Data Simulation
        # ------------------------------

        st.subheader("Simulate Rank Data")

        n_resp = st.slider(
            "Number of Simulated Respondents",
            1, 500, 500
        )

        if st.button("Simulate Rank Dataset"):

            rank_data, true_utils = simulate_rank_data(
                profiles,
                n_resp
            )

            st.session_state["rank_data"] = rank_data

            st.subheader("Simulated Rank Dataset")

            st.dataframe(rank_data.head())

            st.write("True Utilities Used in Simulation")

            st.write(true_utils)

        # ------------------------------
        # Estimate Utilities
        # ------------------------------

        if "rank_data" in st.session_state:

            st.subheader("Estimate Utilities from Simulated Rankings")

            rank_data = st.session_state["rank_data"]

            mean_ranks = rank_data.groupby("Profile")["Rank"].mean()

            ranks = mean_ranks.values

            utilities = estimate_rank_utilities(ranks, profiles)

            st.session_state["utilities"] = utilities

            st.subheader("Estimated Utilities")

            st.dataframe(utilities)

            fig = plot_utilities(utilities)

            st.plotly_chart(fig)

            # ------------------------------
            # Attribute Importance
            # ------------------------------

            importance = calculate_importance(utilities)

            st.subheader("Attribute Importance")

            st.dataframe(importance)

# ------------------------------------------------
# CHOICE BASED CONJOINT
# ------------------------------------------------

if method == "Choice Based Conjoint (CBC)":

    st.header("3️⃣ Choice Tasks")

    if "profiles" in st.session_state:

        profiles = st.session_state["profiles"]

        tasks = generate_choice_tasks(profiles)

        st.session_state["tasks"] = tasks

        st.dataframe(tasks)

        responses = []

        for task in tasks["Task"].unique():

            subset = tasks[tasks["Task"] == task]

            choice = st.radio(
                f"Select preferred option for Task {task}",
                subset["Profile"].tolist(),
                key=f"task{task}"
            )

            responses.append(choice)

        # ------------------------------
        # Simulate Respondents
        # ------------------------------

        st.header("4️⃣ Simulate Respondent Data")

        n_resp = st.slider("Number of Respondents", 50, 500, 100)

        if st.button("Simulate Choice Data"):

            simulated = simulate_choices(tasks, n_resp)

            st.session_state["simulated"] = simulated

            st.subheader("Simulated Data")

            st.dataframe(simulated.head())

        # ------------------------------
        # Estimate Utilities
        # ------------------------------

        if "simulated" in st.session_state:

            st.header("5️⃣ Estimate Utilities")

            simulated = st.session_state["simulated"]

            utilities = estimate_mnl(simulated, profiles)

            st.session_state["utilities"] = utilities

            st.subheader("Estimated Utilities")

            st.dataframe(utilities)

            fig = plot_utilities(utilities)

            st.plotly_chart(fig)

            # ------------------------------
            # Attribute Importance
            # ------------------------------

            importance = calculate_importance(utilities)

            st.subheader("Attribute Importance")

            st.dataframe(importance)

# ------------------------------------------------
# MARKET SIMULATOR
# ------------------------------------------------

if "utilities" in st.session_state and attributes:

    st.header("6️⃣ Market Simulator")

    utilities = st.session_state["utilities"]

    products = []

    for i in range(3):

        st.subheader(f"Product {i+1}")

        product = {}

        for attr in attributes:

            product[attr] = st.selectbox(
                attr,
                attributes[attr],
                key=f"{attr}_{i}"
            )

        products.append(product)

    products_df = pd.DataFrame(products)

    if st.button("Simulate Market Share"):

        result = market_share(products_df, utilities)

        st.subheader("Predicted Market Share")

        st.dataframe(result)
