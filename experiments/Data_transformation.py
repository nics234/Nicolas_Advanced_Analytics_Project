import pandas as pd

def data_merging():
    df_orders = pd.read_csv('./data/olist_orders_dataset.csv', encoding='utf-8')
    df_reviews = pd.read_csv('./data/olist_order_reviews_dataset.csv', encoding='utf-8')
    df_products = pd.read_csv('./data/olist_products_dataset.csv', encoding='utf-8')
    df_payment = pd.read_csv('./data/olist_order_payments_dataset.csv', encoding='utf-8')
    df_customers = pd.read_csv('./data/olist_customers_dataset.csv', encoding='utf-8')
    df_items = pd.read_csv('./data/olist_order_items_dataset.csv', encoding='utf-8')
    df_sellers = pd.read_csv('./data/olist_sellers_dataset.csv', encoding='utf-8')

    merged = pd.merge(df_orders, df_customers, on="customer_id")
    merged2 = pd.merge(merged, df_items, on = "order_id")
    merged3 = pd.merge(merged2, df_sellers, on="seller_id")
    merged4 = pd.merge(merged3, df_payment, on="order_id")
    merged5 = pd.merge(merged4, df_reviews, on="order_id")
    merged6 = pd.merge(merged5, df_products, on="product_id")

    return merged6