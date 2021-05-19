# ========================================================================================================================================================================================================================================================================================================================================
# *
# *     #####    #####    #####   ######  ######
# *     ##  ##  ##   ##  ##   ##    ##       ##
# *     #####   ##   ##  ##   ##    ##      ##
# *     ##  ##  ##   ##  ##   ##    ##     ##
# *     #####    #####    #####     ##    ######
# *
# *     CREATED BY ANDRES VERGAUWEN
# *     -- MAIN.PY --
# ========================================================================================================================================================================================================================================================================================================================================

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# ================================================= 
# * VARIABLES
# ================================================= 
global CurrentDriver
start_time = time.time()
productsArr = []
# ================================================= 
# * CONSTANTS
# ================================================= 
PAGE_NR = 0
WAIT = 10
PRODUCT_URLS = []


# ================================================= 
# * DRIVER UTILITY FUNCTIONS
# ================================================= 
def incrementPageNr():
    global PAGE_NR
    PAGE_NR = PAGE_NR+1

def check_exists_by_selector(CurrentDriver, selector):
    try:
        return CurrentDriver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None

def check_exists_by_selectors(CurrentDriver, selector):
    try:
        return CurrentDriver.find_elements(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None



def waitUntilLoaded(CurrentDriver, selector):
    try:
        element = WebDriverWait(CurrentDriver, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    except TimeoutException as e:
        print('❌ PRODUCTS NOT FOUND', e)
        return False


# ================================================= 
# * GLOBAL FUNCTIONS
# =================================================
def getProducts(DRIVER , ScrapeSelectors):
    # ELEMENTS
    CurrentDriver = DRIVER


    try:
        waitUntilLoaded(CurrentDriver, ScrapeSelectors.PRODUCTS)
        # print('✅ PRODUCTS FOUND')
        products = CurrentDriver.find_elements(By.CSS_SELECTOR, ScrapeSelectors.PRODUCTS)
        # print(len(products))
        # print(CurrentDriver.current_url)
        if(ScrapeSelectors.COOKIE):
            cookie = check_exists_by_selector(CurrentDriver, ScrapeSelectors.COOKIE)
            if(cookie):
                cookie_btn = CurrentDriver.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.COOKIE)
                if(cookie_btn.is_displayed() and cookie_btn.is_enabled()):
                    cookie_btn.click()
        for product in products:
            if(ScrapeSelectors.PRODUCT_URL):
                product_url = product.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_URL).get_attribute("href").strip()
                PRODUCT_URLS.append(product_url)
        print('URLS', len(PRODUCT_URLS))
        getNextPageProducts(CurrentDriver, ScrapeSelectors)
    except TimeoutException as e:
        print('❌ PRODUCTS NOT FOUND', e)
        pass
    finally:
        pass

def getNextPageProducts(CurrentDriver,ScrapeSelectors ):
    incrementPageNr()
    page = check_exists_by_selector(CurrentDriver, ScrapeSelectors.PAGINATOR)
    if(page):
        page_btn = CurrentDriver.find_element(By.CSS_SELECTOR, ScrapeSelectors.PAGINATOR)
        try:
            page_btn.click()
            time.sleep(2)
            getProducts(CurrentDriver, ScrapeSelectors )
        except:
            elapsed_time = time.time() - start_time
            print('URLS DONE', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            getProductsDetail(CurrentDriver, ScrapeSelectors)
    else:
        elapsed_time = time.time() - start_time
        print('URLS DONE', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        getProductsDetail(CurrentDriver, ScrapeSelectors)

def getProductsDetail(CurrentDriver, ScrapeSelectors):
    for index,url in enumerate(PRODUCT_URLS):
        print(index)
        CurrentDriver.get(url)
        try:
            check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_NAME)
            getDetail(CurrentDriver, ScrapeSelectors, url)
            print('✅ DONE WITH SCRAPING', CurrentDriver.title)
        except TimeoutException as e:
            print(e)
            pass

def getDetail(CurrentDriver, ScrapeSelectors, url):
    product_price_sale = check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICESALE)
    allSizes = check_exists_by_selectors(CurrentDriver, ScrapeSelectors.SIZES)
    if(product_price_sale):
        sale = True
        product_price_sale = float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICESALE).get_attribute("textContent").strip().strip('€').strip().replace(',','.'))
    else:
        sale = False
        product_price_sale = None
    if(allSizes):
        sizesArr = []
        for size in allSizes:
            sizesArr.append(float(size.get_attribute("textContent").strip().replace(',','.')))
        sizesArr = list(dict.fromkeys(sizesArr))
    else: 
        sizesArr= None

    if(len(sizesArr) != 0 ):
        available = True
    else: 
        available = False
    
    productObj = dict(
        # Brand
        brand_name = ScrapeSelectors.BRAND_NAME,
        brand_url = ScrapeSelectors.BRAND_URL,
        # Items
        product_brand_name = CurrentDriver.find_element(By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_BRAND_NAME).get_attribute("textContent").strip().capitalize() or None,
        product_name= CurrentDriver.find_element(By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_NAME).get_attribute("textContent").strip().capitalize() or None,
        product_description= CurrentDriver.find_element(By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_DESCRIPTION).get_attribute("textContent").strip().capitalize() or None,
        product_url= url or '',
        product_price_original= float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICEORIGINAL).get_attribute("textContent").strip().strip('€').strip().replace(',','.')) or None,
        product_price_old= float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICEORIGINAL).get_attribute("textContent").strip().strip('€').strip().replace(',','.')) or None,
        product_price_sale =  product_price_sale,
        # Images
        product_images = check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_IMAGES) ,
        product_image_urls = check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_IMAGE_URLS),
        # Attributes
        promotion_codes= check_exists_by_selector(CurrentDriver, ScrapeSelectors.PROMOTION_CODES),
        colors= check_exists_by_selector(CurrentDriver, ScrapeSelectors.COLORS),
        sizes = sizesArr,
        available= available,
        sale= sale)
    productsArr.append(productObj)

