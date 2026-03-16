import pandas as pd
import statsmodels.api as sm


def estimate_mnl(data, profiles):

    # merge design with simulated choices
    merged = data.merge(profiles, on="Profile")

    # create dummy variables
    X = pd.get_dummies(
        merged.drop(columns=["Respondent", "Task", "Choice", "Profile"]),
        drop_first=True
    )

    # ensure numeric
    X = X.astype(float)

    y = merged["Choice"].astype(int)

    # check if both classes exist
    if y.nunique() < 2:
        raise ValueError(
            "Choice variable contains only one class. "
            "Increase respondents or regenerate simulation."
        )

    # add constant
    X = sm.add_constant(X)

    # estimate model
    model = sm.Logit(y, X)

    result = model.fit(disp=False)

    utilities = pd.DataFrame({
        "Feature": X.columns[1:],   # exclude constant
        "Utility": result.params[1:]
    })

    return utilities
