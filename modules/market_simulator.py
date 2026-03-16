import numpy as np
import pandas as pd

def market_share(products, utilities):

    scores = []

    for i, row in products.iterrows():

        utility = 0

        for attr, level in row.items():

            key = f"{attr}_{level}"

            match = utilities[utilities["Feature"] == key]

            if not match.empty:
                utility += match["Utility"].values[0]

        scores.append(np.exp(utility))

    shares = np.array(scores) / np.sum(scores)

    products["MarketShare"] = shares

    return products
