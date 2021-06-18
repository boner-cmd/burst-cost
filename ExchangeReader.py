import base64
import requests
import json
import hashlib
import hmac
from time import time

# btdex URL assumes local btdex instance, will use different URL for production
# using BTC pair on btdex because it has highest volume

api_urls = {'stex': "https://api3.stex.com/public/ticker/1040",
            'bittrex': "https://api.bittrex.com/v3",
            'btdex': "http://localhost:9000/api/v1/orderbook/BTC_BURST"}

exchangeResponses = {}
stexResponse = {}
bittrexResponse = {}
response = ""

# get Stex first

try:
    response = requests.get(api_urls['stex'])
except ConnectionError:
    print("Connection error to Stex")
try:
    exchangeResponses['stex'] = response.json()  # this will create a dictionary of dictionaries
except json.JSONDecodeError:  # test to make sure this catches the correct exception
    print("Response body does not contain valid JSON.")

# get btdex next

try:
    response = requests.get(api_urls['btdex'])
except ConnectionError:
    print("Connection error to Stex")
try:
    exchangeResponses['stex'] = response.json()
except json.JSONDecodeError:
    print("Response body does not contain valid JSON.")

# get... wherever was just added

# get Bittrex last
# request info from Bittrex, conforming to their API standards

bittrex_uri = "https://api.bittrex.com/v3"
bittrex_content = "application/json"
bittrex_market_summary = "/markets/{marketSymbol}/summary"  # need to find out what Burst market symbol is
bittrex_market_ticker = "/markets/{marketSymbol}/ticker"  # need to find out what Burst market symbol is

bittrex_key = ""
bittrex_secret = b""

bittrex_timestamp = int(time() * 1000)
bittrex_request_body = ""
bittrex_content_hash = hashlib.sha512(bittrex_request_body)
bittrex_presign = str(bittrex_timestamp) + bittrex_uri + bittrex_market_ticker + "GET" + str(bittrex_content_hash)
bittrex_signature_prep = hmac.new(bittrex_secret, bittrex_presign, digestmod=hashlib.sha512).digest()
bittrex_signature = base64.b64encode(bittrex_signature_prep)
headers = {'Api-Key': bittrex_key,
           'Api-Timestamp': bittrex_timestamp,
           'Api-Content-Hash': bittrex_content_hash,
           'Api-Signature': bittrex_signature}

try:
    response = requests.get(bittrex_uri + bittrex_market_ticker, headers=headers)
except ConnectionError:  # test to make sure no other exceptions are thrown
    print("Connection error to Bittrex")
try:
    exchangeResponses['bittrex'] = response.json()
except json.JSONDecodeError:
    print("Response body does not contain valid JSON.")

# parse the results from Stex
interestingKeys = {'ask', 'bid', 'last', 'low', 'high'}
stexRates = {}
for key in interestingKeys:
    value: str = exchangeResponses['stex'][key]
    stexResponse[key] = value

currencies = {'USD', 'EUR', 'UAH', 'AUD', 'IDR', 'CNY', 'KRW', 'JPY', 'VND', 'INR', 'GBP', 'GBP', 'CAD', 'BRL', 'RUB'}

for currency in currencies:
    rate: int = exchangeResponses['stex'][currency]
    stexRates[currency] = rate

stexResponse["fiatsRate"] = stexRates

# parse the results from bittrex

# parse the results from btdex
# the only information we can get from btdex is bids and asks for each pair
# we need to use a BTC exchange rate to convert those to fiat
