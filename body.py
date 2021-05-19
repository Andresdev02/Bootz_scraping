# ========================================================================================================================================================================================================================================================================================================================================
# *
# *     #####    #####    #####   ######  ######
# *     ##  ##  ##   ##  ##   ##    ##       ##
# *     #####   ##   ##  ##   ##    ##      ##
# *     ##  ##  ##   ##  ##   ##    ##     ##
# *     #####    #####    #####     ##    ######
# *
# *     CREATED BY ANDRES VERGAUWEN
# *     -- BODY.PY --
# ========================================================================================================================================================================================================================================================================================================================================

import time
import psycopg2
from settings import DriverSettings
from locators import getSelectors
from main import getProducts, productsArr

# ================================================= 
# * VARIABLES
# ================================================= 
Bootz = getSelectors()
start_time = time.time()

# ================================================= 
# * CONSTANTS
# ================================================= 
PRODUCT_URLS = []
PATH = DriverSettings.PATH
WAIT = DriverSettings.WAIT
PAGE_NR = 0

# =================================================
# * MAIN
# =================================================


def scrapeProducts():
    for selector in Bootz:
        Driver = startDriver(selector.URL)
        getProducts(Driver, selector)
        print(Driver)
    quitDriver(Driver)

# =================================================
# * FUNCTIONS
# =================================================


def startDriver(url):
    Driver = getDriver(url)
    print('🕛 OPEN DRIVER')
    return Driver


def getDriver(url):
    Settings = DriverSettings()
    Driver = Settings.DRIVER
    Driver.get(url)
    return Driver


def quitDriver(Driver):
    Driver.quit()
    elapsed_time = time.time() - start_time
    print('🕔 CLOSED DRIVER', time.strftime(
        "%H:%M:%S", time.gmtime(elapsed_time)))


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
    product_description TEXT,
    product_price_original FLOAT,
    product_price_sale FLOAT,
    product_price_old FLOAT,
    brand_name VARCHAR,
    brand_url VARCHAR,
    product_images VARCHAR,
    product_image_urls VARCHAR,
    promotion_codes VARCHAR,
    colors VARCHAR,
    sizes FLOAT [],
    available BOOL,
    sale BOOL, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW());""")
    conn.commit()
    print("TABLE CREATED")

def insertIntoDb():
    conn = connectToDB()
    if(conn):
        # print(productsArr)
        query = """INSERT INTO bootz(
            product_url,
            product_brand_name,
            product_name,
            product_description,
            product_price_original,
            product_price_old, 
            product_price_sale,
            brand_name,brand_url,
            product_images,
            product_image_urls,
            promotion_codes,
            colors,
            sizes,
            available,
            sale) VALUES (%(product_url)s,%(product_brand_name)s,%(product_name)s,%(product_description)s, %(product_price_original)s,%(product_price_old)s,%(product_price_sale)s,%(brand_name)s,%(brand_url)s,%(product_images)s,%(product_image_urls)s,%(promotion_codes)s,%(colors)s,%(sizes)s,%(available)s,%(sale)s) ON CONFLICT (product_url) DO UPDATE
        SET promotion_codes = %(promotion_codes)s, colors = %(colors)s ,sizes = %(sizes)s, product_price_original = %(product_price_original)s, product_price_old = bootz.product_price_original, product_price_sale = %(product_price_sale)s, available = %(available)s, sale = %(sale)s, updated_at = NOW();"""
        db = getCursor(conn)
        db.executemany(query, productsArr)
        conn.commit() 
        closeDbConnection(db, conn)
    else:
        print("I am unable to connect to the database")

# ================================================= 
# * START
# ================================================= 
scrapeProducts()
insertIntoDb()
