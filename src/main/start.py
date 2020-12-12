import pandas as pd
import numpy as np
import warnings
from src.dataflow.dataflow import dataflow
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    print("The input data is loaded.")

df_orders = pd.read_csv('./data/olist_orders_dataset.csv', encoding='utf-8')
df_reviews = pd.read_csv('./data/olist_order_reviews_dataset.csv', encoding='utf-8')
df_products = pd.read_csv('./data/olist_products_dataset.csv', encoding='utf-8')
df_items = pd.read_csv('./data/olist_order_items_dataset.csv', encoding='utf-8')


merged = pd.merge(df_orders, df_items, on="order_id")
merged = pd.merge(merged, df_reviews, on="order_id")
merged = pd.merge(merged, df_products, on="product_id")

Test_Index_of_seller = 1

if __name__ == "__main__":
    print("Cluster and description for the selected seller is calculated...")


seller_class = dataflow(merged, Test_Index_of_seller)

print(seller_class)

