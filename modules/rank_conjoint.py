import pandas as pd
import statsmodels.api as sm


def estimate_rank_utilities(ranks, profiles):

    df = profiles.copy()

    df["Rank"] = ranks

    X = pd.get_dummies(
        df.drop(columns=["Profile", "Rank"]),
        drop_first=True
    )

    X = X.astype(float)

    y = df["Rank"].astype(float)

    X = sm.add_constant(X)

    model = sm.OLS(y, X)

    result = model.fit()

    utilities = pd.DataFrame({
        "Feature": X.columns[1:],
        "Utility": result.params[1:]
    })

    return utilities
