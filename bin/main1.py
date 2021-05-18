import time
from locators import UrlSettings, ScrapeSelectors, getSelectors
from settings import DriverSettings, ProjectSettings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Settings
PATH = DriverSettings.PATH
WAIT = DriverSettings.WAIT
DRIVER = DriverSettings.DRIVER

BASEURL = UrlSettings.BASEURL
URL = UrlSettings.URL
PAGE_NR = 0
PRODUCT_URLS = []

start_time = time.time()

# DRIVER UTILITY FUNCTIONS
def incrementPageNr():
    global PAGE_NR
    PAGE_NR = PAGE_NR+1

def check_exists_by_selector(selector):
    try:
        DRIVER.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True


def waitUntilLoaded(selector):
    try:
        element = WebDriverWait(DRIVER, WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    except TimeoutException as e:
        print('❌ PRODUCTS NOT FOUND', e)
        return False


# GLOBAL FUNCTIONS
def getNextPageProducts():
    incrementPageNr()
    page = check_exists_by_selector('a[data-page="' + str(PAGE_NR) + '"]')
    if(page):
        page_btn = DRIVER.find_element(
            By.CSS_SELECTOR, 'a[data-page="' + str(PAGE_NR) + '"]')
        page_btn.click()
        time.sleep(2)

        getProducts()
    else:
        elapsed_time = time.time() - start_time
        print('URLS DONE', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        getProductsDetail()


def getProductsDetail():
    for index, url in enumerate(PRODUCT_URLS):
        DRIVER.get(url)
        try:
            detail = getDetail()
            print('✅ DONE WITH SCRAPING', DRIVER.title)

        except TimeoutException as e:
            print(e)
            pass


def getDetail():
    element = WebDriverWait(DRIVER, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_NAME)))
    return element


# QUIT DRIVER
def quitDriver():
    DRIVER.quit()
    elapsed_time = time.time() - start_time
    print('🕔 CLOSED DRIVER', time.strftime(
        "%H:%M:%S", time.gmtime(elapsed_time)))


def getProducts():
    # ELEMENTS
    try:
        waitUntilLoaded(ScrapeSelectors.PRODUCTS)
        print('✅ PRODUCTS FOUND')
        products = DRIVER.find_elements(By.CSS_SELECTOR, ScrapeSelectors.PRODUCTS)
        print(len(products))
        print(DRIVER.current_url)
        if(ScrapeSelectors.COOKIE):
            cookie = check_exists_by_selector(ScrapeSelectors.COOKIE)
            if(cookie):
                cookie_btn = DRIVER.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.COOKIE)
                if(cookie_btn.is_displayed() and cookie_btn.is_enabled()):
                    cookie_btn.click()
        for product in products:
            if(ScrapeSelectors.PRODUCT_URL):
                product_url = product.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_URL).get_attribute("href").strip()
                PRODUCT_URLS.append(product_url)
        print('URLS', len(PRODUCT_URLS))
        getNextPageProducts()
    except TimeoutException as e:
        print('❌ PRODUCTS NOT FOUND', e)
    finally:
        quitDriver()
        pass


# START DRIVER
print('🕛 OPEN DRIVER')
# DRIVER.get(URL)
# getProducts()



