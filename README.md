# Google Map Data Scraping
This Python script allows you to scrape data from Google Maps for a given search query. You can specify the number of results you want to scrape and the script will save the scraped data to a CSV file.

![Python](https://badgen.net/badge/Python/3.x/blue)
![Pandas](https://badgen.net/badge/Pandas/1.5.3/blue)
![Selenium](https://badgen.net/badge/Selenium/4.8.0/orange)
![tqdm](https://badgen.net/badge/Tqdm/4.64.1/cyan)
# Getting Started
## Installing
- Clone or download the repository to your local machine
- Install the required Python packages by running the following command in the terminal:
```bash 
pip install -r requirements.txt
```
# Usage
To use the script, simply run it in a Python environment or from the command line.
```bash
python data-scraping.py
```
It will prompt you to input a search query and the size of the results you want to scrape.
```yaml
py data-scraping.py
Search query: pizza near me
Number of results: 50
```
<br>
After that, the script will search for the query on Google Maps and start scraping data for the results.
The data scraped includes the `name`, `category`, `address`, `website`, `phone`, `review stars`, and `links of each place`. <br>
The output is saved as a `CSV` file with the name of the search query in the same directory as the script.

```diff
Note that the script uses headless mode for Chrome by default. If you want to see the browser window during the scraping process, 
you can remove the --headless option from the webdriver.ChromeOptions() method.
```

# Disclaimer
Please note that web scraping may be against the terms of use of certain websites and can result in legal action. Use this script at your own risk.
