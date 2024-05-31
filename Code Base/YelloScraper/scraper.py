import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

def extract_customer_data():
    data = []  # create a list to store data

    base_url = "https://www.findyello.com/jamaica/"

    try:
        string_categories = input("Enter Categories: ")
        lead_categories = string_categories.split()

        browser = webdriver.Chrome()  # create an instance of Chrome WebDriver
        browser.get(base_url)  # open the base URL

        for category in lead_categories:
            category_url = base_url + category
            browser.get(category_url)
            time.sleep(3)

            # Find customer data elements using appropriate CSS selectors
            my_text = browser.find_element(By.XPATH, '//*[@class="listing-content"]/h2')
            print(my_text)

            name_elements = browser.find_elements(By.CSS_SELECTOR, "div.listing-title h4 a")
            address_elements = browser.find_elements(By.CSS_SELECTOR, "div.listing-address")
            telephone_elements = browser.find_elements(By.CSS_SELECTOR, "div.listing-phone")

            # Extract customer data and add to the list
            for name_element, address_element, telephone_element in zip(name_elements, address_elements, telephone_elements):
                customer_data = {
                    "Name": name_element.text.strip(),
                    "Address": address_element.text.strip(),
                    "Telephone": telephone_element.text.strip()
                }
                data.append(customer_data)

        browser.quit()  # close the browser

    except NoSuchElementException:
        print('Unable to open browser.')

    return data

# Main function
def main():
    customer_data = extract_customer_data()

    # Print customer data
    for index, customer in enumerate(customer_data, 1):
        print(f"Customer {index}:")
        print("Name:", customer["Name"])
        print("Address:", customer["Address"])
        print("Telephone:", customer["Telephone"])
        print("--------------------")

    # Save customer data to a JSON file
    with open("customer_data.json", "w") as file:
        json.dump(customer_data, file)

if __name__ == "__main__":
    main()
