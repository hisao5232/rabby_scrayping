from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url="https://rabbynet.zennichi.or.jp/agency/ibaraki/area"

driver.get(url)
time.sleep(2)

#水戸市クリック
driver.find_element(By.CSS_SELECTOR,"#__next > div.MuiContainer-root.MuiContainer-maxWidthMd.MuiContainer-disableGutters.css-u9s6t2 > main > div > div > form > div:nth-child(2) > div > div > ul > li:nth-child(1) > label > span.MuiButtonBase-root.MuiCheckbox-root.MuiCheckbox-colorPrimary.PrivateSwitchBase-root.MuiCheckbox-root.MuiCheckbox-colorPrimary.css-txm1df > input").click()

#検索ボタンクリック
driver.find_element(By.CSS_SELECTOR,"#__next > div.MuiContainer-root.MuiContainer-maxWidthMd.MuiContainer-disableGutters.css-u9s6t2 > main > div > div > form > div:nth-child(1) > button").click()
time.sleep(2)

#変数定義
href_list=[]
detail_list=[]

#詳細取得定義
def get_detail():

    #1ページ目の各社のhref要素取得
    href_elems=driver.find_elements(By.CSS_SELECTOR,"h3>a.MuiTypography-root")

    #hrefのみリストに格納
    for href_elm in href_elems:
        href=href_elm.get_attribute("href")
        href_list.append(href)

    #次のページへクリック
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR,"#__next > div.MuiContainer-root.MuiContainer-maxWidthMd.MuiContainer-disableGutters.css-u9s6t2 > main > div > div > div.MuiBox-root.css-0 > div > nav.MuiPagination-root.MuiPagination-text.css-fkxhek > ul > li:nth-child(6) > button").click()
            time.sleep(2)

            #現在のページの各社のhref要素取得
            href_elems=driver.find_elements(By.CSS_SELECTOR,"h3>a.MuiTypography-root")

            #hrefのみリストに追加
            for href_elm in href_elems:
                href=href_elm.get_attribute("href")
                href_list.append(href)

        except:
            print("page_end")
            print(len(href_list))
            break

    #詳細取得
    for shop_href in href_list:
        driver.get(shop_href)
        time.sleep(3)

        name=driver.find_element(By.CSS_SELECTOR,"div>h1").text
        name=name.replace("\u3000"," ")
        address=driver.find_element(By.XPATH,"//th[contains(text(), '住所')]/following-sibling::td[1]").text
        address=address.replace("\u3000"," ")
        tell=driver.find_element(By.CSS_SELECTOR,"p.css-1iosi0b").text
        fax=driver.find_element(By.CSS_SELECTOR,"p.css-1aeu9lz").text
        ceo=driver.find_element(By.XPATH,"//th[contains(text(), '代表者')]/following-sibling::td[1]").text
        ceo=ceo.replace("\u3000"," ")
        dict_detail={"会社名":name,"会社住所":address,"TELL番号":tell,"FAX番号":fax,"代表者名":ceo}
        print(dict_detail)
        detail_list.append(dict_detail)

get_detail()

#次のページへクリック
while True:
    try:
        driver.find_element(By.CSS_SELECTOR,"#__next > div.MuiContainer-root.MuiContainer-maxWidthMd.MuiContainer-disableGutters.css-u9s6t2 > main > div > div > div.MuiBox-root.css-0 > div > nav.MuiPagination-root.MuiPagination-text.css-fkxhek > ul > li:nth-child(6) > button").click()
        time.sleep(2)

        #詳細取得
        get_detail()
        time.sleep(2)

    except:
        print("page_end")
        break

time.sleep(3)

driver.quit()