from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search
from trafilatura import extract_metadata
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

def get_urls_from_sitemap(resource_url: str) -> list:
    """
    Recovers the sitemap through Trafilatura
    """
    print(resource_url)
    urls = sitemap_search(resource_url)
    print(urls)
    return urls

def create_dataset(list_of_websites: list) :
    """
    scrapes the data from the list of websites
    """
    data = []
    for url in tqdm(list_of_websites, desc="Websites"):
        urls = get_urls_from_sitemap(website)
        print(urls)
        for url in tqdm(urls, desc="URLs"):
            try:
                # Send HTTP request to the URL
                driver.get(url)
                time.sleep(2)  # Adjust the delay time as needed
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Parse HTML content
                soup = BeautifulSoup(driver.page_source, "html.parser")
                title = soup.title.string
                # Extract text from each paragraph
                paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
                #ul = soup.find_all('ul') 
                lists = [l.get_text(strip=True) for l in soup.find_all("li")]
                content = "\n".join(paragraphs + lists)
                d = {
                    "url": url,
                    "title": title,
                    "body": content,

                }
                data.append(d)
                driver.quit()
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt}")
            except requests.RequestException as err:
                print(f"Error during requests to {url}: {str(err)}")
    return data

def scrape(list_of_websites: list) -> None:
    data = create_dataset(list_of_websites)
    with open("dataset.txt", "w", encoding="utf-8") as file:
        for paragraph in data:
            file.write(paragraph["title"] + "\n")
            file.write(paragraph["body"])
            
scrape(["https://reservenature.com/faq", 
        "https://reservenature.com/how-it-works", 
        "https://reservenature.com/pricing", 
        "https://reservenature.com/about-us",
        "http://reservenature.com/affiliate"
        ])