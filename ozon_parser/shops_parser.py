from selenium import webdriver
from excel_table import Excel_table
from bs4 import BeautifulSoup as bs
import time
import data_handler


WAITING_FOR_DOWNLOAD_OZON_PAGE = 15
WAITING_FOR_DOWNLOAD_PRODUCT_OZON = 1
OZON_SCROLLER_COUNTER = 3

SCROLL_CONST = 0.2
RESOLUTION = 1080


class Parser():
    def __init__(self, table, base_url : str, step : int, start_page : int, last_page : str):
        self.is_executed = False
        
        self.base_url = base_url
        self.step = step
        self.page = start_page
        self.last_page = last_page
        self.table = table 
        
        self.driver = self.get_driver()
        
        
    def parsing(self):
        while True:
            try:
                url = self.base_url + f"&page={self.page}"
                html = self.get_html_with_links(url, driver= self.driver)
                
                if html == "" or html == None:
                    self.page += self.step
                    continue
                
                products_links = self.get_products_links(html)
                
                for link in products_links:
                    try:
                        html = self.get_html_of_product(link, self.driver)
                        product_params = data_handler.get_product_params(html, url = link)
                        
                        self.table.add_product(product_params)
                    except:
                        continue

                self.page += self.step
                if self.page > self.last_page:
                    break
            except:
                continue
             
        self.is_executed = True
        
         
    
    def get_html_with_links(self, url, driver) -> str: # when getting links of product

        while True:
            try:
                driver.get(url=url)
                
                for i in range (OZON_SCROLLER_COUNTER):
                    driver.execute_script(f"window.scrollBy(0, {RESOLUTION/2})")
                    time.sleep(SCROLL_CONST)
                
                time.sleep(WAITING_FOR_DOWNLOAD_OZON_PAGE)
                text = driver.page_source

                return text
                
            except Exception as err:
                print (err)
 
    def get_html_of_product(self, url, driver) -> str:
        try:
            driver.get(url=url)
            
            for i in range (OZON_SCROLLER_COUNTER):
                driver.execute_script(f"window.scrollBy(0, {RESOLUTION/2})")
                time.sleep(SCROLL_CONST)
            
            time.sleep(WAITING_FOR_DOWNLOAD_PRODUCT_OZON)
            text = driver.page_source

            return text
            
        except Exception as err:
            print (err)
            return None

        
    
    def get_products_links(self, html) -> list:
        soup = bs(html, "html.parser")

        try :   
            paginator = soup.find("div", id="paginatorContent")
            block = paginator.find("div")
            products = block.find_all("div")
            
        except Exception as err:
            print(err)

        if len(products) == 0:
            return []
        
        links = []
        for product in products:
            a_tags = product.find_all("a")
            
            if len(a_tags) != 0:
                link = a_tags[0].get("href")
                links.append("https://www.ozon.ru" + link)  
            
        return links
        
    def get_driver(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options= options)
        driver.set_page_load_timeout(40)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source" : '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })
        
        driver.maximize_window()
        return driver
