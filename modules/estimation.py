import pandas as pd
import statsmodels.api as sm

def estimate_mnl(data, profiles):

    merged = data.merge(profiles,on="Profile")

    X = pd.get_dummies(
        merged.drop(columns=["Respondent","Choice","Profile"]),
        drop_first=True
    )

    y = merged["Choice"]

    model = sm.Logit(y, sm.add_constant(X))
    result = model.fit()

    utilities = pd.DataFrame({
        "Feature":X.columns,
        "Utility":result.params[1:]
    })

    return utilities
