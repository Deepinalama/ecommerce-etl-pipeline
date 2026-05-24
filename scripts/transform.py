import pandas as pd
import json
#carts
with open("data/raw/carts.json") as f:
    carts_data = json.load(f)

#orderitems
df_order_items = pd.json_normalize(
    carts_data['carts'],
    record_path='products',
    meta=['id', 'userId'],
    meta_prefix='cart_',
    sep="_"
)

df_order_items.rename(columns={
    'id': 'product_id',
    'cart_id':'cart_id',
    'cart_userId': 'user_id',
}, inplace=True)

#orders
df_order = pd.json_normalize(carts_data['carts'])
df_order = df_order.drop(columns=['products'])

df_order.rename(columns={
    'id': 'cart_id',
    'userId': 'user_id'
}, inplace=True)

#products
with open("data/raw/products.json") as f:
    products_data = json.load(f)
products = products_data['products']

#productstable
df_products = pd.json_normalize(products, sep="_")

df_products = df_products[[
    'id', 'title', 'category', 'brand', 'stock',
    'dimensions_width', 'dimensions_height', 'dimensions_depth'
]]

df_products.rename(columns={
    'id': 'product_id'
}, inplace=True)

#productreview
df_product_reviews = pd.json_normalize(
    products,
    record_path='reviews',
    meta=['id']
)

df_product_reviews.rename(columns={
    'id': 'product_id'
}, inplace=True)

#producttag
tags_list = []

for product in products:
    for tag in product['tags']:
        tags_list.append({
            'product_id': product['id'],
            'tag': tag
        })

df_product_tags = pd.DataFrame(tags_list)

#user
with open("data/raw/users.json") as f:
    users_data = json.load(f)

df_users = pd.json_normalize(users_data['users'], sep="_")


print(df_order.head())
print(df_order_items.head())
print(df_products.head())
print(df_product_reviews.head())
print(df_product_tags.head())
print(df_users.head())

df_order.to_csv("data/processed/orders.csv", index=False)
df_order_items.to_csv("data/processed/order_items.csv", index=False)
df_products.to_csv("data/processed/products.csv", index=False)
df_product_reviews.to_csv("data/processed/product_reviews.csv", index=False)
df_product_tags.to_csv("data/processed/product_tags.csv", index=False)
df_users.to_csv("data/processed/users.csv", index=False)