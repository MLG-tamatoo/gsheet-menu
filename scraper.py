import requests
import kroger_api_authorization
import classes
import time


api_url = "https://api.kroger.com/v1/"

def GetProductToken():
    #initilize the access token class
    product_access_token = classes.token(kroger_api_authorization.GetAuth(scope="product.compact"),time.time())
    return product_access_token

def GetLocationToken():
    location_access_token = classes.token(kroger_api_authorization.GetAuth(scope="product.compact"),time.time())
    return location_access_token

def MakeTheAdressDictionary(adress_line_1, city, state_initial, county, zip_code):
    return 'address:{addressLine1:'+adress_line_1+',city:'+city+',state:'+state_initial+',zipCode:'+zip_code+',county:'+county+'}'
    

def FindLocationID(zip_code, location_access_token, number_of_stores):
    if time.time() > 1800+location_access_token.token_time:
        GetLocationToken()
    #else: we have a good token

    search_url = api_url+"locations?"+"filter.zipCode.near="+zip_code+"&filter.limit="+str(number_of_stores) #"&filter.adress={adressLine1:"+adress+"}" # get the first response item for our query
    # print(search_url)
    req_head = {'Accept': 'application/json', 'Authorization': f'Bearer {location_access_token.token_id}'} 

    query = requests.get(search_url, headers=req_head)
    # print(req_head["Authorization"]+"\n\n")
    # print(query.text)
    return query.json()

def FindItem(object_name, location_id, product_access_token, number_of_products):
    #check to see if our token has expired
    if time.time() > 1800+product_access_token.token_time:
        GetProductToken()
    #else: we have a good token

    search_url = api_url+"products?filter.locationId="+location_id+"&filter.term="+object_name+"&filter.limit="+str(number_of_products) # get the first response item for our query

    req_head = {'Accept': 'application/json', 'Authorization': f'Bearer {product_access_token.token_id}'} 

    query = requests.get(search_url, headers=req_head)
    # print(req_head["Authorization"]+"\n\n")
    # print(query.text)
    return query.json()

