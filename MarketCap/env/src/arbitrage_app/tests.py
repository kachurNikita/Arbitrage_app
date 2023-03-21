import unittest
from main import MarketCap
import requests
from main import base_url, coin_url

class TestArbitrageApp(unittest.TestCase):
    def setUp(self):
        self.market_cap = MarketCap('Coin Geko')
        self.response_base = requests.get(base_url)
        self.response_base = self.response_base.json()
        self.response_coin_id = requests.get(coin_url.format(coinId = 'bitcoin')).json()
        self.prices = [
            {
                'converted_last': {
                    'usd': 1000
                },
                'market': {
                    'name': 'Bybit'
                },
                'converted_volume': {
                    'usd': 0000
                }
            },
        ]
        self.min_price = {
            'converted_last': {
                'usd': 1000
            },
            'market': {
                'name': 'Bybit'
            },
            'converted_volume': {
                'usd': 0000
            }
        }
        self.max_prices = [
            {
                'converted_last': {
                    'usd': 2000
                },
                'market': {
                    'name': 'Binance'
                }
            },
            {
                'converted_last': {
                    'usd': 3000
                },
                'market': {
                    'name': 'Whitebit'
                }
            },
        ]
          
    def test_get_currency_id(self):
        # Get id by name
        currency = 'Bitcoin'
        parameter_name = 'name'
        result = self.market_cap.get_currency_id(currency, self.response_base, parameter_name)
        self.assertEqual(result, 'bitcoin')
        
        # Get id by symbol
        currency = 'Btc'
        parameter_name = 'symbol'
        result = self.market_cap.get_currency_id(currency, self.response_base, parameter_name)
        self.assertEqual(result, 'bitcoin')
    
    def test_find_min_currency_price(self):
        result = self.market_cap.find_min_currency_price(self.prices)
        self.assertEqual(result, self.min_price)
    
    def test_find_bigger_currencys_price(self):
        result = self.market_cap.find_bigger_currencys_price(self.min_price['converted_last']['usd'], self.prices)
        self.assertEqual(result, [self.prices[1]])
    
    def test_show_arbitrage_variants(self):
        arbitrage_data = {
            'price': self.min_price['converted_last']['usd'],
            'market': self.min_price['market']['name'],
            'volume': self.min_price['converted_volume']['usd'],
            'arb_variants': self.max_prices,
        }
        result = self.market_cap.show_arbitrage_variants(self.min_price, self.max_prices)
        self.assertEqual(result, arbitrage_data)
    
    def test_create_request(self):
        result = self.market_cap.create_request(base_url)
        self.assertEqual(result, self.response_base)
        
unittest.main()
        