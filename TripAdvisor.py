from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import csv
import pandas as pd

path_to_file = "reviews.csv"
csvFile = open(path_to_file, 'w', newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)

##Creation de header de fichier csv
csvWriter.writerow(["Hotel_Name", "Price", "Global_Rating" , "NBR_Reviews", "Hotel_Location", "Client_Name", "Location", "Review", "Date"])

# Chrome driver
driver = webdriver.Chrome('chromedriver')
driver.get('https://www.tripadvisor.com/Hotels-g293730-a_ufe.true-Morocco-Hotels.html')
# https://www.tripadvisor.com/Hotels-g293730-a_ufe.true-Morocco-Hotels.html
reviews = []
hotel_names = []
names = []
## Boucle 1 permet de parcourir 30 page chaque page a 30 hotel
for i in range(0, 30):
    try:

        hotel_names = driver.find_elements(By.CSS_SELECTOR, "div.listing_title > a".format(10))

        ##La button suivant pour passer vers les autres pages
        next = driver.find_element(By.CSS_SELECTOR, "div.listFooter > span.next")

        ##ID de page originale
        original_window = driver.current_window_handle

        ##Boucle 2 permet de parcourir les 30 hotels de chaque page
        for i in hotel_names:

            ##overture de page de deatills de chaque hotel
            driver.execute_script("window.open('{}')".format(i.get_attribute("href")))

            ##changement de driver vers la nouvelle fenetre d'hotel
            driver.switch_to.window(driver.window_handles[1])

            ##nom hotel
            hotel_name = driver.find_element(By.CSS_SELECTOR, '#HEADING').text

            ##Boucle 3 permet de parcourir la page de detaills d'un hotel 10 fois pour collecter les avis chaque page avec 10 avis
            for i in range(0, 10):

                ##Gestion des exceptions si un element ne se trouve pas dans une page
                try:
                    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.YibKl.MC.R2.Gi.z.Z.BB.pBbQr')
                    nbr_reviews = ""
                    try:
                        nbr_reviews = driver.find_element(By.CSS_SELECTOR,
                                                          'a.BMQDV._F.G-.wSSLS.SwZTJ.FGwzt.ukgoS > div.jVDab.o.W.f.u.w.GOdjs > span.biGQs._P.pZUbB.KxBGd').text
                    except NoSuchElementException:
                        nbr_reviews = ""
                    hotel_location = ""
                    try:
                        hotel_location = driver.find_element(By.CSS_SELECTOR,
                                                             'div.gZwVG.H3.f.u.ERCyA > span.oAPmj._S > span.biGQs._P.pZUbB.KxBGd').text
                    except NoSuchElementException:
                        hotel_location = ""
                    price = ""
                    try:
                        price = driver.find_element(By.CSS_SELECTOR,
                                                    'div.f.u.Pa.PN.Pn.PF.NB > div.ITglM.Wi.PP.Vm > div.mcvYL.b').text
                    except NoSuchElementException:
                        price = ""
                    hotel_name = driver.find_element(By.CSS_SELECTOR, '#HEADING').text
                    rating = driver.find_element(By.CSS_SELECTOR, 'div.ui_column > div.grdwI.P > span.uwJeR.P').text
                    next = driver.find_element(By.CSS_SELECTOR, "div.ui_pagination > a.next")

                    ##Boucle 4 permet de parcourir les 10 avis dans chaque page
                    for i in range(len(reviews)):
                        name = reviews[i].find_element(By.CSS_SELECTOR,
                                                       'div.IHLTq._Z.o > div.cRVSd > span > a.ui_header_link.uyyBf').text
                        location = ""
                        try:
                            location = reviews[i].find_element(By.CSS_SELECTOR,
                                                               'div.MziKN > span.RdTWF > span.default.LXUOn.small').text
                        except NoSuchElementException:
                            location = ""
                        review = reviews[i].find_element(By.CSS_SELECTOR, 'div.fIrGe._T > span.QewHA.H4._a > span').text
                        review_title = reviews[i].find_element(By.CSS_SELECTOR,
                                                               'div.KgQgP.MC._S.b.S6.H5._a > a.Qwuub > span > span').text
                        date = \
                        reviews[i].find_element(By.CSS_SELECTOR, 'div.EftBQ > span.teHYY._R.Me.S4.H3').text.split(":")[
                            1]

                        ##ecreture dans un fichier csv
                        csvWriter.writerow(
                            [hotel_name, price, rating, nbr_reviews, hotel_location, name, location, review, date])
                except StaleElementReferenceException:
                    # Element is stale, wait for it to re-appear or re-locate it
                    next = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui_pagination > a.next")))
                    next.click()
            ##fermeture d'une fenetre
            driver.close()
            ##Changement de driver fvers la fenetre originale
            driver.switch_to.window(original_window)
    except StaleElementReferenceException:
        # Element is stale, wait for it to re-appear or re-locate it
        next = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.listFooter > span.next")))
        next.click()
driver.quit()


spreadsheet = pd.read_csv('reviews.csv')
spreadsheet.head(50)