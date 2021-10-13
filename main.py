import os
if os.path.exists("SCRAPED.csv"):
    os.remove("SCRAPED.csv")

os.system("scrapy crawl HumanaMain -o SCRAPED.csv -t csv")