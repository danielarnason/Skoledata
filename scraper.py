import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import pydawa

@dataclass
class Skoler:
    kommune: str

    def get_skoledata(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
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
        skolenavn_split = df['Skolenavn'].str.rsplit(n=1, expand=True)
        skolenavn_split[1] = skolenavn_split[1].str.strip('()')
        df.drop('Skolenavn', axis=1, inplace=True)
        df = pd.concat([df, skolenavn_split], axis=1)
        df.rename(columns={0: 'Skolenavn', 1: 'Skolekode'}, inplace=True)
        cols = df.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        df = df[cols]
        return df

    def get_koordinater(self, adresse):
        dawa_adresse = pydawa.Adressesoeg(q=adresse)
        dawa_adresse_data = dawa_adresse.info()
        if len(dawa_adresse_data) > 0:
            return dawa_adresse.get_koordinater(dawa_adresse_data[0])
        else:
            vasket = pydawa.Adressevasker(betegnelse=adresse).info()
            adr_id = vasket['resultater'][0]['adresse']['id']
            adr = pydawa.Adresseopslag(id=adr_id)
            adr_data = adr.info()
            return adr.get_koordinater(adr_data)
    
    def geokod(self, dataframe):
        dataframe['Samlet adresse'] = dataframe[['Adresse', 'Postnrby']].apply(lambda x: ' '.join(x), axis=1)
        dataframe['koordinater'] = dataframe[['Samlet adresse']].apply(lambda x: self.get_koordinater(x.item()), axis=1)
        koordinat_df = pd.DataFrame(dataframe['koordinater'].values.tolist(), index=dataframe.index, columns=['x', 'y'])
        dataframe[['x', 'y']] = koordinat_df[['x', 'y']]
        dataframe.drop(columns=['Samlet adresse', 'koordinater'], axis=1, inplace=True)
        return dataframe
    
    def to_csv(self, dataframe):
        dataframe.to_csv(f'skoler_{self.kommune}_kommune.csv', sep=',')
