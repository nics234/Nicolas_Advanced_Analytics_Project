import pandas as pd

def feature_selection(orders_dataframe:pd.DataFrame) -> pd.DataFrame:
    """ Function to perform various preprocessing steps.
        The data has to be transformed to right format to enable calculations.
        Furthermore new variables are created by putting the raw variables into relation.

    Paramters
    -----------
    data:Dataframe
        Dataframe that contains the order data from the raw datasets.

    Returns
    -----------
    data:Dataframe
        Dataframe that contains a subset of the input data and also newly created variables.
    """
    orders_dataframe.review_answer_timestamp = pd.to_datetime(orders_dataframe["review_answer_timestamp"])
    orders_dataframe.review_creation_date = pd.to_datetime(orders_dataframe["review_creation_date"])
    orders_dataframe.order_purchase_timestamp = pd.to_datetime(orders_dataframe["order_purchase_timestamp"])
    orders_dataframe.order_delivered_customer_date = pd.to_datetime(orders_dataframe["order_delivered_customer_date"])

    orders_dataframe = orders_dataframe.drop_duplicates()
    orders_dataframe.review_answer_timestamp = pd.Series(orders_dataframe.review_answer_timestamp).dt.round("D")


    orders_dataframe["delivery_duration"] = (orders_dataframe.order_delivered_customer_date - orders_dataframe.order_purchase_timestamp)
    orders_dataframe["delivery_duration"] = orders_dataframe["delivery_duration"].dt.days

    orders_dataframe["answer_time"] = (orders_dataframe.review_answer_timestamp - orders_dataframe.review_creation_date)
    orders_dataframe["answer_time"] = orders_dataframe["answer_time"].dt.days

    orders_dataframe = orders_dataframe.reset_index()
    del orders_dataframe["index"]


    orders_dataframe["order_delivered"] = 0
    for i in range(len(orders_dataframe)):
        if orders_dataframe["order_status"][i] == "delivered":
            orders_dataframe["order_delivered"][i] = 1

    orders_dataframe["order_not_delivered"] = 0
    for i in range(len(orders_dataframe)):
        if orders_dataframe["order_status"][i] != "delivered":
            orders_dataframe["order_not_delivered"][i] = 1

    orders_dataframe = orders_dataframe[
        ["order_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty",
         "delivery_duration", "answer_time", "order_delivered", "order_not_delivered"]]
    orders_dataframe = orders_dataframe.dropna()



    return orders_dataframe