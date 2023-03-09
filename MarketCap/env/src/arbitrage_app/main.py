#!/usr/bin/env python3
import argparse
import requests

base_url = 'https://api.coingecko.com/api/v3/coins/list'
coin_url = 'https://api.coingecko.com/api/v3/coins/{coinId}'

parser = argparse.ArgumentParser(description='Command that finds currency by name or symbol and returns current market price')
parser.add_argument('-n', '--name', type=str, metavar='N', help='Enter currency name. Ex: --name bitcoin',)
parser.add_argument('-s', '--symbol', type=str, help='Enter currency symbol. Ex: --symbol eth',)
args = parser.parse_args()

class MarketCap:
    greeting_counter = 0
    matching_parameter = 1.5
    crypto_currencys = {}
    
    def __init__(self, name: any) -> None:
        self.name = name
        self.display_greeting()
        
    def get_currency_data(self, parameter_type, currency):
        currency = currency.lower()
        response = self.create_request(base_url)
        coin_id = self.get_currency_id(currency, response, parameter_type)
        if coin_id:
            arbitrage_data = self.get_currency_info(coin_id, coin_url)
            if arbitrage_data != None:
                min_price_description = f'{currency.title()} minimum value found on {arbitrage_data["market"]} with price: ${arbitrage_data["price"]}, volume: ${arbitrage_data["volume"]}'
                print(min_price_description)
                for max_currency in arbitrage_data['arb_variants']:
                    print(f" Opportunity found on Market: {max_currency['market']['name']}, price: ${max_currency['converted_last']['usd']}," 
                          f"volume: ${max_currency['converted_volume']['usd']}")
        else:
            return 'Currency not found'
                
    def get_currency_id(self, currency, response, parameter_type):
        currency_id = ''
        if response is not None:
            for obj in response:
                if currency == obj[parameter_type].lower():
                    currency_id =  obj['id']
            if currency_id:
                print('ye')
                return currency_id
        else:
            print("Currency not found")

    def get_currency_info(self, coin_id, url):
        response = self.create_request(url, coin_id)
        if response != None:
            coin_detail_list = response['tickers']
            min_price = self.find_min_currency_price(coin_detail_list)
            max_price_list = self.find_bigger_currencys_price(min_price['converted_last']['usd'], coin_detail_list)
            return self.show_arbitrage_variants(min_price, max_price_list)
    
    def find_min_currency_price(self, prices_list):
        min_index = 0
        min_price = prices_list[min_index]['converted_last']['usd']
        for index in range(1, len(prices_list)):
            if min_price > prices_list[index]['converted_last']['usd']:
                min_price = prices_list[index]['converted_last']['usd']
                min_index = index
        return prices_list[min_index]    
    
    def find_bigger_currencys_price(self, min_price, prices_list):
        max_price_list = []
        for index in range(1, len(prices_list)):
            current_difference = 100 * (prices_list[index]['converted_last']['usd'] / min_price) - 100
            if current_difference >= self.matching_parameter:
                max_price_list.append(prices_list[index])
        if max_price_list:
            return max_price_list
    
    def show_arbitrage_variants(self, min_price, max_price):
        arbitrage_data = {
            'price': min_price['converted_last']['usd'],
            'market': min_price['market']['name'],
            'volume': min_price['converted_volume']['usd'],
            'arb_variants': max_price,
        }
        return arbitrage_data
        
    def create_request(self, request_url, payload_arg=None):
        if payload_arg:
            response = requests.get(request_url.format(coinId = payload_arg))
            parsed_response = self.is_response_status_ok(response)
            return parsed_response
        else:
            response = requests.get(request_url)
            parsed_response = self.is_response_status_ok(response)
            return parsed_response

    def is_response_status_ok(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            return self.response_exceptions(response)
        
    def response_exceptions(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.ConnectionError as con_err:
            raise Exception('Server connection error')
        except requests.exceptions.InvalidSchema as invlid_schema:
            raise Exception('No connection addapters were found')
        except requests.exceptions.MissingSchema as miss_schema:
            raise Exception('Url isnot provided')
        except requests.exceptions.HTTPError as http_error:
            raise Exception('To many requests, try later')
            
    def display_greeting(self):
        print('To see available commands type: ./arbittrage_app/pex -h')

market_cap = MarketCap('Coin Geko')

if __name__ == '__main__':
    if args.name:
        parameter_type = 'name' 
        print(market_cap.get_currency_data(parameter_type, args.name))
    elif args.symbol:
        parameter_type = 'symbol'
        print(market_cap.get_currency_data(parameter_type, args.symbol))