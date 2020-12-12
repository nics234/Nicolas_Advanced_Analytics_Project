import pandas as pd
import numpy as np
import data
df_orders = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_orders_dataset.csv")


df_reviews = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_order_reviews_dataset.csv")

df_products = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_products_dataset.csv")

df_payment = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_order_payments_dataset.csv")

df_customers = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_customers_dataset.csv")

df_items = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_order_items_dataset.csv")

df_sellers = pd.read_csv(r"/Users/Nicolas/Desktop/Masterstudium /Semester 5/Advanced Analytics/Dataset/archive/olist_sellers_dataset.csv")



merged = pd.merge(df_orders, df_customers, on="customer_id")
merged = pd.merge(merged, df_items, on = "order_id")
merged = pd.merge(merged, df_sellers, on="seller_id")
merged = pd.merge(merged, df_payment, on="order_id")
merged = pd.merge(merged, df_reviews, on="order_id")
merged = pd.merge(merged, df_products, on="product_id")

#avg_pay_sum = 154.10038041699553
pay_types = df_payment.groupby("payment_type").count()
customer_states = df_customers.groupby("customer_state").count()

#avg_review_score = 4.07089
df_reviews.review_score.mean()

# Potentiell interessante Spalten:
# order_id, order_status, diff(order_purchase_tmsp & order_delievered_customer_date')
# diff(order_estimated_delivery_date & order_delievered_customer_date)
# review_score, order_status, price
merged6.columns

# order_count by state:
# 71% aller Bestellungen sind alleine aus dem Bundesstaat Sao Paulo
test2 = merged6.groupby("seller_state").count()
test2 = test2["order_id"].sort_values()
test2[-1]/test2.sum()
# In Sao Paulo gibt es 1.849 verschiedene Seller
SP = merged6[merged6["seller_state"]=="SP"]
len(SP.seller_id.unique())


seller_scores = merged6.groupby("seller_id").review_score.mean().sort_values()
sales_size = merged6.groupby("seller_id").count()
sales_size = sales_size["order_id"]
seller_data = pd.merge(seller_scores, sales_size, on = "seller_id")
seller_data.columns = ["review_score","frequency"]
seller_data.mean()
seller_data[seller_data["frequency"] > 10].mean()
seller_revenue = merged6.groupby("seller_id").sum()["price"]
seller_data = pd.merge(seller_data, seller_revenue, on = "seller_id")
seller_data.columns = ["review_score", "frequency", "revenue"]
seller_data["price_per_order"] = (seller_data.revenue/seller_data.frequency)

# Da der p-value des Tests kleiner als 0.05 ist muss angenommen werden,
# die schwache Korrelation von - 0.03 auch schwach signifikant ist. -->
# Keine Aussagekraft.
from scipy.stats import pearsonr
pearsonr(seller_data.review_score, seller_data.price_per_order)

status_review = merged6[["order_id", "order_status", "review_score"]]
status_review.groupby("order_status").mean()
status_review.groupby("order_status").count()

delivered = merged6[merged6["order_status"]=="delivered"]
not_delivered = status_review[status_review["order_status"] != "delivered"]
# Means delivered = 4,1 - not_delivered = 1.7

#  50665 reviews wurden beschrieben
len(merged6)-sum(merged6.review_comment_message.isna())

# Idee:
# Scoring-modell für die Lieferanten bauen zur Auswahl welche Lieferanten
# beibehalten bleiben sollen und welche gekickt werden sollen.
# Target = Selbst entwickelter Seller score
# metrics = price, review_score, delay_post, order_size, payment_type, product_description_type_length,
# share of not delivered orders, difference between review creation and answer, product_photos_qty
