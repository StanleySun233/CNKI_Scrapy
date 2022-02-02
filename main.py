import time
import pandas as pd
import selenium.webdriver

resTable = []
search = "树莓派"
pages = 10

option = selenium.webdriver.ChromeOptions()
option.add_argument('headless')

url = 'https://www.cnki.net/'
client = selenium.webdriver.Chrome(options=option)
client.headless = True
client.get(url)

searchBox = client.find_element_by_name("txt_SearchText")
searchBox.send_keys(search)

searchButton = client.find_elements_by_class_name("search-btn")
searchButton[0].click()

time.sleep(2)
title = client.find_elements_by_class_name("result-table-list")
title = title[0].text.split("\n")
col = title[0].split(" ")
page = pages

while pages:
    title = client.find_elements_by_class_name("result-table-list")
    title = title[0].text.split("\n")
    for i in range(len(title)):
        if i % 2 == 1:
            text = title[i].replace("; ", ";")
            text = text.split(" ")[1:]
            resTable.append(text)
    nextPage = client.find_element_by_link_text("下一页")
    nextPage.click()
    print("第{}页，共{}页".format(page-pages + 1, page))
    time.sleep(3)
    pages -= 1

data = pd.DataFrame(data=resTable, columns=col)
data.to_csv(search + ".csv", encoding='utf-8', index=False)

client.close()
