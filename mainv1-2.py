import scraper
import json
import gsheet_functions as gfuncs

try:
    with open("client_information.json", "r") as file:
        client_data = json.load(file)
except FileNotFoundError:
    client_zip_code = input("Please give me the zipcode for the Frys you would like to look at: ")
    with open("client_information.json", "w") as file:
        file.write('{\n\t"zipCode":"'+client_zip_code+'"\n}')
        
    with open("client_information.json", "r") as file:
        client_data = json.load(file)
        
def SetUpSpreadSheet():
    spreadsheet_name = input("What is the name of your spreadsheet?")
    print("Make sure to share this spread sheet with your google service account\nIF YOU DO NOT DO THIS IT WILL NOT WORK")
    client_data["spreadsheetName"] = spreadsheet_name
    with open("client_information.json", "w") as file:
            json.dump(client_data, file)
    gfuncs.SetUpIngredientsSheet(spreadsheet_name)

def EstablishStore():
    user_in = input("Would you like to update/change your zipcode in your client data?(y/n): ").lower()
    if user_in == "y":
        new_zip = input("What is the new zipcode?: ")
        client_data["zipCode"] = new_zip
        with open("client_information.json", "w") as file:
            json.dump(client_data, file)

    number_of_stores = 5
    print(f"Searching for top {number_of_stores} stores...")
    location_access_token = scraper.GetLocationToken()
    stores = scraper.FindLocationID(zip_code=client_data["zipCode"], number_of_stores=number_of_stores, location_access_token=location_access_token)["data"]
    for i in range(0,number_of_stores):
        print("#"+str(i+1)+"\t"+json.dumps(stores[i]["address"]))
        print("\n")
    store_choice = int(input("What # store would you like(1,2,3,4, or 5)?: "))
    client_data["storeId"] = stores[store_choice-1]["locationId"]
    client_data["storeName"] = stores[store_choice-1]["name"]
    with open("client_information.json", "w") as file:
            json.dump(client_data, file)
    print("User Information Updated")
    return 0
    

def SearchProducts():
    try:
        print(f"You are searching at the store with ID: "+client_data["storeId"])
    except KeyError:
        print("You have not established a store yet, please establish a store before searching for a product")
        return 1
    
    number_of_products = 5
    wanted_item = input("What would you like to look for at your store?: ")

    product_access_token = scraper.GetProductToken()
    items = scraper.FindItem(object_name=wanted_item, number_of_products=number_of_products, location_id=client_data["storeId"], product_access_token=product_access_token)["data"]
    for i in range(0,len(items)):
        item = items[i]
        description = item["description"]
        price_info = item["items"][0]["price"]
        print(f"#{i+1}\tDESCRPTION: {description}\n\tPRICE: {price_info}\n")
    product_choice = int(input("What # product would you like(1,2,3,4, or 5)?: "))
    
    attempt = gfuncs.AddProduct(item_json=items[product_choice-1],client_data=client_data)
    
    if attempt == 0:
        print("Product Added to Gsheet")
        return 0
    else:
        return 1

commands = {"set up gsheet":"This is how you store the google sheet information that you need, do this before product search", "establish store":"This is what is used to establish the store id for searching for products based off of zipcodes", "product search":"Once a store is established this is how the product information is retried from kroger", "help":"displays this message", "exit":"This closes the program"}

flag = False
while flag == False:
    user_in = input("What would you like to do?('help' for options): ")
    match user_in.lower():
        case "set up gsheet":
            SetUpSpreadSheet()
        case "establish store":
            EstablishStore()
        case "product search":
            SearchProducts()
        case "help":
            print(commands)
        case "exit":
            flag = True
            print("Exiting Program, Thank you")
        case _:
            print("I don't understand")


