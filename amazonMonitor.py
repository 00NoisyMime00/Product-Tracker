import requests
from bs4 import BeautifulSoup
import sys


# function to send an email
from mailerScript import main

import os.path
from os import path
import json

from time import sleep

# get an Indian elite proxy
from proxies import getELiteProxies


# gets a working Elite Indian proxy
proxies = {}
print('getting a new proxy:')
while proxies == {} or proxies == None:
    try:
        proxies = getELiteProxies()
        if proxies != {} and proxies != None:
            break
    except:
        print('retry..')
        sleep(2)
        pass
print('recieved proxy',proxies)

# creates a file for flipkart data if not already present
if path.exists('flipkartDataBase.json') == False:
    with open('flipkartDataBase.json', 'w') as f:
        details = []
        json.dump(details, f)


# creates a file for amazon data if not already present
if path.exists('amazonDataBase.json') == False:
    with open('amazonDataBase.json', 'w') as f:
        details = []
        json.dump(details, f)

# urls of the products to monitor, can change according to you
urls = ['https://www.amazon.in/dp/B071Z8M4KX/',
'https://www.flipkart.com/boat-bassheads-100-wired-headset-mic/p/itmf3vhhxfrt47tq']


# you can add the urls as system arguments and it will be added automatically
if len(sys.argv) > 1:
    urls = sys.argv[1:]


# user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
}

# main loop for all urls
for i in urls:
    
    url = i
    
    # removes unwanted information from the url
    if url.find('flipkart') != -1:
            if url.find('?') != -1:
                url = url[:url.find('?')]
    elif url.find('amazon') != -1:
            url = url[:url.find('B0') + 10]
    
    # Tries to get the content of the page using the proxy, if fails 3 times, gets a new proxy
    try:
        print(url)
        count = 0
        while True:
            try:
                response = requests.get(url,proxies=proxies, headers=headers,timeout=50)
                if response.status_code == 200:
                    break
            except:

                count += 1
                if count == 3:
                    count = 0
                    print('getting new proxy...')
                    proxies = getELiteProxies()
                else:
                    print('take a break..')
    
                sleep(3)
            

        soup = BeautifulSoup(response.content, 'html.parser')
        

        productName = ''
        price = 0
        websiteName = ''


        # finds all the relevant information for flipkart urls
        if url.find('flipkart') != -1:

            
            # on flipkart all the prices are present in a class name given
            websiteName = 'flipkart'
            columns = soup.find('div', attrs={'class':'_1uv9Cb'})
            
            price = list(columns.children)[0].text[1:]

            productName = soup.find('span', attrs={'class':'_35KyD6'}).text.strip()
            

            print('The name of the product is:', productName)
            print('The price on flipkart is:',price)

            currentProductDetails = {}
            currentProductDetails['productName'] = str(productName)
            currentProductDetails['price'] = price
            
            with open('flipkartDataBase.json', 'r') as f:
                products = json.loads(f.read())


            with open('flipkartDataBase.json', 'w') as f:            

                if products == []:
                    products.append(currentProductDetails)
                    
                
                else:
                    found = 0
                    for product in products:
                        if product['productName'] == productName:
                            found = 1
                            oldPrice = product['price']

                            product['price'] = price

                            if oldPrice > price:
                                main(productName, price, websiteName, url)
                            break
                    if found == 0:
                        products.append(currentProductDetails)

                json.dump(products, f)



        # finds all the relevant information for amazon urls
        elif url.find('amazon') != -1:
            
            websiteName = 'Amazon'

            

            productName = soup.find('span', attrs={'id':'productTitle'}).text.strip()
            print('The product name is:',productName)

            
            try:
                price = float(soup.find('span', attrs={'id':'priceblock_dealprice'}).text[2:])
                print('The price is:',price)
            except:
                price = float(soup.find('span', attrs={'id':'priceblock_ourprice'}).text[2:])
                print('The price is:',price)
            
            currentProductDetails = {}
            currentProductDetails['productName'] = str(productName)
            currentProductDetails['price'] = price
            
            with open('amazonDataBase.json', 'r') as f:
                products = json.loads(f.read())


            with open('amazonDataBase.json', 'w') as f:            

                if products == []:
                    products.append(currentProductDetails)
                    
                
                else:
                    found = 0
                    for product in products:
                        if product['productName'] == productName:
                            found = 1
                            oldPrice = product['price']

                            product['price'] = price

                            if oldPrice > price:
                                main(productName, price, websiteName, url)
                            break
                    if found == 0:
                        products.append(currentProductDetails)

                json.dump(products, f)
                sleep(3)

            

    except:
        print('ERROR')
    