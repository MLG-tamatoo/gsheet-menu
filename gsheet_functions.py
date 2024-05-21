import gspread
import json
import time

gc = gspread.service_account(filename=".\google_credentials.json")


def SetUpIngredientsSheet(sheet_name):
    
    sheet = gc.open(sheet_name)
    #check if the ingredients sheet exists
    try:
        wrks = sheet.worksheet("Ingredients")
    except:
        print("Creating Ingredients Sheet...")
        sheet.add_worksheet(title="Ingredients", rows=1000, cols=1000)

    wrks = sheet.worksheet("Ingredients")

    print("Adding Headers...")
    wrks.update(range_name="A1:J1", values=[["Ingredient Name", "ProductId", "Unit Price", "Size", "Price Per Oz", "Sold By",  "Store Name", "StoreId", "Time Updated", "Whole Query"]])
    wrks.format("A1:J1", {'textFormat': {'bold': True}})

def AddProduct(client_data, item_json):
    try:
        sheet_name = client_data["spreadsheetName"]
    except KeyError:
        print("You have not given us a gsheet name to edit. Please do that and try again.")
        return 1
    sheet = gc.open(sheet_name)
    try:
        wrks = sheet.worksheet("Ingredients")
    except:
        SetUpIngredientsSheet(sheet_name)
    wrks = sheet.worksheet("Ingredients")
    possible_position = CheckIfProductInIngredients(wrks=wrks, product_id=item_json["productId"])
    if possible_position != (0,0):#then the ingredient already exists
        print(f"We have found that this ingredient already exists in the list and have updated it in row {possible_position[0]}")
        number_of_rows = possible_position[0]-1
    else: #the ingredient does not exist
        list_of_lists = wrks.get_all_values()
        number_of_rows = len(list_of_lists)
    oz_size = item_json["items"][0]["size"].split(" ")[0]
    if "/" in oz_size:
        oz_size = float(oz_size.split("/")[0])/float(oz_size.split("/")[1])
    else:
        oz_size = float(oz_size)
    unit = item_json["items"][0]["size"].split(" ")[1]
    if unit == "lb":
        oz_size = oz_size*16
    elif unit == "gallon":
        oz_size = oz_size*128

    list_of_info = [ item_json["description"], item_json["productId"], item_json["items"][0]["price"]["regular"], f"{oz_size} oz", float(item_json["items"][0]["price"]["regular"])/oz_size, item_json["items"][0]["soldBy"], client_data["storeName"], client_data["storeId"], time.time() , json.dumps(item_json) ]
    print(list_of_info)
    wrks.update( range_name=f"A{number_of_rows+1}:J{number_of_rows+1}", values=[list_of_info])
    return 0

def CheckIfProductInIngredients(wrks, product_id):
    search = wrks.find(product_id)
    if search == None:
        return (0,0)
    else:
        return (search.row, search.col)
    