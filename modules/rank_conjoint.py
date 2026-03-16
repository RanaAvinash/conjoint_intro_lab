import pandas as pd
import statsmodels.api as sm

def estimate_rank_utilities(rank_data, design):

    data = design.copy()
    data["Rank"] = rank_data

    X = pd.get_dummies(
        data.drop(columns=["Profile","Rank"]),
        drop_first=True
    )

    y = data["Rank"]

    model = sm.OLS(y, sm.add_constant(X))
    result = model.fit()

    utilities = pd.DataFrame({
        "Feature": X.columns,
        "Utility": result.params[1:]
    })

    return utilities
