"""Demo for find module"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from find import element


def main():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)

    driver.get("https://polar-scrubland-57061.herokuapp.com/review/18#one")

    # XPATHS
    bruuveri_title_x = "//*[contains(text(),'Bruuveri')]"
    paisano_title_x = "//*[contains(text(),'Paisano')]"
    crit_1 = '//*[@id="one"]/div/div/div[2]/table/tbody/tr[1]/td[1]'
    crit_2 = '//*[@id="one"]/div/div/div[2]/table/tbody/tr[2]/td[1]'
    crit_3 = '//*[@id="one"]/div/div/div[2]/table/tbody/tr[3]/td[1]'
    crit_4 = '//*[@id="one"]/div/div/div[2]/table/tbody/tr[4]/td[1]'

    print("# --- first --- #")
    locators = [
        (By.XPATH, paisano_title_x), 
        (By.XPATH, bruuveri_title_x)
    ]

    title = element(driver, locators)
    print(title.text)

    locators = [
        (By.XPATH, crit_1),
        (By.XPATH, crit_2),
        (By.XPATH, crit_3),
        (By.XPATH, crit_4),

    ]

    criteria = element(driver, locators)
    print(criteria.text)

    print("\n# --- inclusive --- #")
    locators = [
        (By.XPATH, bruuveri_title_x),
        (By.XPATH, crit_2),
        (By.XPATH, bruuveri_title_x),
        (By.XPATH, crit_4)
    ]
    
    some_none = element(driver, locators, method="inclusive")
    for item in some_none:
        print(item)

    
    print("\n# --- exclusive --- #")
    locators = [
        (By.XPATH, bruuveri_title_x),
        (By.XPATH, crit_2),
        (By.XPATH, bruuveri_title_x),
        (By.XPATH, crit_4)
    ]
    
    some_none = element(driver, locators, method="exclusive")
    for item in some_none:
        print(item.text)
        
    
if __name__ == "main":
    main()

