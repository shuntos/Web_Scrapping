from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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


def merge_pdfs(pdf_list):
    '''
    Merger all the pdfs in list 
    '''

    pdf_merger = PdfFileMerger()

    # Add PDFs to the merger
    for pdf_path in pdf_paths:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_merger.append(pdf_file)

    # Write the merged PDF to the output file
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

def refresh_page():

    driver.refresh()
    time.sleep(1)

    car_hovers = driver.find_elements_by_class_name("carbox") # returnls name of item_list
    car_hover = car_hovers[car_index]
    car_hover.click()
    models = car_hover.find_elements_by_class_name("cartype") # returnls name of items

    models[last_model].click()
    time.sleep(1)


def print_beautify(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())


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


def download_file(url, savepath):
    if not os.path.exists(savepath):
        print("Saving {} into {}".format(url, savepath))
        response = session.get(url)
        with open(savepath, 'wb') as f:
            f.write(response.content)


def download(beautiful_perioids, selenimum_periods,index ):
    pdf_info = beautiful_perioids[index]


    outpath = outfolder+pdf_info[2]+"/"

    

    if not os.path.exists(outpath):
        os.makedirs(outpath)



    if pdf_info[0]=="pdfsimple":#latest single pfds
        pdf_url = url+"modeles/"+pdf_info[1]+"/"+pdf_info[2]+"/"+pdf_info[3]+"/"+language+"/"+ pdf_info[1]+"_"+pdf_info[2]+"_"+pdf_info[3]+"_"+language+".pdf"

        pdf_file = pdf_url.split('/')[-1]

        savefile = outpath+pdf_file

        if not os.path.exists(savefile):
            print("Downloading: ",pdf_url)


            response = session.get(pdf_url)

            # Save the PDF file to disk
            with open(savefile, 'wb') as f:
                f.write(response.content)


    elif pdf_info[0]=="pdf": #Multiple pages pdfs
        selenimum_periods[i].click()
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
 
        image_url = soup.find("div", id="doczone").find('img').attrs['src']


        
        img_path = outfolder+car_brand+img_folder+os.path.join(os.path.splitext(os.path.basename(image_url))[0], image_url.split('/')[-1])

        if not os.path.exists(os.path.split(img_path)[0]):
            os.makedirs(os.path.split(img_path)[0])


        download_file(image_url, img_path)


        pages = soup.find_all("a", class_="prglinkpdf")
        pdf_links = []

        for link in pages:
            href = link.get('href')
            if href and href.endswith('.pdf'):
                pdf_links.append(href)


        outpath = outfolder+car_brand+pdf_info[1]+"-"+pdf_info[2]+"/"+pdf_info[3]+"/"

        if not os.path.exists(outpath):
            print("Creating dir: ", outpath)
            os.makedirs(outpath)

        pdf_list = []
        for pdf_link in pdf_links:
            savepath = outfolder+car_brand+pdf_info[1]+"-"+pdf_info[2]+"/"+pdf_info[3]+"/"+pdf_link
            source_path = url+"modeles/"+pdf_info[1]+"/"+pdf_info[2]+"/"+pdf_info[3]+"/"+language+"/"+ pdf_link

            pdf_list.append(savepath)

            download_file(source_path, savepath)

        time.sleep(2)
        refresh_page()


    elif pdf_info[0]=="eGuide":
        outpath = outfolder+car_brand+pdf_info[1]+"-"+pdf_info[2]+"/"+pdf_info[3]+"/"
        if not os.path.exists(outpath):
            os.makedirs(outpath)


        selenimum_periods[i].click()
        time.sleep(2)
        soup_new = BeautifulSoup(driver.page_source, 'html.parser')


        new_frame_url = url+soup_new.find("iframe")["src"]
 

        new_driver = webdriver.Chrome(ChromeDriverManager().install())

        new_driver.get(new_frame_url)

        pdf_location = new_driver.find_element_by_id("eguide_pdf")
        time.sleep(1)
        pdf_location.click()
        time.sleep(2)

        new_driver.switch_to.window(new_driver.window_handles[-1])

        savepath = outpath+new_driver.current_url.split('/')[-1]

        download_file(new_driver.current_url, savepath)
        new_driver.quit()

        refresh_page()




driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://service.citroen.com/ACddb/"

img_folder  = "Front_covers/"
car_brand = "Citroen/"
driver.get(url)


car_hovers = driver.find_elements_by_class_name("carbox") # returnls name of items

time.sleep(1)

car_index = 6
car_hover = car_hovers[car_index]

print(car_hover.text)

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

        if "dag" not  in models[i].get_attribute("title"):
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
