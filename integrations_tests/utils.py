def scroll_and_click(browser, element):
    browser.execute_script("arguments[0].scrollIntoView(true);", element)
    browser.execute_script("arguments[0].click();", element)
