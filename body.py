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
from main import getProducts

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
    product_url varchar,
    product_brand_name varchar,
    product_name varchar,
    product_description text,
    product_price_original varchar,
    product_price_sale varchar,
    brand_name varchar,
    brand_url varchar,
    product_images varchar,
    product_image_urls varchar,
    promotion_codes varchar,
    colors varchar,
    sizes varchar,
    available varchar,
    sale varchar);""")
    conn.commit()
    print("TABLE CREATED")


# ================================================= 
# * START
# ================================================= 
# scrapeProducts()
connectToDB()
