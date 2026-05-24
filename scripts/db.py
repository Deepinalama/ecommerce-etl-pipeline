import pandas as pd

from sqlalchemy import create_engine
from urllib.parse import quote_plus

password='Ichig0kur0s@ki'
encoded_password=quote_plus(password)




df_users = pd.read_csv("data/processed/users.csv")

# Rename columns to match DB
df_users.rename(columns={
    'id': 'user_id',
    'firstName': 'first_name',
    'lastName': 'last_name',
    'maidenName': 'maiden_name',
    'birthDate': 'birth_date',
    'bloodGroup': 'blood_group',
    'eyeColor': 'eye_color',
    'macAddress': 'mac_address',
    'stateCode': 'state_code',
    'postalCode': 'postal_code',

    # address
    'address_address': 'address',
    'address_city': 'city',
    'address_state': 'state',
    'address_stateCode': 'state_code',
    'address_postalCode': 'postal_code',
    'address_country': 'country',
    'address_coordinates_lat': 'latitude',
    'address_coordinates_lng': 'longitude',

    # company
    'company_department': 'company_department',
    'company_name': 'company_name',
    'company_title': 'company_title',
    'company_address_address': 'company_address',
    'company_address_city': 'company_city',
    'company_address_state': 'company_state',
    'company_address_stateCode': 'company_state_code',
    'company_address_postalCode': 'company_postal_code',
    'company_address_country': 'company_country',
    'company_address_coordinates_lat': 'company_latitude',
    'company_address_coordinates_lng': 'company_longitude'

}, inplace=True)

df_users['birth_date']=pd.to_datetime(df_users['birth_date'],errors='coerce')

df_users=df_users.drop(columns=['password','ssn','ein',
                                'crypto_coin','crypto_wallet','crypto_network'],errors='ignore')

engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_users.to_sql('users',engine,if_exists='replace',index=False)


print("users table loaded successfully")


df_orders=pd.read_csv("data/processed/orders.csv")

df_orders.rename(columns={
    'discountedTotal':'discounted_total',
    'totalProducts':'total_products',
    'totalQuantity':'total_quantity'},inplace=True)

engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_orders.to_sql('orders',engine,if_exists='append',index=False)
print('orders loaded successfully')

df_products=pd.read_csv("data/processed/products.csv")
engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_products.to_sql('products',engine,if_exists='append',index=False)
print('products loaded successfully')


df_product_reviews=pd.read_csv("data/processed/product_reviews.csv")
df_product_reviews.rename(columns={
    'reviewerName':'review_name',
    'reviewerEmail':'reviewer_email',
    'date':'review_date'
},inplace=True)
engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_product_reviews.to_sql('product_reviews',engine,if_exists='append',index=False)
print('product_review loaded successfully')

df_product_tags=pd.read_csv("data/processed/product_tags.csv")
engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_product_tags.to_sql('product_tags',engine,if_exists='append',index=False)
print('product_reviews loaded')






df_order_items=pd.read_csv("data/processed/order_items.csv")
df_order_items.rename(columns={
    'discountPercentage':'discount_percentage',
    'discountedTotal':'discounted_total'},inplace=True)
engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
df_order_items.to_sql('order_items',engine,if_exists='append',index=False)
print('order_items loaded successfully')




