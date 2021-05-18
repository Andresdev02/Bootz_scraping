# ========================================================================================================================================================================================================================================================================================================================================
# *
# *     #####    #####    #####   ######  ######
# *     ##  ##  ##   ##  ##   ##    ##       ##
# *     #####   ##   ##  ##   ##    ##      ##
# *     ##  ##  ##   ##  ##   ##    ##     ##
# *     #####    #####    #####     ##    ######
# *
# *     CREATED BY ANDRES VERGAUWEN
# *     -- SETTINGS.PY --
# ========================================================================================================================================================================================================================================================================================================================================

from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# ================================================= 
# * FUNCTIONS
# =================================================
def rotate_user_agent():
    # Rotate user_agent
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                        OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent

class DriverSettings():
    PATH = '/Applications/chromedriver'
    WAIT = 10
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("user-agent={}".format(rotate_user_agent()))
    DRIVER = webdriver.Chrome(PATH, 0,OPTIONS)
