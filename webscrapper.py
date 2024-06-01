#You can use these two URLs given below to test application:
#https://www.amazon.in/Euroline-Stainless-Indicator-Detachable-Connector/dp/B0C58B878M/ref=sr_1_1?crid=PFTNDIB9RQLU&keywords=Milton%2BHagen%2BElectric%2B18%2BStainless%2BSteel%2BElectric%2BKettle%2C%2B1%2BPiece%2C%2B18%2BLitres%2C%2BBlack&nsdOptOutParam=true&qid=1699370314&sprefix=milton%2Bhagen%2Belectric%2B18%2Bstainless%2Bsteel%2Belectric%2Bkettle%2C%2B1%2Bpiece%2C%2B18%2Blitres%2C%2Bblack%2Caps%2C234&sr=8-1&th=1
#https://www.snapdeal.com/product/milton-black-18-litres-stainless/674728156188#bcrumbLabelId:234

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

# Function to scrape product information from Amazon
def scrape_amazon_product(url):
    try:
        # Define request headers to mimic a web browser
        headers = {
            'User-Agent': 'Your-User-Agent-Here',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
        }

        # Send an HTTP GET request to the specified URL with the headers
        response = requests.get(url, headers=headers)

        # Check if the response status code is 200 (success)
        if response.status_code == 200:
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the product name element in the HTML
            product_name_element = soup.find('span', class_='a-size-large product-title-word-break')

            if product_name_element:
                # Extract and clean the product name, limiting it to 50 characters
                product_name = product_name_element.get_text().strip()[:50]

                # Find the product price element in the HTML
                price_element = soup.find('span', class_='a-price-whole')

                if price_element:
                    # Extract and clean the product price
                    price = price_element.get_text().strip()
                    return product_name, price

    except Exception as e:
        return None, str(e)

# Function to scrape product information from Snapdeal
def scrape_snapdeal_product(url):
    try:
        # Send an HTTP GET request to the specified URL
        response = requests.get(url)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the product name and price elements in the HTML
        product_name = soup.find('h1', {'class': 'pdp-e-i-head'}).text.strip()
        product_price = soup.find('span', {'class': 'payBlkBig'}).text.strip()

        # Limit the product name to 50 characters
        return product_name[:50], product_price
    except Exception as e:
        return None, str(e)

# Function to update the table with the comparison results
def compare_products():
    amazon_url = amazon_url_entry.get()
    snapdeal_url = snapdeal_url_entry.get()

    amazon_product_name, amazon_product_price = scrape_amazon_product(amazon_url)
    snapdeal_product_name, snapdeal_product_price = scrape_snapdeal_product(snapdeal_url)

    if amazon_product_price and snapdeal_product_price:
        amazon_price = float(amazon_product_price.replace(',', ''))
        snapdeal_price = float(snapdeal_product_price.replace(',', ''))

        price_difference = abs(amazon_price - snapdeal_price)

        # Clear existing rows in the table
        for row in product_table.get_children():
            product_table.delete(row)

        # Insert new data into the table
        product_table.insert("", "end", values=("Amazon", amazon_product_name, f"₹{amazon_price:.2f}"))
        product_table.insert("", "end", values=("Snapdeal", snapdeal_product_name, f"₹{snapdeal_price:.2f}"))
        product_table.insert("", "end", values=("", "Price Difference", f"₹{price_difference:.2f}"))

    else:
        comparison_text.set("Price comparison failed.")

# Create a Tkinter window
root = tk.Tk()
root.title("Product Comparison")

# Create and configure input fields
amazon_url_label = tk.Label(root, text="Amazon URL:")
amazon_url_label.pack()
amazon_url_entry = tk.Entry(root)
amazon_url_entry.pack()

snapdeal_url_label = tk.Label(root, text="Snapdeal URL:")
snapdeal_url_label.pack()
snapdeal_url_entry = tk.Entry(root)
snapdeal_url_entry.pack()

# Create and configure comparison button
compare_button = tk.Button(root, text="Compare", command=compare_products)
compare_button.pack()

# Create a label to display comparison results
comparison_text = tk.StringVar()
comparison_label = tk.Label(root, textvariable=comparison_text)
comparison_label.pack()

# Create a table to display product information
product_table = ttk.Treeview(root, columns=("Website", "Product Name", "Product Price"))

# Configure column widths (in pixels) 
product_table.column("#1", width=300)  # Website
product_table.column("#2", width=800)  # Product Name
product_table.column("#3", width=200)  # Product Price

product_table.heading("#1", text="Website")
product_table.heading("#2", text="Product Name")
product_table.heading("#3", text="Product Price")
product_table.pack()


# Run the Tkinter main loop
root.mainloop()
