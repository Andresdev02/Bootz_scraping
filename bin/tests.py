# import unittest
# from selenium import webdriver
# import pages

# class PythonOrgSearch(unittest.TestCase):

#     def setUp(self):
#         PATH = "/Applications/chromedriver"
#         BASEURL = "https://www.torfs.be"
#         URL = "https://www.torfs.be/nl/heren/schoenen/sneakers/?sz=2"
#         self.driver = webdriver.Chrome(PATH)
#         self.driver.get(URL)

#     def test_title(self):
#         mainPage = pages.MainPage(self.driver)
#         assert mainPage.is_title_matches()
        
#     def test_torfs(self):
#         print('start torfs')
#         assert False

#     def test_snipes(self):
#         print('start snipes')
#         assert True


#     def tearDown(self): 
#         self.driver.close()


# if __name__ == "__main__":
#     unittest.main()