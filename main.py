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
        CurrentDriver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True


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
    print(ScrapeSelectors.CONTAINER)

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
    page = check_exists_by_selector(CurrentDriver, 'a[data-page="' + str(PAGE_NR) + '"]')
    if(page):
        page_btn = CurrentDriver.find_element(
            By.CSS_SELECTOR, 'a[data-page="' + str(PAGE_NR) + '"]')
        page_btn.click()
        time.sleep(2)

        getProducts(CurrentDriver, ScrapeSelectors )
    else:
        elapsed_time = time.time() - start_time
        print('URLS DONE', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        getProductsDetail(CurrentDriver, ScrapeSelectors)

def getProductsDetail(CurrentDriver, ScrapeSelectors):
    for index, url in enumerate(PRODUCT_URLS):
        CurrentDriver.get(url)
        try:
            detail = getDetail(CurrentDriver, ScrapeSelectors)
            print('✅ DONE WITH SCRAPING', CurrentDriver.title)

        except TimeoutException as e:
            print(e)
            pass

def getDetail(CurrentDriver, ScrapeSelectors):
    element = WebDriverWait(CurrentDriver, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_NAME)))
    return element

