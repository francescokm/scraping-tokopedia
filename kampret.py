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
list_source_html = []
maximum_prduct_numbers = 99 #Change this to 100 if you want to get 100 product list 


def toCSV():
    j=0
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
            
            for data in list_product:
                writer.writerow({
                    "product" : list_product[j].replace('""', ""),
                    "price" : list_price[j],
                    "desc" : list_desc[j].replace('""', ""),
                    "rating" : list_rating[j],
                    "image" : list_image[j],
                    "store" : list_store[j].replace('""', ""),
                })
                if j == maximum_prduct_numbers:
                    break
                    exit()
                j =+ 1  
    except IOError:
        print("I/O error")
  
def callLink(link):
    link_slice = link.split('%2F')
    length = len(link_slice)
  

    try:
        if length == 5 :
            link_slicex = link_slice[4].split('%3F')
            link = link_slice[2]+'/'+link_slice[3]+'/'+link_slicex[0]
        if length == 1:
                link_slicex = link_slice[0].split('%3F')
                link = link_slice[0]
        elif length == 2:    
                link_slicex = link_slice[0].split('%3F')
                link = link_slice[0]+'/'+link_slice[1]
        elif length == 3:        
                link_slicex = link_slice[0].split('%3F')
                link = link_slice[2]
        elif length == 4:        
                link_slicex = link_slice[0].split('%3F')
                link = link_slice[2]+'/'+link_slice[3]+'/'+link_slicex[0]
        
            
    except:
        link = link_slice[2]+'/'+link_slice[3]
    
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 3)
    lin = link.replace("https://", "")
    driver.get('https://'+lin)
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
    

def get_source_code() :
    iix = 0
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 10)
        
        driver = webdriver.Firefox()
        print ("Start Get html code from page list from Tokopedia")
        for iii in range(11) :
            
            driver.get("https://www.tokopedia.com/p/handphone-tablet/handphone?page={}&rt=4,5".format(iii+1))
            time.sleep(10)
            total_height = int(driver.execute_script("return document.body.scrollHeight"))
            list_source_html.append(driver.page_source)                
            soup = BeautifulSoup(list_source_html[iii], "html.parser")                
            div_a_ = soup.find_all("div", {"data-testid": "lstCL2ProductList"})   

            for div in div_a_ :
                aTags = div.find_all("a", href=True)
                for tag in aTags:
                        
                    print ("Get {} product...".format(1+iix))
                    callLink(str(tag['href']))
                    iix += 1
                

get_source_code()        
print ("Export to CSV")
toCSV()
print ("DONE")
