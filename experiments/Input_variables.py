import pandas as pd
import numpy as np
import hdbscan
import warnings

warnings.filterwarnings("ignore")
def variable_selection(data):
# Select the variables that should be used
    input_data = data[
        ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_delivered_customer_date",
         "product_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty",
         "review_creation_date", "review_answer_timestamp"]]

# transforming the necessary data
# review_answer_timestamp, review_creation_date, order_purchase_timestamp, order_delivered_customer_date


def preprocessing(data):

    data.review_answer_timestamp = pd.to_datetime(data["review_answer_timestamp"])
    data.review_creation_date = pd.to_datetime(data["review_creation_date"])
    data.order_purchase_timestamp = pd.to_datetime(data["order_purchase_timestamp"])
    data.order_delivered_customer_date = pd.to_datetime(data["order_delivered_customer_date"])

    data = data.drop_duplicates()

    data.review_answer_timestamp = pd.Series(data.review_answer_timestamp).dt.round("D")
    data["delivery_duration"] = (data.order_delivered_customer_date - data.order_purchase_timestamp)
    data["answer_time"] = (data.review_answer_timestamp - data.review_creation_date)
    data = data.reset_index()
    del data["index"]
    data = data[["order_id", "customer_id", "order_status", "product_id", "seller_id", "price", "review_score",
                             "product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time"]]

    data["order_delivered"] = 0
    for i in range(len(data)):
        if data["order_status"][i] == "delivered":
            data["order_delivered"][i] = 1

    data["order_not_delivered"] = 0
    for i in range(len(data)):
        if data["order_status"][i] != "delivered":
            data["order_not_delivered"][i] = 1

    data = data[
        ["order_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty",
         "delivery_duration", "answer_time", "order_delivered", "order_not_delivered"]]
    data = data.dropna()
    data["answer_time"] = data["answer_time"].dt.days
    data["delivery_duration"] = data["delivery_duration"].dt.days

    return data


def aggregation(data):
    variables = data.groupby("seller_id").mean()

    variables["orders_handled"] = data.groupby("seller_id").count().order_id[0:]
    variables["share_of_not_delivered"] = (variables["order_not_delivered"] / (
                variables["order_not_delivered"] + variables["order_delivered"])) * 100
    variables["avg_price"] = 0
    for i in range(len(variables)):
        variables["avg_price"] = (variables["price"]) / (variables["orders_handled"])
    data = variables
    return data

#variables_full = variables.copy()



def Normalize(data):
    for i in range(len(data)):
        data[i] = (data[i] - min(data)) / (max(data) - min(data))

def normalization(data):
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
def Rescale(data):
    for i in range(len(data)):
        data[i] = abs(1 - data[i])

def rescaling(data):

    Rescale(data["delivery_duration"])
    Rescale(data["answer_time"])
    Rescale(data["order_not_delivered"])
    return data

def Input_selection(data):
    data = data[
        ["product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time", "share_of_not_delivered",
         "avg_price"]]

    return data




# Cluster 1 = Complex product sellers. With high description length and many pictures and highest average price. negative siedeffect is a high delivery_duration
# Cluster 2 = new_commers with the smallest amount of orders handeled. High focus in fast delivery and response to customer questions. Also all orders are delivered
# Cluster 3 = Low-Compley produtc seller. Low description and lowest photo quantity. Even though most orders has the least average price.

test = [np.array([401, 1, 8, 2, 0, 24])]


def approximator(processed_data, testdata):
    processed_data_npy = np.array(processed_data)

    clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.2, approx_min_span_tree=True,
                                gen_min_span_tree=False, leaf_size=35, cluster_selection_method='eom',
                                metric='euclidean', min_cluster_size=15, min_samples=10, p=None,
                                prediction_data=True).fit(processed_data_npy)

    test_labels, strengths = hdbscan.approximate_predict(clusterer, testdata)
    test_labels = test_labels[0]
    return test_labels


def seller_classifier(datapoint):
    if datapoint == -1:
        stats = "This seller belongs to cluster1"
    elif datapoint == 0:
        stats = "This seller belongs to cluster2"
    else:
        stats = "This seller belongs to cluster3"

    return print(stats)

#seller_classifier(approximator(Input_selection(rescaling(normalization(aggregation(preprocessing(input_data))))), test))
