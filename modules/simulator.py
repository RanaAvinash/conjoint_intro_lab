import numpy as np
import pandas as pd

def simulate_choices(tasks,n_resp=100):

    data=[]

    for r in range(n_resp):

        for task in tasks["Task"].unique():

            subset = tasks[tasks["Task"]==task]

            utilities = np.random.normal(0,1,len(subset))

            probs = np.exp(utilities)/np.sum(np.exp(utilities))

            choice = np.random.choice(subset["Profile"],p=probs)

            for p in subset["Profile"]:

                data.append({
                    "Respondent":r,
                    "Task":task,
                    "Profile":p,
                    "Choice":1 if p==choice else 0
                })

    return pd.DataFrame(data)
