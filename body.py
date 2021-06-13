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
from main import getProducts, insertIntoDb, resetUrls

# ================================================= 
# * VARIABLES
# ================================================= 
Bootz = getSelectors()
start_time = time.time()

# ================================================= 
# * CONSTANTS
# ================================================= 
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
        resetUrls()    
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
# * START
# ================================================= 
scrapeProducts()
insertIntoDb()
