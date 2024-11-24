import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import json
import traceback

def get_HTML(url):
    response = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
    if(response.status_code!=200):
        raise Exception("Wrong status code")
    return BeautifulSoup(response.text, features="html.parser")

def shopify(url):
    soup = get_HTML(url)
    deran = soup.find('script', text=re.compile(r"d\(d,e,r,a,n\).*")).text
    if("collection_viewed" in deran):
        item_data = json.loads(deran.split("\"collection_viewed\", ")[1].split(");")[0])['collection']['productVariants']
    elif("initData" in deran):
        item_data = json.loads(deran.split("initData: ")[1].split(",},")[0])['productVariants']
    outputs=[]
    parsed_items=[]
    for item in item_data:
        if(item['product']['title'] in parsed_items):
            continue
        parsed_items.append(item['product']['title'])
        outputs.append({'type':'offer', 'name':item['product']['title'], 'price':item['price']['amount'], 'currency':item['price']['currencyCode']})
    return list(outputs)

def parse_woocommerce_product(item):
    tot_offers=0
    min_price=10000.0
    max_price=0.0
    priceCurrency='EUR'
    for offer in item['offers']:
        if(offer['@type']=="AggregateOffer"):
            tot_offers+=offer['offerCount']
            if(float(offer['lowPrice'])<min_price):
                min_price=float(offer['lowPrice'])
            if(float(offer['highPrice'])>max_price):
                max_price=float(offer['highPrice'])
        else:
            tot_offers+=1
            if(float(offer['price'])<min_price):
                min_price=float(offer['price'])
            if float(offer['price'])>max_price:
                max_price=float(offer['price'])
        if(offer['priceCurrency']!=priceCurrency):
            priceCurrency=offer['priceCurrency']
    output=None
    if(tot_offers>0):
        output = {'type':'multipleOffers', 'name':item['name'], 'currency': priceCurrency, 'tot_offers': tot_offers, 'min_price':min_price, 'max_price':max_price}
    return output

def woocommerce(url):
    soup = get_HTML(url)
    item_data = json.loads(soup.find('script', type='application/ld+json').text)
    if('@graph' in item_data):
        item_data = item_data['@graph']
    outputs=[]
    if(isinstance(item_data, list)):
        for item in item_data:
            if(item['@type']=='Product'):
                output = parse_woocommerce_product(item)
                if(output!=None):
                    outputs.append(output)
    else:
        if(item_data['@type']=='Product'):
            output = parse_woocommerce_product(item_data)
            if(output!=None):
                outputs.append(output)
    return list(outputs)


def antikorp(url):
    soup = get_HTML(url)
    item_data = json.loads(soup.find('script', text=re.compile(r".*function\(w,d,s,l,i\).*")).text.split("let cdcDatalayer = ")[1].split(";")[0])['ecommerce']
    outputs=[]
    for item in item_data['items']:
        outputs.append({'type':'offer', 'name':item['item_name'], 'price':item['price'], 'currency':item_data['currency']})
    return list(outputs)

domain_type_switch={'inariorganics.it':woocommerce, 'piercingmed.com':woocommerce, 'www.neometal.com':shopify, 'antikorp.com':antikorp, 'implantgrade.com':shopify}


def get_price(url):
    try:
        o = urlparse(url)
        if(o.hostname not in domain_type_switch):
            return {'success':False, 'error':f'Sito non supportato: {o.hostname}'}
        else:
            return {'success':True, 'data': domain_type_switch[o.hostname](url)}
    except Exception as ex:
        traceback.print_exc()
        return {'success':False, 'error':f'Errore generico: {ex}'}



from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')

CORS(app)

@app.route('/')
def serve_react_app():
    # This will return the React index.html file
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route("/extract/<path:url>")
def extract(url):
    app.logger.debug(f"Got request for {url}")
    response = get_price(url)
    app.logger.debug(f"Response is {response}")
    return response




if __name__=="__main__":
    while(True):
        url=input("> ")
        print(get_price(url))