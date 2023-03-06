# Bloc N° 1 : Construction et alimentation d'une infrastructure de gestion de données



# Plan your trip with Kayak


## Context and goals of this study:

Kayak is a travel search engine that helps users plan their next trip at the best price.

They did discover that 70% of their users who are planning a trip would like to have more information about the destination they are going to.

Kayak Marketing Team would like to create an application that will recommend where people should plan their next holidays; the application should do recommandations about the best destinations based on weather informations and hotels in the area.


This study is a data collection study using API request and scraping.
It also deals with data storage, ETL and SQL queries.

Note that **the credentials to AWS have been removed**

## Available files:

**Main file:**
-	Kayak_FINAL.ipynb: notebook containing the project

**Scraping:**
-	cities.txt : list of cities used to scrap booking.com
-	Kayak_booking.py : Script scraping the site booking.com
-	hotel_details.json: data scraped from booking.com

**Storage:**
-	df_load_to_s3.csv : file loaded to AWS
-	df_load_from_s3.csv : file pulled from AWS

Happy reading !

