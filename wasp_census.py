import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


def unique_wasps(census_df):
    """Return the IDs of every wasp in the census."""
    wasps = set()
    for date, nest in census_df.iteritems():
        for wasps_on_nest in nest:
            if not pd.isna(wasps_on_nest):
                for wasp in wasps_on_nest.replace(" ", "").split(","):
                    wasps.add(wasp)
    return wasps


def wasp_interaction_count(census_df, wasp_1, wasp_2):
    """Return the number of times wasp_1 and wasp_2 are on the same nest."""
    # If wasp_1 and wasp_2 are the same wasp then its interaction count is 0
    if wasp_1 == wasp_2:
        return 0

    # Search through the census data frame and count the number of times wasp_1 and
    # wasp_2 are on the same nest
    sum = 0
    for col in census_df.columns:
        for ind in census_df.index:
            nest = census_df.at[ind, col]
            # When a nest is empty pandas represents it as NaN
            # Make sure the nest is not empty before testing if the nest contains
            # wasp_1 and wasp_2
            if not pd.isna(nest) and wasp_1 in nest and wasp_2 in nest:
                sum += 1
    return sum


def create_interaction_df(census_df):
    """Return a wasp interaction data frame using wasp census data."""
    # Get the IDs of each wasp from the census
    wasps = unique_wasps(census_df)

    # Create a new data frame (matrix) with the wasp IDs as the row and column names
    # Initialize each element in the data frame to 0
    interaction_df = pd.DataFrame(
        np.zeros((len(wasps), len(wasps)), dtype=int), index=wasps, columns=wasps,
    )

    # Iterate over the row and column names to get every possible wasp pairing
    for wasp_1 in interaction_df.columns:
        for wasp_2 in interaction_df.index:
            interaction_df.at[wasp_2, wasp_1] = wasp_interaction_count(
                census_df, wasp_1, wasp_2
            )

    return interaction_df


def save_interaction_df(interaction_df):
    interaction_df.to_csv("interaction_matrix.csv")


def plot_interaction_df(interaction_df):
    fig = go.Figure(
        data=go.Heatmap(
            z=[interaction_df.loc[row, :].values for row in interaction_df.index],
            x=interaction_df.columns,
            y=interaction_df.index,
        ),
    )
    pyo.plot(fig, filename="interaction-matrix-heatmap.html")


def days_seen_count(census_df, wasp):
    """Return the number of days the wasp was seen."""
    days_seen = 0

    # Iterate over the dates and nests
    for date in census_df.columns:
        for nest in census_df.index:
            wasps_on_nest = census_df.at[nest, date]
            # When a nest is empty pandas represents it as NaN
            # Make sure the nest is not empty before testing if the nest contains
            # the wasp
            if not pd.isna(wasps_on_nest) and wasp in wasps_on_nest:
                days_seen += 1
                break
    return days_seen


def nests_visited_count(census_df, wasp):
    """Return the number of nests the wasp visited."""
    nests_visited = 0

    # Iterate over the nests and dates
    for nest in census_df.index:
        for date in census_df.columns:
            wasps_on_nest = census_df.at[nest, date]
            # When a nest is empty pandas represents it as NaN
            # Make sure the nest is not empty before testing if the nest contains
            # the wasp
            if not pd.isna(wasps_on_nest) and wasp in wasps_on_nest:
                nests_visited += 1
                # After we've found a wasp on a particular nest, we must break out of
                # the loop iterating over each date so we don't count a nest more than
                # once
                break
    return nests_visited


def wasp_partners(census_df, wasp):
    """Return a list of all the partners the wasp has shared a nest with."""
    partners = set()

    # Iterate over the nests and dates
    for nest in census_df.index:
        for date in census_df.columns:
            wasps_on_nest = census_df.at[nest, date]
            if not pd.isna(wasps_on_nest) and wasp in wasps_on_nest:
                # Split the string of wasps on the nest "YYYY, WWWW, GGGG" into a list
                # of wasps so we can iterate over each wasp ['YYYY', 'WWWW', 'GGGG']
                for partner in wasps_on_nest.replace(" ", "").split(","):
                    if partner != wasp:
                        partners.add(partner)
    return list(partners)


def create_wasp_summary_df(census_df):
    """Return a wasp summary data frame using wasp census data."""
    # Get the IDs of each wasp from the census
    wasps = unique_wasps(census_df)

    # Create a new data frame (matrix) with the wasp IDs as the row names and
    # "Days Seen", "Nests Visited", and "Partners" as the column names
    summary_df = pd.DataFrame(
        index=wasps, columns=["Days Seen", "Nests Visited", "Partners"]
    )

    # Iterate over all the wasps
    for wasp in wasps:
        summary_df.at[wasp, summary_df.columns[0]] = days_seen_count(census_df, wasp)
        summary_df.at[wasp, summary_df.columns[1]] = nests_visited_count(
            census_df, wasp
        )
        summary_df.at[wasp, summary_df.columns[2]] = wasp_partners(census_df, wasp)

    return summary_df


def save_summary_df(summary_df):
    summary_df.to_csv("wasp_summary_matrix.csv")


if __name__ == "__main__":
    census_df = pd.read_csv("wasp_census_2019.csv", index_col=0)

    # Note: This takes a long time to calculate
    interaction_df = create_interaction_df(census_df)
    save_interaction_df(interaction_df)
    plot_interaction_df(interaction_df)

    summary_df = create_wasp_summary_df(census_df)
    save_summary_df(summary_df)
