# Skole scraper
Et lille script til at scrape informationer om skoler fra Undervisningsministeriet.

Bruger [PyDawa](https://github.com/danielarnason/pydawa) til at geokode adresserne.

Scriptet bruger [Selenium](https://selenium-python.readthedocs.io/), så man skal begynde med at downloade en Chromedriver til sit OS [herfra](https://sites.google.com/a/chromium.org/chromedriver/downloads). 

Scriptet går udfra, at driveren ligger i den samme mappe som *scraper.py*.

## Eksempel

```python
from scraper import Skoler

# Erstat 'Egedal' med et andet kommunenavn, uden efterfølgende 'kommune' - f.eks. 'Ballerup' til at få skoler fra Ballerup kommune.
skoler = Skoler('Egedal')
skoler_egedal = skoler.get_skoledata()

df = skoler.create_df(skoler_egedal)
```
Det returnere en pandas dataframe med de informationer fra Undervisningsministeriets hjemmeside.

Hvis man også vil geokode adresserne, så kan man kalde _geokod_ functionen.

```python
df_med_koordinater = skoler.geokod(df)
```
Så har man X/Y koordinater med i sin dataframe.

Hvis man vil skrive resultaterne til en csv fil, som kan læses ind i QGIS, kan man kalde *to_csv* functionen. Csv filen får navnet *skoler_KOMMUNE_kommune.csv* og bliver gemt i samme mappe som *scraper.py* ligger i.

```python
skoler.to_csv(df_med_koordinater)
```
