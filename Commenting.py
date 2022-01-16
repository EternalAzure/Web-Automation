import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

'''
This robot goes to my Restaurant web app where it 
logs in as admin,
makes a review that says 'robot says hi'
and deletes the review.
'''

def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    comment = "robot says hi"
    open_website(driver)
    login(driver)
    make_comment(driver, comment)
    delete_comment(driver, comment)
    breakpoint()

def open_website(driver):
    driver.get("https://polar-scrubland-57061.herokuapp.com/")
    pass

def login(driver):
    driver.find_element_by_id("openLoginView").click()
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("password").submit()

def make_comment(driver, comment):
    click_link(driver, "/review/1#one")
    driver.find_element_by_name("review").send_keys(comment)
    driver.find_element_by_name("review").submit()


def delete_comment(driver, text):
    soup = bs4.BeautifulSoup(driver.page_source)
    form_element = ""
    children = list(soup.find("div", class_="scroll").children)

    for i, child in enumerate(children):
        if text in child.text:
            form_element = child.find_next_sibling()
            break

    action = form_element["action"]
    element = driver.find_element_by_xpath(f"//form[@action='{action}']/input[@type='submit']")
    element.click()

def click_link(driver, url):
    driver.find_element_by_xpath("//a[@href='"+url+"']").click()

if __name__ == '__main__':
    main()
