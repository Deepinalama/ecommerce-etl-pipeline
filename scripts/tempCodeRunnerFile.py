df_orders=pd.read_csv("data/processed/orders.csv")

# df_orders.rename(columns={
#     'discountedTotal':'discounted_total',
#     'totalProducts':'total_products',
#     'totalQuantity':'total_quantity'},inplace=True)

# engine=create_engine(f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ecommerce")
# df_orders.to_sql('orders',engine,if_exists='append',index=False)
# print('orders loaded successfully')