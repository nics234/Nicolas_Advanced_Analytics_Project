import pandas as pd
def aggregation(extracted_order_df:pd.DataFrame) -> pd.DataFrame:
    """ Aggregation of the orders to recieve the average values for each seller.


    Parameters
    ____________
    data:Dataframe
        Dataframe that contains metadata about the orders.

    Returns
    ___________
    data:Dataframe
        Dataframe that contains aggregated information about each seller."""
    variables = extracted_order_df.groupby("seller_id").mean()

    variables["orders_handled"] = extracted_order_df.groupby("seller_id").count().order_id[0:]
    variables["share_of_not_delivered"] = (variables["order_not_delivered"] / (
                variables["order_not_delivered"] + variables["order_delivered"])) * 100
    variables["avg_price"] = 0
    for i in range(len(variables)):
        variables["avg_price"] = (variables["price"]) / (variables["orders_handled"])

    extracted_order_df = variables
    return extracted_order_df


def Normalize(data:pd.Series) -> pd.Series:
    """ Function for the normalization of a Series. The specific values are normalized according
        to the relative position they obtain.

    Parameters
    __________
    data:pd.Series
        Series that represents a whole column of a dataframe.

    Returns
    ___________
    data:pd.Series
        Series that represents the normalized values for a whole column of a dataframe"""
    for i in range(len(data)):
        data[i] = (data[i] - min(data)) / (max(data) - min(data))
    return data

def normalization(data:pd.DataFrame) -> pd.DataFrame:
    """ Function that normalizes specific columns of a dataframe and replaces the actual values with the normalized ones.

    Parameters
    ____________
    data:Dataframe
        Dataframe that contains the aggregated information about the sellers.

    Returns
    ___________
    data:Dataframe
        Dataframe that contains contains normalized values."""

    Normalize(data["product_description_lenght"])
    Normalize(data["product_photos_qty"])
    Normalize(data["delivery_duration"])
    Normalize(data["answer_time"])
    Normalize(data["share_of_not_delivered"])
    Normalize(data["avg_price"])
    return data


# transform the order of the data
# for i in range(len(variables)):
#    variables["price"][i] = abs(1-variables["price"][i])

def Rescale(data:pd.Series) -> pd.Series:
    """ Function that takes the normalized values of a variable and flips their order.
        After this process previously high Values are now small and vice versa.

    Parameters
    ____________
    data:pd.Series
        Series, or a dataframe column respectively, that contains the normalized value of a variable.

    Returns
    ____________
    data:pd.Series
        Series that now contains the normalized variable with the flipped order of values."""
    for i in range(len(data)):
        data[i] = abs(1 - data[i])
    return data

def rescaling(normalized_order_df:pd.DataFrame) ->pd.DataFrame:
    """ Function that flips the order of specific dataframe columns.

    Parameters
    _____________
    data:Dataframe
        Dataframe that contains the normalized values of important variables.

    Returns
    data:Dataframe
        Dataframe that contains the normalized values of important variables, where the order of the
        values is flipped, when necessary."""

    Rescale(normalized_order_df["delivery_duration"])
    Rescale(normalized_order_df["answer_time"])
    Rescale(normalized_order_df["order_not_delivered"])
    return normalized_order_df

def input_selection(preprocessed_order_df:pd.DataFrame) -> pd.DataFrame:
    """ Function that selects the key values from a datafram, on which the clustering shall be performed.

    Parameters
    ____________
    data:Dataframe
        Dataframe that contains the now aggregated, normalized and rescaled values that are interestig
        for the cluster analysis.

    Returns
    data:Dataframe
        Dataframe that now only contains the necessary 6 variables on which the clustering will be performed."""
    preprocessed_order_df = preprocessed_order_df[
        ["product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time", "share_of_not_delivered",
         "avg_price"]]

    return preprocessed_order_df