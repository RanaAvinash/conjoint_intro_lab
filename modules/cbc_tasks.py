import pandas as pd
import numpy as np

def generate_choice_tasks(profiles, n_tasks=5, alts=3):

    tasks = []

    for t in range(n_tasks):

        subset = profiles.sample(alts).copy()

        subset["Task"] = t + 1

        tasks.append(subset)

    return pd.concat(tasks).reset_index(drop=True)
