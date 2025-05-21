from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

from zapimoveis_scraper.enums import ZapAcao, ZapTipo
from zapimoveis_scraper.item import ZapItem
from collections import defaultdict
import re

__all__ = [
    # Main search function.
    'search',
]


# URL templates to make urls searches.
url_home = "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/?pagina=%(page)s"

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    return response

def search(localization='go+goiania++setor-marista', num_pages=1, acao=ZapAcao.aluguel.value, tipo=ZapTipo.apartamentos.value, time_to_wait=10):
    page = 1
    items = []
    df = pd.DataFrame()
    while page <= num_pages:
        html = get_page(url_home % vars())
        soup = BeautifulSoup(html, 'html.parser')
        listings2 = get_listings2(soup)

        #
        # listings = get_listings(soup)
        #
        # for listing in listings:
        #     if 'type' not in listing or listing['type'] != 'nearby':
        #         items.append(get_ZapItem(listing))
        df = pd.concat([df, listings2], ignore_index=True)
        page += 1
        randwait = np.random.randint(1,3)
        time.sleep(time_to_wait + randwait)

    #if dictionary_out:
    #    return convert_dict(items)

    return df


def search_yield(localization='go+goiania++setor-marista', num_pages=1,
           acao=ZapAcao.aluguel.value, tipo=ZapTipo.apartamentos.value, time_to_wait=10):
    page = 1
    while page <= num_pages:
        html = get_page(url_home % vars())
        soup = BeautifulSoup(html, 'html.parser')
        listings2 = get_listings2(soup)

        # Retorna os dados dessa página
        yield listings2

        page += 1
        randwait = np.random.randint(1, 3)
        time.sleep(time_to_wait + randwait)


def get_listings2(soup):
    df = pd.DataFrame()

    for i in soup.find_all('li', attrs={'data-cy': 'rp-property-cd'}):
        try:
            line_dic = {"URL"}
            u = i.find('a')
            url = u.attrs['href']
            line_dic = {"URL": url}

            for k in i.find_all("div"):
                try:
                    neighborhood_tag = k.find("h2", attrs={"data-cy": "rp-cardProperty-location-txt"})
                    neighborhood = neighborhood_tag.text.split(',')[0].strip()
                    city = neighborhood_tag.text.split(',')[1].strip()

                    line_dic["neighborhood"] = neighborhood.replace('Apartamento para alugar em ','')
                    line_dic["city"] = city

                except:
                    pass

                try:
                    price_tag= k.find("div", attrs={"data-cy": "rp-cardProperty-price-txt"})
                    arr_ = price_tag.find_all("p")

                    for valor in arr_[0].text.split("/"):
                        if "R$" in valor:
                            line_dic["price"] = float(re.findall(r'\d+\.?\d*', valor)[0].replace('.',''))
                        else:
                            line_dic["period"] = valor


                    for valor in arr_[1].text.split('•'):
                            if "Cond." in valor:
                                line_dic["Condo"] = float(re.findall(r'\d+\.?\d*', valor)[0].replace('.',''))
                            if "IPTU" in valor:
                                line_dic["IPTU"] = float(re.findall(r'\d+\.?\d*', valor)[0].replace('.',''))

                except:
                    pass

                for j in k.find_all("li"):
                    try:
                        tag= j.attrs['data-cy'].replace("rp-cardProperty-","").replace("-txt","")

                        line_dic[tag] = int(re.findall(r'\d+\.?\d*', j.text)[0])
                    except:
                        pass

                for j in k.find_all("p"):
                    try:
                        tag = j.attrs['data-cy'].replace("rp-cardProperty-", "").replace("-txt", "")

                        line_dic[tag] = j.text
                    except:
                        pass


                    #print(f" {tag}:{j.text}")
                    #if "Quantidade de quartos" in str(j):
                    #    print(j.text)
            #print(line_dic)
            df = pd.concat([df, pd.DataFrame([line_dic])], ignore_index=True)
        except:
            pass

    return df