import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_skoledata(kommune):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://statistik.uni-c.dk/instregvisning/oversigt.aspx')

    grundskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt1')
    grundskoler.click()

    folkeskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt4')
    folkeskoler.click()

    driver.find_element_by_id('ContentPlaceHolder1_DropDownListKommune').send_keys(kommune)

    trs = driver.find_elements(By.TAG_NAME, 'tr')

    # driver.close()

    return [tr.text.split(',  ') for tr in trs]

def create_df(skoledata):
    df = pd.DataFrame(skoledata, columns=['Skolenavn', 'Adresse', 'Postnrby', 'Tlf', 'Mail'])
    df['Tlf'] = [x.strip('tlf: ') for x in df['Tlf']]
    df['Mail'] = [x.strip('e-mail: ') for x in df['Mail']]
    df['Skolenavn'] = [' '.join(x.split(' ')[:-1]) for x in df['Skolenavn']]

    return df

if __name__ == "__main__":
    skoler = get_skoledata('Egedal')
    df = create_df(skoler)
    print(df)