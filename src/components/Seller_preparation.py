import pandas as pd

def seller_preparation(orders_df:pd.DataFrame, sellernumber:int) -> list:
    """Function to select a seller by the seller_id and the index number in the dataframe.

    Parameters
    ___________
    data:pd.DataFrame
        Dataframe that contains the meta data to each specific seller.

    seller_number:int
        Integer that represents the Index of the seller that should be reviewed.

    Returns
    __________
    test:list
        List that contains the metadata of one specific seller.
    """
    seller_id = orders_df.iloc[sellernumber].name
    test = orders_df[orders_df.index == seller_id]
    return test