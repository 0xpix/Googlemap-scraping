import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

script = """
function waitCss(selector, timeout=5000) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      let elements = document.querySelectorAll(selector);
      if (elements.length > 0) {
        resolve(Array.from(elements).map((el) => el.getAttribute("href")));
      } else {
        reject(`selector "${selector}" not found`);
      }
    }, timeout);
  });
}

return waitCss("div[role*=article]>a").catch(() => []);
"""

#
print('------------------------------------------')
print('             GOOGLE MAPS            \n ')
print('            DATA SCRAPING              ')
print('------------------------------------------')
input_search = input("Search query:  ")
input_size = int(input("size of the results:  "))


# ------------------------------
#       searching for urls
# ------------------------------
def search_and_scroll(query, input_size):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/?hl=en"
    driver.get(url)
    results = []
    while len(results) < input_size:
        scroll_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
        )
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_container)
        urls = driver.execute_script(script)
        results.extend(urls)
    return results


# ------------------------------
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# ------------------------------
result_urls = search_and_scroll(input_search, input_size)


def parse_place(driver):
    """parse Google Maps place"""

    def aria_with_label(label):
        """gets aria element as is"""
        try:
            element = driver.find_element(By.CSS_SELECTOR, f"*[aria-label*='{label}']")
            return element.get_attribute("aria-label")
        except:
            return None

    def aria_no_label(label):
        """gets aria element as text with label stripped off"""
        text = aria_with_label(label)
        if text:
            return text.split(label, 1)[1].strip()
        else:
            return None

    def get_website_link():
        """gets website link if it exists and is not a Google.com link, otherwise returns None"""
        try:
            link_element = driver.find_element(By.CSS_SELECTOR, "a[href*=//]")
            link = link_element.get_attribute("href")
            if "google.com" not in link:
                return link
            else:
                return None
        except:
            return None

    name = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    category = driver.find_element(By.CSS_SELECTOR, "button[jsaction='pane.rating.category']").text

    result = {
        "name": name,
        "category": category,
        # most of the data can be extracted through accessibility labels:
        "address": aria_no_label("Address: "),
        "website": aria_no_label("Website: "),
        "phone": aria_no_label("Phone: "),
        # to extract star numbers from text we can use regex pattern for numbers: "\d+"
        "stars": aria_with_label(" stars"),
        "5_stars": aria_with_label("5 stars"),
        "4_stars": aria_with_label("4 stars"),
        "3_stars": aria_with_label("3 stars"),
        "2_stars": aria_with_label("2 stars"),
        "1_stars": aria_with_label("1 stars"),
        # add website link
        "website_link": get_website_link(),
    }

    for key in ["stars", "5_stars", "4_stars", "3_stars", "2_stars", "1_stars"]:
        value = result[key]
        if value is not None:
            match = re.findall(r"\d+", value)
            if match:
                result[key] = int(match[0])
    return result


places = []
# Wrap the iterable with tqdm
for url in tqdm(result_urls):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[jsaction='pane.rating.category']")))
    places.append(parse_place(driver))
Results_df = pd.DataFrame(places)
Results_df.to_csv(input_search + '.csv', index=False, encoding='UTF-8')
print("Scraping Successful")
