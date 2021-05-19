# ========================================================================================================================================================================================================================================================================================================================================
# *
# *     #####    #####    #####   ######  ######
# *     ##  ##  ##   ##  ##   ##    ##       ##
# *     #####   ##   ##  ##   ##    ##      ##
# *     ##  ##  ##   ##  ##   ##    ##     ##
# *     #####    #####    #####     ##    ######
# *
# *     CREATED BY ANDRES VERGAUWEN
# *     -- LOCATORS.PY --
# ========================================================================================================================================================================================================================================================================================================================================

class ScrapeSelectors:
    def __init__(self, Selectors):
        self.BASEURL = Selectors.BASEURL
        self.URL = Selectors.URL
        self.PAGE_NUMBER = Selectors.PAGE_NUMBER
        self.CONTAINER = Selectors.CONTAINER
        self.PRODUCTS = Selectors.PRODUCTS
        self.PRODUCT_URL = Selectors.PRODUCT_URL
        self.COOKIE = Selectors.COOKIE
        self.PAGINATOR = Selectors.PAGINATOR
        self.PRODUCT_BRAND_NAME = Selectors.PRODUCT_BRAND_NAME
        self.PRODUCT_NAME = Selectors.PRODUCT_NAME
        self.PRODUCT_DESCRIPTION = Selectors.PRODUCT_DESCRIPTION
        self.PRODUCT_PRICEORIGINAL = Selectors.PRODUCT_PRICEORIGINAL
        self.PRODUCT_PRICESALE = Selectors.PRODUCT_PRICESALE
        self.BRAND_NAME = Selectors.BRAND_NAME
        self.BRAND_URL = Selectors.BRAND_URL
        self.PRODUCT_IMAGES = Selectors.PRODUCT_IMAGES
        self.PRODUCT_IMAGE_URLS = Selectors.PRODUCT_IMAGE_URLS
        self.PROMOTION_CODES = Selectors.PROMOTION_CODES
        self.COLORS = Selectors.COLORS
        self.SIZES = Selectors.SIZES
        self.AVAILABLE = Selectors.AVAILABLE
        self.SALE = Selectors.SALE

# ================================================= 
# * FUNCTIONS
# =================================================
def setSelectors():
    selectors = []
    selectors.append(ScrapeSelectors(Torfs))
    # selectors.append(ScrapeSelectors(Snipes))
    return selectors


def getSelectors():
    selectors = setSelectors()
    print(selectors)
    return selectors

# ================================================= 
# * STORES
# =================================================
class Torfs:
    BASEURL = 'https://www.torfs.be'
    URL = 'https://www.torfs.be/nl/meisjes/schoenen/sneakers/?sz=100'
    # URL = 'https://www.torfs.be/nl/heren/schoenen/sneakers/?sz=100'
    # URL = 'https://www.torfs.be/nl/outlet/heren/?sz=1'
    PAGE_NUMBER = 1
    CONTAINER = 'div.product-grid.search-products__products'
    PRODUCTS = '.product-tile'
    PRODUCT_URL = '.js-product-tile-link'
    COOKIE = '.js-cookieAccept'
    PAGINATOR = '.bs-next'
    # PRODUCTS
    PRODUCT_BRAND_NAME = '.brand-name'
    PRODUCT_NAME = '.product-name'
    PRODUCT_DESCRIPTION = 'div[itemprop="description"]'
    PRODUCT_PRICEORIGINAL = 'span[itemprop="price"]'
    PRODUCT_PRICESALE = '.price__list .value'
    # BRAND
    BRAND_NAME = 'Torfs'
    BRAND_URL = 'https://www.torfs.be'
    # IMAGES
    PRODUCT_IMAGES= ''
    PRODUCT_IMAGE_URLS= ''
    # ATTRIBUTES
    PROMOTION_CODES= ''
    COLORS= ''
    SIZES= '.size-blocks .size-button:not(.disabled)'
    AVAILABLE= False
    SALE= False

class Snipes:
    BASEURL = 'https://www.snipes.be'
    URL = 'https://www.snipes.be'
    PAGE_NUMBER = 1
    CONTAINER = '.CONTAINER_SNIPES'
    PRODUCTS = '.product-tile'
    PRODUCT_URL = '.js-product-tile-link'
    COOKIE = '.js-cookieAccept'
    PAGINATOR = 'a[data-page="0"]'
    # PRODUCTS
    PRODUCT_BRAND_NAME = ''
    PRODUCT_NAME = '.product-name'
    PRODUCT_DESCRIPTION = 'div[itemprop="description"]'
    PRODUCT_PRICEORIGINAL = ''
    PRODUCT_PRICESALE = ''
    # BRAND
    BRAND_NAME = 'Snipes'
    BRAND_URL = 'https://www.snipes.be'
    # IMAGES
    PRODUCT_IMAGES= ''
    PRODUCT_IMAGE_URLS= ''
    # ATTRIBUTES
    PROMOTION_CODES= ''
    COLORS= ''
    SIZES= ''
    AVAILABLE= False
    SALE= False





    