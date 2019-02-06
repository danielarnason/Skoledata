import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import pydawa

@dataclass
class Skoler:
    kommune: str

    def get_skoledata(self):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://statistik.uni-c.dk/instregvisning/oversigt.aspx')

        grundskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt1')
        grundskoler.click()

        folkeskoler = driver.find_element_by_id('ContentPlaceHolder1_TreeViewInstt4')
        folkeskoler.click()

        driver.find_element_by_id('ContentPlaceHolder1_DropDownListKommune').send_keys(self.kommune)

        trs = driver.find_elements(By.TAG_NAME, 'tr')

        return [tr.text.split(',  ') for tr in trs]

    def create_df(self, skoledata):
        df = pd.DataFrame(skoledata, columns=['Skolenavn', 'Adresse', 'Postnrby', 'Tlf', 'Mail'])
        df['Tlf'] = [x.strip('tlf: ') for x in df['Tlf']]
        df['Mail'] = [x.strip('e-mail: ') for x in df['Mail']]
        df['Skolenavn'] = [' '.join(x.split(' ')[:-1]) for x in df['Skolenavn']]

        return df

    def get_koordinater(self, adresse):
        dawa_adresse = pydawa.Adressesoeg(adresse).info()
        if len(dawa_adresse) > 0:
            return (dawa_adresse[0]['x'], dawa_adresse[0]['y'])
        else:
            vasket = pydawa.Adressevasker(adresse).info()
            adr_id = vasket['resultater'][0]['adresse']['id']
            adr = pydawa.Adresseopslag(adr_id).info()
            return (adr['x'], adr['y'])
    
    def geokod(self, dataframe):
        dataframe['Samlet adresse'] = dataframe[['Adresse', 'Postnrby']].apply(lambda x: ' '.join(x), axis=1)
        dataframe['koordinater'] = dataframe[['Samlet adresse']].apply(lambda x: self.get_koordinater(x), axis=1)
        print(dataframe)