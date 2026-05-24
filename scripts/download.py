import requests
import json
endpoints={
    "products":"https://dummyjson.com/products",
    "users":"https://dummyjson.com/users",
    "carts":"https://dummyjson.com/carts"
}
for name,url in endpoints.items():
    response=requests.get(url)
    data=response.json()


    with open(f"{name}.json","w")as f:
        json.dump(data,f,indent=4) 

        print(f"{name}downloaded")