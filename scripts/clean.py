import pandas as pd
def clean_df(path):
    df = pd.read_csv(path)
    df = df.drop_duplicates()
    df = df.fillna(0)
    df.columns = df.columns.str.lower()
    print(df.isna().sum())
    return df


df_order_items = clean_df("data/processed/order_items.csv")
df_orders = clean_df("data/processed/orders.csv")
df_product_reviews = clean_df("data/processed/product_reviews.csv")
df_product_tags = clean_df("data/processed/product_tags.csv")
df_products= clean_df("data/processed/products.csv")
df_users = clean_df("data/processed/users.csv")