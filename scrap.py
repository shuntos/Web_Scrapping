from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import os
import requests

'''
car_models = driver.find_elements_by_class_name("carbox") # return drop menu of each car item

print(driver.page_source)  # print whole page source

pdf_links = driver.find_elements_by_xpath("//a[contains(@onclick, 'pdf')]") # get all the pdf file with onclick

'''

from selenium.webdriver.common.action_chains import ActionChains
outfolder = "pdfs/"
language = "en_us"
session = requests.Session()


def refresh_page():

    driver.refresh()
    time.sleep(1)

    car_hovers = driver.find_elements_by_class_name("carbox") # returnls name of item_list
    car_hover = car_hovers[car_index]
    car_hover.click()
    models = car_hover.find_elements_by_class_name("cartype") # returnls name of items

    models[last_model].click()
    time.sleep(1)


def extract_car_periods(html):
    soup = BeautifulSoup(html, 'html.parser')

    args_list = []
    date_list  = []
    ul_element = soup.find("ul", id="licarperiodelist")
    li_elements = ul_element.find_all("li")
    for li in li_elements:
        a_tag = li.find("a")
        onclick_str = a_tag["onclick"]
        start_index = onclick_str.index("(") + 1
        end_index = onclick_str.index(")")
        args_str = onclick_str[start_index:end_index].strip("'")
        item_list = [item.strip("' ") for item in args_str.split(',')]


        args_list.append(item_list)
        date_list.append(li.text)


    return args_list, date_list




def download(beautiful_perioids, selenimum_periods,index ):
    pdf_info = beautiful_perioids[index]


    outpath = outfolder+pdf_info[2]+"/"

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    if pdf_info[0]=="pdfsimple":
        pdf_url = url+"modeles/"+pdf_info[1]+"/"+pdf_info[2]+"/"+pdf_info[3]+"/"+language+"/"+ pdf_info[1]+"_"+pdf_info[2]+"_"+pdf_info[3]+"_"+language+".pdf"

        pdf_file = pdf_url.split('/')[-1]

        savefile = outpath+pdf_file

        if not os.path.exists(savefile):
            print("Downloading: ",pdf_url)


            response = session.get(pdf_url)

            # Save the PDF file to disk
            with open(savefile, 'wb') as f:
                f.write(response.content)


    elif pdf_info[0]=="pdf":
        selenimum_periods[i].click()
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
 
        image_url = soup.find("div", id="doczone").find('img').attrs['src']


        print(image_url)

        time.sleep(2)
        refresh_page()



driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://service.citroen.com/ACddb/"


driver.get(url)


car_hovers = driver.find_elements_by_class_name("carbox") # returnls name of items

time.sleep(1)

car_index = 4
car_hover = car_hovers[car_index]

car_hover.click()



models = car_hover.find_elements_by_class_name("cartype") # returnls name of items

global last_model 


if len(models) == 0:
    print("No Car models Found")
    time.sleep(1)

    element = driver.find_element_by_id("licarperiodelist")
    beautiful_periods = extract_car_periods(driver.page_source)

    print(beautiful_periods)


else:
    for i in range(len(models)):
        last_model = i
        print("Fetching pdfs from {}".format(models[i].get_attribute("title")))

    
        models[i].click()



        # Fetching periods of each model

        # Find all <li> elements under the <ul> element

        beautiful_periods, date_periods = extract_car_periods(driver.page_source)



        for i in range(len(beautiful_periods)):
            element = driver.find_element_by_id("licarperiodelist")
            selenium_period_list = element.find_elements_by_tag_name("li")

            print(beautiful_periods[i], "::::", date_periods[i])
            download(beautiful_periods, selenium_period_list, i)


        #Refreshing the page again
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        car_hovers = driver.find_elements_by_class_name("carbox") # returnls name of item_list
        car_hover = car_hovers[car_index]
        car_hover.click()
        models = car_hover.find_elements_by_class_name("cartype") # returnls name of items



    
#Close the browser window
driver.quit()
