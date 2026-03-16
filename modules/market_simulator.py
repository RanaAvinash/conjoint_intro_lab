import numpy as np
import pandas as pd

def simulate_market(products, utilities):

    scores = []

    for i,row in products.iterrows():

        u = 0

        for feature,value in row.items():

            key = f"{feature}_{value}"

            if key in utilities["Feature"].values:

                u += utilities.loc[
                    utilities["Feature"]==key,"Utility"
                ].values[0]

        scores.append(np.exp(u))

    total = sum(scores)

    shares = [s/total for s in scores]

    products["MarketShare"] = shares

    return products

import numpy as np
import pandas as pd

def market_share(products,utilities):

    scores=[]

    for i,row in products.iterrows():

        u=0

        for col,val in row.items():

            key=f"{col}_{val}"

            match=utilities[utilities["Feature"]==key]

            if not match.empty:

                u+=match["Utility"].values[0]

        scores.append(np.exp(u))

    total=sum(scores)

    shares=[s/total for s in scores]

    products["Share"]=shares

    return products
