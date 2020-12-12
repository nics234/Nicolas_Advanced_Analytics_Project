
import pandas as pd
import numpy as np

from src.components.Preprocessing import feature_selection
from src.components.Aggregation_and_extraction import aggregation, normalization, rescaling, input_selection
from src.components.Seller_prediction import approximator, seller_classifier
from src.components.Seller_preparation import seller_preparation

def dataflow(orders_dataframe, seller_index:int) -> None:
    """Dataflow for clustering the sellers based on their handled orders.

    Parameters
    ----------
    orders_dataframe:list[pd.DataFrame]
        Dataframe with metadata about all the orders that the shop has processed.

    seller_index:int
        Integer that represents a seller based on his rank in the merged dataset.

    Returns
    ---------
    [Print Output]
        Print the cluster of the seller and a short description with key characteristics."""
    orders_dataframe = feature_selection(orders_dataframe)
    orders_dataframe = aggregation(orders_dataframe)
    orders_dataframe = normalization(orders_dataframe)
    orders_dataframe = rescaling(orders_dataframe)
    orders_dataframe = input_selection(orders_dataframe)
    seller_index = seller_preparation(orders_dataframe, seller_index)
    orders_dataframe = approximator(orders_dataframe, seller_index)
    orders_dataframe = seller_classifier(orders_dataframe)
    return orders_dataframe

