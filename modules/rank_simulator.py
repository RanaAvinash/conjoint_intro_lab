import numpy as np
import pandas as pd


def simulate_rank_data(profiles, n_resp=100):

    attributes = profiles.drop(columns=["Profile"]).columns

    # Generate true utilities
    true_utils = {}

    for attr in attributes:
        levels = profiles[attr].unique()
        true_utils[attr] = dict(
            zip(levels, np.random.normal(0, 1, len(levels)))
        )

    rows = []

    for r in range(n_resp):

        utilities = []

        for _, row in profiles.iterrows():

            u = 0

            for attr in attributes:
                level = row[attr]
                u += true_utils[attr][level]

            # add noise
            u += np.random.normal(0, 0.3)

            utilities.append(u)

        ranks = pd.Series(utilities).rank(ascending=False).astype(int)

        for i, profile in enumerate(profiles["Profile"]):

            rows.append({
                "Respondent": r,
                "Profile": profile,
                "Rank": ranks[i]
            })

    df = pd.DataFrame(rows)

    return df, true_utils
