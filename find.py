"""
Concurrent search for multiple webelements.
Funtionality of element() can be expanded by adding
new functions to search_methods dictionary.

Funtionality is three part: 
element() - public interface
method - customize results
_find() - get results

of those parts method is changeable
"""
# 30/04/2022
# EternalAzure

from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

import asyncio


def element(driver: WebDriver, locators: List[tuple], attempts: int = 5, method = "first") -> WebElement:
    """
    By default returns first element found or None.
    Searches for elements in locators concurrently.

    Arguments:
        driver: webdriver instance
        locators: search strategy for driver.find_element
        attempts: how many times will be tried
        method: selects what results are returned

        eg. element(driver, [(By.XPATH, '//div[1]'), (By.XPATH, '//div[2]')], method='inclusive')

    Methods:
        first: returns first webelement found
        inclusive: returns all results including None
        exclusive: returns all results excluding None
    """
    if attempts < 1:
            raise TypeError("must have atleast one attempt")
    if not locators:
        return None

    tasks = []
    for locator in locators:
        tasks.append(_find(driver, locator, attempts))

    return asyncio.run(search_methods[method](tasks))


async def _find(driver: WebDriver, locator: tuple, attempts: int) -> WebElement:
    fails = 0
    while True:
        try:
            return driver.find_element(locator[0], locator[1])
        except NoSuchElementException:
            await asyncio.sleep(0.1)
            fails += 1
            if fails >= attempts:
                return None


async def _first_element(tasks: list) -> WebElement:
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        if task.result():
            return task.result()
        if len(pending) == 0:
            return None


async def _including_none(tasks: list) -> WebElement:
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    return [task.result() for task in done]


async def _excluding_none(tasks: list) -> WebElement:
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    return [task.result() for task in done if task.result() is not None]


search_methods = {
    "first": _first_element,
    "inclusive": _including_none,
    "exclusive": _excluding_none
}
