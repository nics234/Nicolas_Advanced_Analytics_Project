import pandas as pd
import numpy as np
import hdbscan
import warnings
warnings.filterwarnings("ignore")


# Select the variables that should be used
input_data = merged[["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_delivered_customer_date", "product_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty","review_creation_date", "review_answer_timestamp"]]

# transforming the necessary data
# review_answer_timestamp, review_creation_date, order_purchase_timestamp, order_delivered_customer_date
input_data.review_answer_timestamp = pd.to_datetime(input_data["review_answer_timestamp"])
input_data.review_creation_date = pd.to_datetime(input_data["review_creation_date"])
input_data.order_purchase_timestamp = pd.to_datetime(input_data["order_purchase_timestamp"])
input_data.order_delivered_customer_date = pd.to_datetime(input_data["order_delivered_customer_date"])

input_data = input_data.drop_duplicates()
input_data.review_answer_timestamp = pd.Series(input_data.review_answer_timestamp).dt.round("D")
input_data["delivery_duration"] = (input_data.order_delivered_customer_date - input_data.order_purchase_timestamp)
input_data["answer_time"] = (input_data.review_answer_timestamp - input_data.review_creation_date)
input_data = input_data.reset_index()
del input_data["index"]
input_data = input_data[["order_id", "customer_id", "order_status", "product_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time"]]


input_data["order_delivered"] = 0
for i in range(len(input_data)):
    if input_data["order_status"][i] == "delivered":
        input_data["order_delivered"][i] = 1

input_data["order_not_delivered"] = 0
for i in range(len(input_data)):
    if input_data["order_status"][i] != "delivered":
        input_data["order_not_delivered"][i] = 1

input_data = input_data[["order_id", "seller_id", "price", "review_score", "product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time", "order_delivered", "order_not_delivered"]]
input_data = input_data.dropna()
input_data["answer_time"] = input_data["answer_time"].dt.days
input_data["delivery_duration"] = input_data["delivery_duration"].dt.days

variables = input_data.groupby("seller_id").mean()
variables["orders_handled"] = input_data.groupby("seller_id").count().order_id[0:]
variables["share_of_not_delivered"] = (variables["order_not_delivered"]/(variables["order_not_delivered"]+variables["order_delivered"]))*100
variables["avg_price"] = 0
for i in range(len(variables)):
    variables["avg_price"] = (variables["price"])/(variables["orders_handled"])

variables_full = variables.copy()

def Normalize(data):
    for i in range(len(data)):
        data[i] = (data[i] - min(data))/(max(data)-min(data))

#Normalize(variables["avg_price"])
#Normalize(variables["review_score"])
Normalize(variables["product_description_lenght"])
Normalize(variables["product_photos_qty"])
Normalize(variables["delivery_duration"])
Normalize(variables["answer_time"])
#Normalize(variables["order_delivered"])
#Normalize(variables["order_not_delivered"])
#Normalize(variables["orders_handled"])
Normalize(variables["share_of_not_delivered"])
Normalize(variables["avg_price"])

# transform the order of the data
#for i in range(len(variables)):
#    variables["price"][i] = abs(1-variables["price"][i])
def rescale(data):
    for i in range(len(data)):
        data[i] = abs(1-data[i])

rescale(variables["delivery_duration"])
rescale(variables["answer_time"])
rescale(variables["order_not_delivered"])


variables = variables[["product_description_lenght", "product_photos_qty", "delivery_duration", "answer_time", "share_of_not_delivered", "avg_price"]]
variables_npy = np.array(variables)



clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.2, approx_min_span_tree=True,
gen_min_span_tree=False, leaf_size=35, cluster_selection_method = 'eom',
metric='euclidean', min_cluster_size=15, min_samples=10, p=None, prediction_data=True).fit(variables_npy)

output = np.array(clusterer.labels_)
output = pd.DataFrame(output)
output.columns = ["Cluster"]

variables_full["Cluster"] = 3
for i in range(len(variables_full)):
    variables_full["Cluster"][i] = output["Cluster"][i]


variables.groupby("Cluster").mean()
variables.groupby("Cluster").size()
variables_full.groupby("Cluster").mean()

Cluster1 = variables_full[variables_full["Cluster"] == -1]
Cluster2 = variables_full[variables_full["Cluster"] == 0]
Cluster3 = variables_full[variables_full["Cluster"] == 1]


# Cluster 1 = Complex product sellers. With high description length and many pictures and highest average price. negative siedeffect is a high delivery_duration
# Cluster 2 = new_commers with the smallest amount of orders handeled. High focus in fast delivery and response to customer questions. Also all orders are delivered
# Cluster 3 = Low-Compley produtc seller. Low description and lowest photo quantity. Even though most orders has the least average price.

test = [np.array([401,1,8,2,0,24])]

test_labels, strengths = hdbscan.approximate_predict(clusterer, test)
test_labels[0]



def approximator(testdata):
    test_labels, strengths = hdbscan.approximate_predict(clusterer, testdata)
    test_labels = test_labels[0]
    return test_labels

def seller_classifier(datapoint):
    if datapoint == -1:
        print("This seller probably belongs to cluster1.\nThey are selling more complex products that require a detailed product description and many pictures.\nBecause of maybe custom made solutions the products usually have a very high delivery_duration.\nNonetheless the sellers in this cluster average the moste revenue per order from all our sellers.")
    elif datapoint == 0:
        print("This seller probably belongs to cluster2.\nThis cluster is said to contain our newcomers since they have not handled many orders just yet.\nBut they are keen on delivering a pleasent customer service through short delivery times and qucik review responses.")
    else:
        print("This seller probably belongs to cluster3.\nSellers are focused on very easy, self-explanatory products. Therefore they usually keep the product description length as well as the amount of pictures relatively low.\nBecause of the basic product-design the average price is very low.\n The sellers even this out by handling more orders than other sellers.")