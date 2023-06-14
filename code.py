from bs4 import BeautifulSoup
#library used for web scraping and parsing HTML or XML documents.
import requests
#allows sending HTTP requests to web servers and retrieving the response.
import time
#provides various time-related functions and utilities.
import datetime
#provides classes for manipulating dates and times
import smtplib


#for sending emails using the Simple Mail Transfer Protocol (SMTP)
URL = 'https://www.amazon.ae/Logitech-Master-Performance-Ultra-fast-Scrolling/dp/B07W5JKHFZ/ref=sr_1_1?pd_rd_r=3379ac8e-dae6-4d71-96fa-505df5ed2df7&pd_rd_w=n23SH&pd_rd_wg=ktRgc&pf_rd_p=5910d99f-ac67-4c71-a8f7-d3c7c5f2dc06&pf_rd_r=S3XDY0F0FXTPJXDY7T7J&qid=1686721250&s=computers&sr=1-1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
#User agent helps in identifying the client (browser) making the request. In this case, it is set to simulate a request made by the Mozilla Firefox browser.

response = requests.get(URL, headers=headers)
#sends an HTTP GET request to the specified URL

soup = BeautifulSoup(response.content, "html.parser")
#creates a BeautifulSoup object soup by parsing the content of the response.

product_name_element = soup.find("span", class_="a-size-large product-title-word-break")
#search for a specific HTML element in the parsed HTML content

# Extract the product name from the element
product_name = product_name_element.get_text(strip=True) if product_name_element else "Product name not found"

# Find the whole number part of the price
whole_price_element = soup.find("span", class_="a-price-whole")
whole_price = whole_price_element.get_text(strip=True) if whole_price_element else ""

# Find the decimal part of the price
decimal_price_element = soup.find("span", class_="a-price-fraction")
decimal_price = decimal_price_element.get_text(strip=True) if decimal_price_element else ""

# Combine the whole and decimal parts to get the complete price
price = f"{whole_price}{decimal_price}" if whole_price and decimal_price else "Price not found"

# Print the product name and price
#print("Product Name:", product_name)
#print("Price:", price)

import csv

# Create a timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write data to CSV file
with open("product_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price","Date"])  # Write the headers
    writer.writerow([product_name, price, timestamp])  # Write the data

#Appending the data to the file
file_path = "product_data.csv"
with open(file_path, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([product_name, price, timestamp])

#Function to scrap the required data and create an excel sheet

def check_price():
    URL = 'https://www.amazon.ae/Logitech-Master-Performance-Ultra-fast-Scrolling/dp/B07W5JKHFZ/ref=sr_1_1?pd_rd_r=3379ac8e-dae6-4d71-96fa-505df5ed2df7&pd_rd_w=n23SH&pd_rd_wg=ktRgc&pf_rd_p=5910d99f-ac67-4c71-a8f7-d3c7c5f2dc06&pf_rd_r=S3XDY0F0FXTPJXDY7T7J&qid=1686721250&s=computers&sr=1-1'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
    response = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    product_name_element = soup.find("span", class_="a-size-large product-title-word-break")
    product_name = product_name_element.get_text(strip=True) if product_name_element else "Product name not found"
    
    whole_price_element = soup.find("span", class_="a-price-whole")
    whole_price = whole_price_element.get_text(strip=True) if whole_price_element else ""
    
    decimal_price_element = soup.find("span", class_="a-price-fraction")
    decimal_price = decimal_price_element.get_text(strip=True) if decimal_price_element else ""
    
    price = f"{whole_price}{decimal_price}" if whole_price and decimal_price else "Price not found"
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    import csv
    header=["Title", "Price","Date"]
    data=[product_name, price, timestamp]
    file_path = "product_data.csv"
    
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)
while(True):
    check_price()
    time.sleep(86400)

def send_email(product_url, threshold):
    URL = product_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    product_price_element = soup.find("span", class_="a-price-whole")
    
    product_price = float(product_price_element.get_text().replace(",", ""))
    
    if product_price < threshold:
        # Email configuration
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('your_email@gmail.com', 'xxxxxxxx')
    
    
        subject = "The Shirt you want is below $15! Now is your chance to buy!"
        body = "This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data+analyst+tshirt&qid=1626655184&sr=8-3"
   
        msg = f"Subject: {subject}\n\n{body}"
    
        server.sendmail(
        'your_email@gmail.com',
        'your_email@gmail.com',
        msg
    )
    server.quit()
    else:
        print("The price is not below the threshold.")
