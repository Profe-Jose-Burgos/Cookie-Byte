import requests
from bs4 import BeautifulSoup
import pandas as pd

class RunAmazon:
    def scrape(url):
        HEADERS = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'),
            'Accept-Language' : 'en-US, en;q=0.5'
        }

        url = url

        html = requests.get(url, headers = HEADERS)
        soup = BeautifulSoup(html.text)

        #Buscar titulo y precio del articulo
        title = soup.select_one("span[id='productTitle']").text.strip()
        price = soup.select_one("span[class='a-offscreen']").text.strip()

        #Buscar peso del producto
        table = soup.select('table#productDetails_detailBullets_sections1')[0] 
        rows = table.find_all('tr')
        columns = table.find_all('td')
        table_df = pd.read_html(str(table))[0]  

        weight = table_df[table_df[0]=='Item Weight'][:1][1].to_string().split()
        weight = float(weight[1]) 
        precio = weight * 2.75
        
        response = "El producto " + title + "de valor " + price + " tiene un costo de envio de " + precio
        return response
    
    

        