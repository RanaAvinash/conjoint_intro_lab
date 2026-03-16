import pandas as pd

def calculate_importance(utilities):

    utilities["Attribute"] = utilities["Feature"].apply(
        lambda x: x.split("_")[0]
    )

    importance = utilities.groupby("Attribute")["Utility"].agg(
        lambda x: x.max() - x.min()
    )

    importance = importance / importance.sum()

    return importance.reset_index(name="Importance")
