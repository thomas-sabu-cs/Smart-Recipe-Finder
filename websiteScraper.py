from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import pandas as pd

# Step 1: Set up Selenium and Chrome WebDriver
def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no UI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Step 2: Use Selenium to get the webpage
def get_page_source(url):
    driver = get_webdriver()
    driver.get(url)

    # Wait for the listings to load by looking for the "result-row" element
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'result-row'))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
    
    # Get the rendered page source
    page_source = driver.page_source

    # Save the page source to a file for inspection if needed
    with open('output_page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    
    driver.quit()  # Close the browser
    return page_source

# Step 3: Scrape listings using XPath
def scrape_website(page_source):
    tree = html.fromstring(page_source)
    listings = []

    # Craigslist-specific XPath for titles, prices, and links
    titles = tree.xpath("//li[@class='result-row']/p[@class='result-info']/a[@class='result-title hdrlnk']/text()")
    prices = tree.xpath("//li[@class='result-row']/p[@class='result-meta']/span[@class='result-price']/text()")
    links = tree.xpath("//li[@class='result-row']/p[@class='result-info']/a[@class='result-title hdrlnk']/@href")

    if not titles or not prices:
        print("No listings found. Please check the structure of the webpage.")
        return pd.DataFrame()  # Return an empty DataFrame instead of exit()

    # Build the listings DataFrame
    for title, price, link in zip(titles, prices, links):
        listings.append({
            'title': title.strip(),
            'price': price.strip().replace(r'[\$,]', '', regex=True),  # Strip out dollar signs and commas
            'link': link.strip() if link else 'N/A'
        })

    return pd.DataFrame(listings)

# Step 4: Main function to execute the script
def main():
    url = input("Enter the Craigslist URL you want to scrape (including https://): ")

    # Step 2: Get the page source using Selenium
    page_source = get_page_source(url)

    # Step 3: Scrape the listings
    df = scrape_website(page_source)

    # If no data is found, exit early
    if df.empty:
        print("No data found.")
        return

    # Display the first few listings
    print("Top Apartment Listings:")
    print(df.head(10))

    # Optionally save to CSV
    save_choice = input("Would you like to save the listings to a CSV file? (y/n): ")
    if save_choice.lower() == 'y':
        df.to_csv('craigslist_listings.csv', index=False)
        print("Listings saved to 'craigslist_listings.csv'.")

if __name__ == "__main__":
    main()
