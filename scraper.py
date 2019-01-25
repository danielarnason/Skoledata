import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://statistik.uni-c.dk/instregvisning/oversigt.aspx')

grundskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt1')
grundskoler.click()

folkeskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt4')
folkeskoler.click()

egekom = driver.find_element_by_id('ContentPlaceHolder1_DropDownListKommune').send_keys('Egedal')

trs = driver.find_elements(By.TAG_NAME, 'tr')

skoler = [tr.text.split(',  ') for tr in trs]

df = pd.DataFrame(skoler, columns=['Skolenavn', 'Adresse', 'Postnrby', 'Tlf', 'Mail'])
df['Tlf'] = [x.strip('tlf: ') for x in df['Tlf']]
df['Mail'] = [x.strip('e-mail: ') for x in df['Mail']]
print(df)

driver.close()