import pandas as pd

def calculate_importance(utilities):

    utilities["Attribute"] = utilities["Feature"].str.split("_").str[0]

    importance = utilities.groupby("Attribute")["Utility"].agg(
        lambda x: x.max()-x.min()
    )

    importance = importance / importance.sum()

    return importance.reset_index(name="Importance")
