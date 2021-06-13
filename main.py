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

from settings import DriverSettings
import psycopg2
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
ProductUrlsArr = []
# =================================================
# * CONSTANTS
# =================================================
PAGE_NR = 0
WAIT = 10


# =================================================
# * DRIVER UTILITY FUNCTIONS
# =================================================
def incrementPageNr():
    global PAGE_NR
    PAGE_NR = PAGE_NR+1


def check_exists_by_selector(CurrentDriver, selector):
    try:
        if(selector == ''):
            return None
        return CurrentDriver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None


def check_exists_by_selectors(CurrentDriver, selector):
    try:
        if(selector == ''):
            return None
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
def getProducts(DRIVER, ScrapeSelectors):
    # ELEMENTS
    CurrentDriver = DRIVER
    try:
        waitUntilLoaded(CurrentDriver, ScrapeSelectors.PRODUCTS)
        # print('✅ PRODUCTS FOUND')
        products = CurrentDriver.find_elements(
            By.CSS_SELECTOR, ScrapeSelectors.PRODUCTS)
        # print(len(products))
        # print(CurrentDriver.current_url)
        if(ScrapeSelectors.COOKIE):
            cookie = check_exists_by_selector(
                CurrentDriver, ScrapeSelectors.COOKIE)
            if(cookie):
                cookie_btn = CurrentDriver.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.COOKIE)
                if(cookie_btn.is_displayed() and cookie_btn.is_enabled()):
                    cookie_btn.click()
        for product in products:
            if(ScrapeSelectors.PRODUCT_URL):
                product_url = product.find_element(
                    By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_URL).get_attribute("href").strip()
                ProductUrlsArr.append(product_url)
        print('URLS', len(ProductUrlsArr))
        getNextPageProducts(CurrentDriver, ScrapeSelectors)
    except TimeoutException as e:
        print('❌ PRODUCTS NOT FOUND', e)
        pass
    finally:
        pass


def getNextPageProducts(CurrentDriver, ScrapeSelectors):
    incrementPageNr()
    page = check_exists_by_selector(CurrentDriver, ScrapeSelectors.PAGINATOR)
    if(False):
    # if(page):
        page_btn = CurrentDriver.find_element(
            By.CSS_SELECTOR, ScrapeSelectors.PAGINATOR)
        try:
            current_url = CurrentDriver.current_url
            page_btn.click()
            time.sleep(2)
            if(current_url == CurrentDriver.current_url):
                raise Exception
            else:
                getProducts(CurrentDriver, ScrapeSelectors)
        except Exception:
            elapsed_time = time.time() - start_time
            print('URLS DONE', time.strftime(
                "%H:%M:%S", time.gmtime(elapsed_time)))
            getProductsDetail(CurrentDriver, ScrapeSelectors)
    else:
        elapsed_time = time.time() - start_time
        print('URLS DONE', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        getProductsDetail(CurrentDriver, ScrapeSelectors)


def getProductsDetail(CurrentDriver, ScrapeSelectors):
    for index, url in enumerate(ProductUrlsArr):
        print(index)
        try:
            CurrentDriver.get(url)
            check_exists_by_selector(
                CurrentDriver, ScrapeSelectors.PRODUCT_NAME)
            getDetail(CurrentDriver, ScrapeSelectors, url)
            print('✅ DONE WITH SCRAPING', CurrentDriver.title)
            if(index % DriverSettings.SAVE == 0):
                insertIntoDb()
                print('save into db')

        except TimeoutException as e:
            print(e)
            pass


def getDetail(CurrentDriver, ScrapeSelectors, url):
    product_price_sale = check_exists_by_selector(
        CurrentDriver, ScrapeSelectors.PRODUCT_PRICESALE)
    product_image_urls = check_exists_by_selectors(
        CurrentDriver, ScrapeSelectors.PRODUCT_IMAGE_URLS)
    product_model_name = check_exists_by_selector(
        CurrentDriver, ScrapeSelectors.PRODUCT_MODEL_NAME)
    allSizes = check_exists_by_selectors(CurrentDriver, ScrapeSelectors.SIZES)
    # Product Model Name
    if(product_model_name):
        product_model_name = product_model_name.get_attribute(
            "textContent").strip().capitalize()
    else:
        product_model_name = None
    # Product Price
    if(product_price_sale):
        sale = True
        product_price_sale = float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICESALE).get_attribute(
            "textContent").strip().strip('€').strip().replace(',', '.'))
    else:
        sale = False
        product_price_sale = None
    # Sizes
    if(allSizes):
        sizesArr = []
        for size in allSizes:
            sizesArr.append(float(size.get_attribute(
                "textContent").strip().replace(',', '.')))
        sizesArr = list(dict.fromkeys(sizesArr))
    else:
        sizesArr = None
    available = False
    if(sizesArr):
        if(len(sizesArr) != 0):
            available = True
        else:
            available = False
    # Image
    if(product_image_urls):
        product_image_urls_arr = []
        for image_urls in product_image_urls:
            if image_urls != None:
                product_image_urls_arr.append(
                    str(image_urls.get_attribute("data-src")))
    else:
        product_image_urls_arr = None

    productObj = dict(
        # Brand
        brand_name=ScrapeSelectors.BRAND_NAME,
        brand_url=ScrapeSelectors.BRAND_URL,
        # Items
        product_brand_name=CurrentDriver.find_element(
            By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_BRAND_NAME).get_attribute("textContent").strip().capitalize() or None,
        product_name=CurrentDriver.find_element(By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_NAME).get_attribute(
            "textContent").strip().capitalize() or None,
        product_model_name=product_model_name or None,
        product_description=CurrentDriver.find_element(
            By.CSS_SELECTOR, ScrapeSelectors.PRODUCT_DESCRIPTION).get_attribute("textContent").strip().capitalize() or None,
        product_url=url or '',
        product_price_original=float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICEORIGINAL).get_attribute(
            "textContent").strip().strip('€').strip().replace(',', '.')) or None,
        product_price_old=float(check_exists_by_selector(CurrentDriver, ScrapeSelectors.PRODUCT_PRICEORIGINAL).get_attribute(
            "textContent").strip().strip('€').strip().replace(',', '.')) or None,
        product_price_sale=product_price_sale,
        # Images
        product_images=check_exists_by_selector(
            CurrentDriver, ScrapeSelectors.PRODUCT_IMAGES),
        product_image_urls=product_image_urls_arr,
        # Attributes
        promotion_codes=check_exists_by_selector(
            CurrentDriver, ScrapeSelectors.PROMOTION_CODES),
        colors=check_exists_by_selector(CurrentDriver, ScrapeSelectors.COLORS),
        sizes=sizesArr,
        available=available,
        sale=sale,
        clicked=0,
        gender=ScrapeSelectors.GENDER)
    productsArr.append(productObj)


