# IMPORTS
import time
import json
import random
import psycopg2
from psycopg2.extras import Json, DictCursor
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bootzitems import BootzItems
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


# VARIABLES
BASEURL = 'https://www.torfs.be'
DELAY = 15
bootzProduct = BootzItems
productsArr = []


# DATABASE
# ------- SEEDERS ------- #
def setSeeders():
    conn = getConnection()
    if(conn):
        cur = getCursor(conn)
        createTables(conn, cur)
        closeDbConnection(cur, conn)
    else:
        print("I am unable to connect to the database")


def createTables(conn, cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS sneakers (id serial PRIMARY KEY,brand_name varchar,brand_url varchar,item_brand_name varchar,  item_name varchar, item_description text, item_url varchar);""")
    conn.commit()
    print("TABLE CREATED")
  

# DATABASE SETTINGS


def connectToDB():
    try:
        conn = psycopg2.connect(
            "dbname='d2n2f9v3vubu6' user='kdbcwlijtpweyi' host='ec2-34-250-16-127.eu-west-1.compute.amazonaws.com' password='077ac9c59bff1cce464f689442ab6a1fc3d38b9f8b53b1bdf24195d6e1573ab4'")
    except:
        conn = False
    return conn


def getConnection():
    conn = connectToDB()
    if(conn):
        print("DB CONNECTED")
    else:
        print("I am unable to connect to the database")
    return conn


def getCursor(conn):
    cur = conn.cursor()
    return cur


def closeDbConnection(cur, conn):
    cur.close()
    conn.close()
    print('DB CLOSED')


# FUNCTIONS

# ------- settings -------- #
def rotate_user_agent():
    # Rotate user_agent
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent


def driverSettings(currentUrl):
    user_agent = rotate_user_agent()
    headers = {'User-Agent': user_agent}
    browser = Request(currentUrl, headers=headers)
    webpage = urlopen(browser).read()
    return webpage


# ------- navigate -------- #


def goToStartPage():
    # url = 'https://www.snipes.be/nl/c/shoes/sneaker?sz=1'
    url = 'https://www.torfs.be/nl/heren/schoenen/sneakers/?sz=5'
    webpage = driverSettings(url)

    time.sleep(1)
    try:
        print('Page is ready!')
        getPageContent(webpage, 'start', url)
    except TimeoutException:
        print('Loading took too much time!')
        pass


def goToDetailPage(url: str):
    webpage = driverSettings(url)
    time.sleep(1)
    try:
        print('Detail is ready!')
        getPageContent(webpage, 'detail' , url)
    except TimeoutException:
        print('Loading took too much time!')
        pass

# ------- content -------- #


def getPageContent(webpage, type, url):

    html = BeautifulSoup(webpage, 'html.parser')
    # print(html.title.text)
    if type == 'start':
        getAllItems(html)
        print('start')
    elif type == 'detail':
        getDetailItem(html, url)
        print('detail')
    else:
        getAllItems(html)
        print('start')


def getAllItems(html):
    items = html.select('.product-tile')
    getItem(items)


def getItem(items):
    for item in items:
        # BootzItems.itemBrand = item.select_one( '.b-product-tile-brand').text.strip() or None
        # BootzItems.itemName = item.select_one(
        #     '.b-product-tile-link').text.strip() or None
        url = BASEURL + item.select_one('.js-product-tile-link')['href'].strip() or ''
        goToDetailPage(url)
    insertIntoDb()


def getDetailItem(html, url):
    productObj = dict (
        # Brand
        brand_name= '',
        brand_url= '',
        product_brand_name= '',

        # Items
        product_name= '',
        product_description= '',
        product_url= url or '',
        product_priceOriginal= 0,
        product_priceSale= '',

        # Attributes
        promotion_codes= '',
        colors= '',
        sizes= '',
        available= False,
        sale= False,

        # Images
        image_urls= '',
        images= '',
    )

    productObj['product_name'] = html.select_one('.product-name').text.strip() or ''
    productObj['product_description'] = html.select_one('div', {'itemprop' : 'description'}).text.strip() or ''
    # BootzItems.productName = html.select_one('.b-product-tile-link').text.strip() or None
    # BootzItems.productDescription = html.select_one('.b-details-content p').text.strip() or None
    # symbols =  ['$', '€', '£']
    # BootzItems.productPriceOriginal = [x.strip(symbols) for x in html.select_one('.b-product-tile-price-product').text] or None
    print(productObj['item_name'])
    productsArr.append(productObj)


def insertIntoDb():
    conn = getConnection()
    if(conn):
        print(productsArr)
        query = """INSERT INTO sneakers(brand_name,brand_url,item_brand_name, item_name,item_description, item_url) VALUES (%(brand_name)s,%(brand_url)s,%(item_brand_name)s,%(item_name)s, %(item_description)s,%(item_url)s)"""
        cur = getCursor(conn)
        cur.executemany(query, productsArr)
        conn.commit()
        closeDbConnection(cur, conn)
    else:
        print("I am unable to connect to the database")

# Run on start script


setSeeders()
goToStartPage()
