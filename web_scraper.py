from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#Function to extract Product Title
def gettitle(soup):
     # used error handlers .
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        
        title_value = title.text

        title_string = title_value.strip()

    except AttributeError:
        title_string = "Not Mentioned"

    return title_string

# Function to extract Product Price
def getprice(soup):

    try:
        price = soup.find("span", attrs={'class':'a-price a-text-price a-size-medium'}).find("span", attrs={"class": "a-offscreen"}).text

    except AttributeError:

        try:
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = "Not Mentioned"

    return price

# Function to extract Product Rating
def getrating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon-alt'}).text
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = "Not Mentioned"	

    return rating

#  Function to extract seller  of the product.
def getSeller(soup):
    try:
        Seller = soup.find("a", attrs={"id":'sellerProfileTriggerId'}).text.strip()


    except AttributeError:
        Seller = "Not Mentioned"	

    return Seller

# Function to extract Stock Status
def getStock(soup):
    try:
        available = soup.find("span", attrs={"class":'a-size-base a-color-price a-text-bold'}).text.strip()
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


if __name__ == '__main__':

# add your user agent.
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

       #  webpage URL used is pilgrim serum hair oil on amazon.
    URL = "https://www.amazon.com/s?k=pilgrim+serum&crid=3VZA5DRNJ0KAA&sprefix=pilgrim++se%2Caps%2C435&ref=nb_sb_ss_ts-doa-p_1_10"

    #  Requesting HTTP.
    webpage = requests.get(URL, headers=HEADERS)

    # using BeautifulSoup object, which allows you to parse  HTML content retrieved from  web.
    soup = BeautifulSoup(webpage.content, "html.parser")


    # Fetch links as List of each  products 
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # used to store the links
    links_list = []

    # Loop for extracting links from product
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "Seller":[],"Stock":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(gettitle(new_soup))
        d['price'].append(getprice(new_soup))
        d['rating'].append(getrating(new_soup))
        d['Seller'].append(getSeller(new_soup))
        d['Stock'].append(getStock(new_soup))

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("scraped_data.csv", header=True, index=False)
