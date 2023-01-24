import requests
from bs4 import BeautifulSoup
import pandas as pd

class RunAmazon:
    def __init__(self):
        pass

    def scrape(self, url):

        HEADERS = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'),
            'Accept-Language' : 'en-US, en;q=0.5'
        }
        url = url
        html = requests.get(url, headers = HEADERS)
        soup = BeautifulSoup(html.text, "lxml")

        #Titulo
        try:
            title = soup.select_one("span[id='productTitle']").text.strip()  
        except AttributeError:
            title = "*No se encontro el titulo*"	

        #Precio
        try:
            price = soup.select_one("span[class='a-offscreen']").text.strip()
        except AttributeError:
            price = "*No se encontro el precio*"
        
        #Peso
        try:
            table = soup.select('table#productDetails_detailBullets_sections1')[0] 
            rows = table.find_all('tr')
            columns = table.find_all('td')
            table_df = pd.read_html(str(table))[0]  

            weight = table_df[table_df[0]=='Item Weight'][:1][1].to_string().split()
            print(weight)
            medida = weight[2]
            weight = round(float(weight[1]))
            print(weight)

            if medida == "ounces" or medida =="Ounces":
                weight = weight*0.0625

            if weight <= 1:
                envio = "2.75"
                
            if weight > 1:   
                envio = str(weight * 2.75)

        except AttributeError:
            envio = "*no se encontro el precio*"
        except IndexError:
            envio = "*no se encontro el precio*"

        response = "El producto " + title + " de valor " + price + " tiene un costo de envio de " + envio
        return response
    
    

        