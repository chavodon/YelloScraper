import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import json

data = []  # create a list to store data

base_url = "https://www.findyello.com/jamaica/"
new_tab_url = "https://www.findyello.com"

try:
    string_categories = input("Enter Categories: ")
    lead_categories = string_categories.split()

    browser = webdriver.Chrome()  # create an instance of Chrome WebDriver
    browser.get(base_url)  # open the base URL
    count = 0
    #need a do while that under a category, loops through possible pages and drags data 

    for category in lead_categories:
        pageNo = 1
        noMorePagesFlag = True
        while (noMorePagesFlag):
            category_url = base_url + category + "/" + "pageno=" + str(pageNo)
            browser.get(category_url)
            print(browser.current_url)
            time.sleep(3)
            repeatFlag = False
            elements = browser.find_elements(By.XPATH, "//a[@class='favorite add-favorite']")
            print(lead_categories[count])
            if (pageNo == 1):
                topOfList = elements[0].get_attribute("data-name")
            elif(topOfList == elements[0].get_attribute("data-name")):
                print("Front Page Loop")
                break
            for element in elements:
                data_url = element.get_attribute("data-url")
                tab_url = new_tab_url + data_url
                
                
                # Open a new tab using JavaScript
                browser.execute_script("window.open();")

                # Switch to the newly opened tab
                browser.switch_to.window(browser.window_handles[-1])

                # Navigate to a different URL in the new tab
                browser.get(tab_url)

                # Perform additional scraping in the new tab
                time.sleep(3)
                cust_data = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[1]/address[1]")
                cust_info = cust_data.get_attribute("innerText")
                #print(cust_info)
                row = [lead_categories[count], cust_info, tab_url]
                file_exists = os.path.isfile("lead_list.csv")
                with open("lead_list.csv", "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)

                    if not file_exists:
                        writer.writerow(["Category", "Info", "Ad Link"])

                    writer.writerow(row)


                # Close the new tab
                browser.close()

                # Switch back to the original tab
                browser.switch_to.window(browser.window_handles[0])

                # Continue scraping in the original tab
                # ...
            browser.get(base_url + category + "/" + "pageno=" + str(pageNo + 1))
            
            try:
                EndOfListingCheck = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/h2")
                if (EndOfListingCheck.get_attribute("innerText") == "We couldn't find what you're looking for." ):
                    print("End of listing")
                    noMorePagesFlag = False
            except NoSuchElementException:
                try:
                    if (browser.current_url == (base_url + category + "/")):
                        print("exhausted viewable")
                        noMorePagesFlag = False
                    else:
                       pageNo = pageNo + 1 
                except NoSuchElementException:
                    continue
                
        count = count + 1
    browser.quit()  # close the browser

except NoSuchElementException:
    print('Unable to open browser.')

