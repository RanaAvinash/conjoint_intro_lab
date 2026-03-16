
import numpy as np
import pandas as pd

def simulate_choices(profiles, n_resp=100):

    data = []

    for r in range(n_resp):

        for i,row in profiles.iterrows():

            utility = np.random.normal()

            prob = np.exp(utility)/(1+np.exp(utility))

            choice = np.random.binomial(1,prob)

            data.append({
                "Respondent":r,
                "Profile":row["Profile"],
                "Choice":choice
            })

    return pd.DataFrame(data)
