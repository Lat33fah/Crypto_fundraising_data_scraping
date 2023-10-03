import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
# import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

base_url = "https://crypto-fundraising.info/deal-flow/page/"
total_pages = 241


all_href_list = []

# Looping through all the pages
for page_number in range(1, total_pages + 1):
   
    page_url = f"{base_url}{page_number}/"

    driver.get(page_url)

    
    driver.implicitly_wait(10)

    # Get project links on the current page
    project_links = driver.find_elements(By.CLASS_NAME, "t-project-link")
 
    
    href_list = [link.get_attribute("href") for link in project_links]
    all_href_list.extend(href_list)

# print(all_href_list)

with open('crypto_fundraising_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Headers
    fieldnames = ["Project Name", "Project Ticker", "Project Description", "Project Category", "Website Link", "Community Links", "Raised Information"]

    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writeheader()

  
    for href in all_href_list:
        try:
        
            driver.execute_script("window.open('about:blank', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

            driver.get(href)

            driver.implicitly_wait(10)

            # project name
            project_name = driver.find_element(By.CLASS_NAME, "header-project-name").text

            #project ticker
            project_ticker = driver.find_element(By.CLASS_NAME, "header-ticker").text

            # project description
            project_description = driver.find_element(By.CLASS_NAME, "project-description").text

            #  project category
            project_category = driver.find_element(By.CSS_SELECTOR, ".catitem").text

            #  website link
            website_link = driver.find_element(By.CSS_SELECTOR, ".sidewebsites a.linkwithicon").get_attribute("href")

            #  community links
            community_links = [link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR, ".sidewebsites.community a.linkwithicon")]

            # Raised information 
            raised_info_elements = driver.find_elements(By.CSS_SELECTOR, ".recently-fundraising .newrisedblock")
            raised_info = []

            for element in raised_info_elements:
                raised_date = element.find_element(By.CSS_SELECTOR, ".raisedin").text
                raised_amount = element.find_element(By.CLASS_NAME, 'abbrusd').text
                raised_details_link = element.find_element(By.CLASS_NAME, "raisedinlink").get_attribute("href")
                lead_investors = [investor.get_attribute("title") for investor in element.find_elements(By.CSS_SELECTOR, ".newrised_investors_logos a")]
            
                raised_info.append({
                    "Raised Date": raised_date,
                    "Raised Amount": raised_amount,
                    "Details Link": raised_details_link,
                    "Lead Investors": lead_investors
                })


            csv_writer.writerow({
                "Project Name": project_name,
                "Project Ticker": project_ticker,
                "Project Description": project_description,
                "Project Category": project_category,
                "Website Link": website_link,
                "Community Links": ', '.join(community_links),
                "Raised Information": raised_info
            })
        
        # except NoSuchElementException as e:
        #     print(f"Error: {e}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            
            driver.close()

            
            driver.switch_to.window(driver.window_handles[0])

# Closing the webdriver
driver.quit()
