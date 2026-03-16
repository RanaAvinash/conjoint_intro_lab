import pandas as pd
import numpy as np

def generate_choice_tasks(profiles,n_tasks=5,alts=3):

    tasks=[]

    for t in range(n_tasks):

        sample = profiles.sample(alts)

        sample["Task"]=t+1

        tasks.append(sample)

    return pd.concat(tasks)
