import itertools
import pandas as pd

def generate_profiles(attributes):

    keys = attributes.keys()
    values = attributes.values()

    combos = list(itertools.product(*values))

    df = pd.DataFrame(combos,columns=keys)

    df["Profile"] = range(1,len(df)+1)

    return df
