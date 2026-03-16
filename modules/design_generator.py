import itertools
import pandas as pd
from itertools import product
def generate_profiles(attributes: dict) -> pd.DataFrame:
    """
    Generate full factorial profiles
    """
    keys = list(attributes.keys())
    values = list(attributes.values())

    combinations = list(itertools.product(*values))

    df = pd.DataFrame(combinations, columns=keys)
    df["Profile"] = range(1, len(df)+1)
    combinations = list(product(*values))
    return df
