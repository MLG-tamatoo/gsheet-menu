# ABOUT
This is a webscraper program that will find the cost per ounce for an item on Fry's(Kroger) website and then import that into a Google sheet. This allows for the sheet owner to import the cost values throughout the gsheet to make a cost led menu.

# SET UP
The user downloads the latest distro folder(I don't think the build folder matters). The user goes to the google api services and creates their own service api credentials with scope of the google drive api and google sheet api. Then the user gets credentials with the kroger api with scopes of Environment and Location. The user then saves the google credentials json as "google_credentials.json" in the directory of the distro executable. The user will te create a json file called credentials.json and it should look like this

```
{"user":"<your kroger api cred name>", "pass":"<your kroger API client secret>"}
```
Once these are in the same directory as the distro, double click on the mainv?.exe file to launch the program.

# HOW TO USE
First the program will ask you for your zipcode, this is important as it will be used for finding your store. Next do "establish store" and select the store that you want to shop at. Then create a google sheet and share it with the google service account that you created, this is the email adress in your google_credentials.json. Then do "set up gsheet" and put in the name of the google sheet. It will create a sheet inside of the spreadsheet called Ingredients with a tab at the bottom left. This is where the product information will be stored. If the product already exists in the sheet it will update the row of the product with the current information. If it does not exist it will create a product entry after the last product. Once products are added to the sheet use the basic Sheet1 or whatever you want to name it to make your ingredients. You can access the information stored in the Ingredients sheet by doing "Ingredients!<cell_location_of_wanted_product_info>. 

# USE EXAMPLE
Assume I have created the credential files and the google sheet and given the sheet info to the program.
![image](https://github.com/MLG-tamatoo/gsheet-menu/assets/44129367/d57a3630-7efb-4e35-89fb-9a7bdc7e34b2)
![image](https://github.com/MLG-tamatoo/gsheet-menu/assets/44129367/9a04951a-f31c-4264-8dda-0f8fcf14fe52)

# HOW TO HELP
I would love to collab with people on this project. However, this project has reached the point that for me it's good enough and I can do what I need. If someone wants to add something or help please submit an issue or contact me via github to see what we can do, I haven't really used github for collab stuff.