def resetUrls():
    print("Reset urls")
    global ProductUrlsArr
    ProductUrlsArr = []


# =================================================
# * DATABASE SETTINGS
# =================================================
def connectToDB():
    try:
        conn = psycopg2.connect(
            "dbname='d2n2f9v3vubu6' user='kdbcwlijtpweyi' host='ec2-34-250-16-127.eu-west-1.compute.amazonaws.com' password='077ac9c59bff1cce464f689442ab6a1fc3d38b9f8b53b1bdf24195d6e1573ab4'")
    except:
        conn = False
    if(conn):
        print("DB CONNECTED")
        cursor = getCursor(conn)
        createTables(conn, cursor)
    else:
        print("I am unable to connect to the database")
    return conn


def getCursor(conn):
    cursor = conn.cursor()
    return cursor


def closeDbConnection(cursor, conn):
    cursor.close()
    conn.close()
    print('DB CLOSED')


def createTables(conn, cursor):

    cursor.execute("""CREATE TABLE IF NOT EXISTS bootz (id serial PRIMARY KEY,
    product_url VARCHAR UNIQUE,
    product_brand_name VARCHAR,
    product_name VARCHAR,
    product_model_name VARCHAR,
    product_description TEXT,
    product_price_original FLOAT,
    product_price_sale FLOAT,
    product_price_old FLOAT,
    brand_name VARCHAR,
    brand_url VARCHAR,
    product_images VARCHAR,
    product_image_urls TEXT [],
    promotion_codes VARCHAR,
    colors VARCHAR,
    sizes FLOAT [],
    available BOOL,
    sale BOOL, 
    clicked INT, 
    gender VARCHAR, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW());""")
    conn.commit()
    print("TABLE CREATED")


def insertIntoDb():
    conn = connectToDB()
    if(conn):
        query = """INSERT INTO bootz(product_url,product_brand_name,product_name,product_model_name,product_description,product_price_original,product_price_old, product_price_sale,brand_name,brand_url,product_images,product_image_urls,promotion_codes,colors,sizes,available,sale, clicked, gender) VALUES (%(product_url)s,%(product_brand_name)s,%(product_name)s,%(product_model_name)s,%(product_description)s,%(product_price_original)s,%(product_price_old)s,%(product_price_sale)s,%(brand_name)s,%(brand_url)s,%(product_images)s,%(product_image_urls)s,%(promotion_codes)s,%(colors)s,%(sizes)s,%(available)s,%(sale)s,%(clicked)s, %(gender)s) ON CONFLICT (product_url) DO UPDATE SET product_image_urls = %(product_image_urls)s, promotion_codes = %(promotion_codes)s,colors = %(colors)s ,sizes = %(sizes)s,product_price_original = %(product_price_original)s,product_price_old = bootz.product_price_original,product_price_sale = %(product_price_sale)s,brand_url = %(brand_url)s,available = %(available)s,sale = %(sale)s,clicked = %(clicked)s,updated_at = NOW();"""
        global productsArr
        db = getCursor(conn)
        db.executemany(query, productsArr)
        conn.commit()
        closeDbConnection(db, conn)
        # productsArr = []
    else:
        print("I am unable to connect to the database")
