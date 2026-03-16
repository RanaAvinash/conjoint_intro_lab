import plotly.express as px

def plot_utilities(utilities):

    fig = px.bar(
        utilities,
        x="Feature",
        y="Utility",
        title="Part-worth Utilities"
    )

    return fig
