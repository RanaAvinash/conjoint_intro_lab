import numpy as np
import pandas as pd

def simulate_choices(tasks, n_resp=100):

    rows = []

    for r in range(n_resp):

        for task in tasks["Task"].unique():

            subset = tasks[tasks["Task"] == task]

            utilities = np.random.normal(0, 1, len(subset))

            probs = np.exp(utilities) / np.sum(np.exp(utilities))

            chosen = np.random.choice(subset.index, p=probs)

            for i, row in subset.iterrows():

                rows.append({
                    "Respondent": r,
                    "Task": task,
                    "Profile": row["Profile"],
                    "Choice": 1 if i == chosen else 0
                })

    return pd.DataFrame(rows)
