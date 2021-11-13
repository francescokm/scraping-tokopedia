import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv



list_product = []
list_price = []
list_desc = []
list_rating = []
list_image = []
list_store = []

def toCSV():
  
    try:
        fieldname = [
            'product',
            'price',
            'desc',
            'rating',
            'image',
            'store',
            ]
        with open('csv_file.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= fieldname)
            writer.writeheader()
            j=0
            for data in list_product:
                writer.writerow({
                    "product" : list_product[j],
                    "price" : list_price[j],
                    "desc" : list_desc[j],
                    "rating" : list_rating[j],
                    "image" : list_image[j],
                    "store" : list_store[j],
                })
                j =+ 1  
    except IOError:
        print("I/O error")
  
def callLink(link):
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 3)
    driver.get(link)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    title_mentah = soup.find("meta",  property="og:title")
    x = str(title_mentah["content"]).split("di ")
    judul = x[0].strip()
    toko = x[1]    

    price_mentah = soup.find("meta", property="product:price:amount")
    price = str(price_mentah["content"])

    desc_mentah = soup.find("meta", property="og:description")
    desc = str(desc_mentah["content"])

    img_mentah = soup.find("meta", property="og:image")
    img = str(img_mentah["content"])

    rating = soup.select_one("span[data-testid*=lblPDPDetailProductRatingNumber]").text
    
    list_product.append(judul)
    list_price.append(price)
    list_desc.append(desc)	
    list_rating.append(rating)	
    list_image.append(img)	
    list_store.append(toko)	
    


with webdriver.Firefox() as driver:

    wait = WebDriverWait(driver, 10)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.tokopedia.com/discovery/kejar-diskon")
    time.sleep(5)
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    
    print ("Start Get all list from Tokopedia")
    print ("Please wait..")
    for i in range(1, 50, 5):
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
        except:
            print("Problem")

    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, "html.parser")
    intersection_div = soup.find_all("div", {"class": "intersection-visible-wrapper"})
    div_a_ = soup.find_all("div", {"class": "css-1ehqh5q"})   

    ii = 0
    for div in div_a_ :
        aTags = div.find_all("a", href=True)
        for tag in aTags:
            if ii == 2 :
                break
            print ("Get {} product...".format(ii))
            callLink(str(tag['href']))
            ii += 1
           
        if ii == 2:
            break
        
    print ("Export to CSV")
    toCSV()
    print ("DONE")
