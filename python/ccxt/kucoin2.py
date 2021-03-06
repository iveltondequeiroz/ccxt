# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import AccountSuspended
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce


class kucoin2 (Exchange):

    def describe(self):
        return self.deep_extend(super(kucoin2, self).describe(), {
            'id': 'kucoin2',
            'name': 'KuCoin',
            'countries': ['SC'],
            'rateLimit': 334,
            'version': 'v2',
            'certified': True,
            'comment': 'Platform 2.0',
            'has': {
                'fetchMarkets': True,
                'fetchCurrencies': True,
                'fetchTicker': True,
                'fetchOrderBook': True,
                'fetchOrder': True,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchDepositAddress': True,
                'withdraw': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchBalance': True,
                'fetchTrades': True,
                'fetchMyTrades': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchAccounts': True,
                'fetchFundingFee': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/51909432-b0a72780-23dd-11e9-99ba-73d23c8d4eed.jpg',
                'referral': 'https://www.kucoin.com/ucenter/signup?rcode=E5wkqe',
                'api': {
                    'public': 'https://openapi-v2.kucoin.com',
                    'private': 'https://openapi-v2.kucoin.com',
                },
                'test': {
                    'public': 'https://openapi-sandbox.kucoin.com',
                    'private': 'https://openapi-sandbox.kucoin.com',
                },
                'www': 'https://www.kucoin.com',
                'doc': [
                    'https://docs.kucoin.com',
                ],
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'password': True,
            },
            'api': {
                'public': {
                    'get': [
                        'timestamp',
                        'symbols',
                        'market/orderbook/level{level}',
                        'market/histories',
                        'market/candles',
                        'market/stats',
                        'currencies',
                        'currencies/{currency}',
                    ],
                    'post': [
                        'bullet-public',
                    ],
                },
                'private': {
                    'get': [
                        'accounts',
                        'accounts/{accountId}',
                        'accounts/{accountId}/ledgers',
                        'accounts/{accountId}/holds',
                        'deposit-addresses',
                        'deposits',
                        'withdrawals',
                        'withdrawals/quotas',
                        'orders',
                        'orders/{orderId}',
                        'fills',
                    ],
                    'post': [
                        'accounts',
                        'accounts/inner-transfer',
                        'deposit-addresses',
                        'withdrawals',
                        'orders',
                        'bullet-private',
                    ],
                    'delete': [
                        'withdrawals/{withdrawalId}',
                        'orders/{orderId}',
                    ],
                },
            },
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '8h': '8hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
            },
            'exceptions': {
                '400': BadRequest,
                '401': AuthenticationError,
                '403': NotSupported,
                '404': NotSupported,
                '405': NotSupported,
                '429': DDoSProtection,
                '500': ExchangeError,
                '503': ExchangeNotAvailable,
                '200004': InsufficientFunds,
                '300000': InvalidOrder,
                '400001': AuthenticationError,
                '400002': InvalidNonce,
                '400003': AuthenticationError,
                '400004': AuthenticationError,
                '400005': AuthenticationError,
                '400006': AuthenticationError,
                '400007': AuthenticationError,
                '400008': NotSupported,
                '400100': ArgumentsRequired,
                '411100': AccountSuspended,
                '500000': ExchangeError,
                'order_not_exist': OrderNotFound,  # {"code":"order_not_exist","msg":"order_not_exist"} ¯\_(ツ)_/¯
            },
            'options': {
                'version': 'v1',
                'symbolSeparator': '-',
            },
        })

    def nonce(self):
        return self.milliseconds()

    def load_time_difference(self):
        response = self.publicGetTimestamp()
        after = self.milliseconds()
        kucoinTime = self.safe_integer(response, 'data')
        self.options['timeDifference'] = int(after - kucoinTime)
        return self.options['timeDifference']

    def fetch_markets(self, params={}):
        response = self.publicGetSymbols(params)
        #
        # {quoteCurrency: 'BTC',
        #   symbol: 'KCS-BTC',
        #   quoteMaxSize: '9999999',
        #   quoteIncrement: '0.000001',
        #   baseMinSize: '0.01',
        #   quoteMinSize: '0.00001',
        #   enableTrading: True,
        #   priceIncrement: '0.00000001',
        #   name: 'KCS-BTC',
        #   baseIncrement: '0.01',
        #   baseMaxSize: '9999999',
        #   baseCurrency: 'KCS'}
        #
        responseData = response['data']
        result = {}
        for i in range(0, len(responseData)):
            entry = responseData[i]
            id = entry['name']
            baseId = entry['baseCurrency']
            quoteId = entry['quoteCurrency']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            active = entry['enableTrading']
            baseMax = self.safe_float(entry, 'baseMaxSize')
            baseMin = self.safe_float(entry, 'baseMinSize')
            quoteMax = self.safe_float(entry, 'quoteMaxSize')
            quoteMin = self.safe_float(entry, 'quoteMinSize')
            priceIncrement = self.safe_float(entry, 'priceIncrement')
            precision = {
                'amount': -math.log10(self.safe_float(entry, 'quoteIncrement')),
                'price': -math.log10(priceIncrement),
            }
            limits = {
                'amount': {
                    'min': quoteMin,
                    'max': quoteMax,
                },
                'price': {
                    'min': max(baseMin / quoteMax, priceIncrement),
                    'max': baseMax / quoteMin,
                },
            }
            result[symbol] = {
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'active': active,
                'precision': precision,
                'limits': limits,
                'info': entry,
            }
        return result

    def fetch_currencies(self, params={}):
        response = self.publicGetCurrencies(params)
        #
        # {precision: 10,
        #   name: 'KCS',
        #   fullName: 'KCS shares',
        #   currency: 'KCS'}
        #
        responseData = response['data']
        result = {}
        for i in range(0, len(responseData)):
            entry = responseData[i]
            id = self.safe_string(entry, 'name')
            name = entry['fullName']
            code = self.common_currency_code(id)
            precision = self.safe_integer(entry, 'precision')
            result[code] = {
                'id': id,
                'name': name,
                'code': code,
                'precision': precision,
                'info': entry,
            }
        return result

    def fetch_accounts(self, params={}):
        response = self.privateGetAccounts(params)
        responseData = response['data']
        result = []
        for i in range(0, len(responseData)):
            entry = responseData[i]
            accountId = entry['id']
            result.append({
                'id': accountId,
                'type': self.safe_string(entry, 'type'),  # main or trade
                'currency': None,
                'info': entry,
            })
        return result

    def fetch_funding_fee(self, code, params={}):
        currencyId = self.currencyId(code)
        request = {
            'currency': currencyId,
        }
        response = self.privateGetWithdrawalsQuotas(self.extend(request, params))
        data = response['data']
        withdrawFees = {}
        withdrawFees[code] = self.safe_float(data, 'withdrawMinFee')
        return {
            'info': response,
            'withdraw': withdrawFees,
            'deposit': {},
        }

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "symbol": "ETH-BTC",
        #         "high": "0.1",
        #         "vol": "3891.5909166",
        #         "low": "0.024",
        #         "changePrice": "0.031809",
        #         "changeRate": "31809",
        #         "close": "0.03181",
        #         "volValue": "119.5545894397034",
        #         "open": "0.000001",
        #     }
        #
        change = self.safe_float(ticker, 'changePrice')
        percentage = self.safe_float(ticker, 'changeRate')
        open = self.safe_float(ticker, 'open')
        last = self.safe_float(ticker, 'close')
        high = self.safe_float(ticker, 'high')
        low = self.safe_float(ticker, 'low')
        baseVolume = self.safe_float(ticker, 'vol')
        quoteVolume = self.safe_float(ticker, 'volValue')
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': high,
            'low': low,
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetMarketStats(self.extend(request, params))
        #
        #     {
        #         "code": "200000",
        #         "data": {
        #             "symbol": "ETH-BTC",
        #             "high": "0.1",
        #             "vol": "3891.5909166",
        #             "low": "0.024",
        #             "changePrice": "0.031809",
        #             "changeRate": "31809",
        #             "close": "0.03181",
        #             "volValue": "119.5545894397034",
        #             "open": "0.000001",
        #         },
        #     }
        #
        return self.parse_ticker(response['data'], market)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        #
        #   [["1545904980",             #Start time of the candle cycle
        #       "0.058",                  #opening price
        #       "0.049",                  #closing price
        #       "0.058",                  #highest price
        #       "0.049",                  #lowest price
        #       "0.018",                  #Transaction amount
        #       "0.000945"], ...]       #Transaction volume
        #
        timestamp = self.safe_integer(ohlcv, 0)
        open = self.safe_float(ohlcv, 1)
        close = self.safe_float(ohlcv, 2)
        high = self.safe_float(ohlcv, 3)
        low = self.safe_float(ohlcv, 4)
        volume = self.safe_float(ohlcv, 6)
        return [timestamp, open, high, low, close, volume]

    def fetch_ohlcv(self, symbol, timeframe='15m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        request = {
            'symbol': marketId,
            'endAt': self.seconds(),  # required param
            'type': self.timeframes[timeframe],
        }
        if since is not None:
            request['startAt'] = int(math.floor(since / 1000))
        response = self.publicGetMarketCandles(self.extend(request, params))
        responseData = response['data']
        return self.parse_ohlcvs(responseData, market, timeframe, since, limit)

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currencyId = self.currencyId(code)
        request = {'currency': currencyId}
        response = self.privateGetDepositAddresses(self.extend(request, params))
        data = self.safe_value(response, 'data')
        address = self.safe_string(data, 'address')
        tag = self.safe_string(data, 'memo')
        self.check_address(address)
        return {
            'info': response,
            'currency': code,
            'address': address,
            'tag': tag,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        request = {'symbol': marketId, 'level': 3}
        response = self.publicGetMarketOrderbookLevelLevel(self.extend(request, params))
        #
        # {sequence: '1547731421688',
        #   asks: [['5c419328ef83c75456bd615c', '0.9', '0.09'], ...],
        #   bids: [['5c419328ef83c75456bd615c', '0.9', '0.09'], ...],}
        #
        responseData = response['data']
        timestamp = self.safe_integer(responseData, 'sequence')
        return self.parse_order_book(responseData, timestamp, 'bids', 'asks', 1, 2)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        # required param, cannot be used twice
        clientOid = self.uuid()
        request = {
            'clientOid': clientOid,
            'price': price,
            'side': side,
            'size': amount,
            'symbol': marketId,
            'type': type,
        }
        response = self.privatePostOrders(self.extend(request, params))
        responseData = response['data']
        return {
            'id': responseData['orderId'],
            'symbol': symbol,
            'type': type,
            'side': side,
            'status': 'open',
            'clientOid': clientOid,
            'info': responseData,
        }

    def cancel_order(self, id, symbol=None, params={}):
        request = {'orderId': id}
        response = self.privateDeleteOrdersOrderId(self.extend(request, params))
        return response

    def fetch_orders_by_status(self, status, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'status': status,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetOrders(self.extend(request, params))
        responseData = self.safe_value(response, 'data', {})
        orders = self.safe_value(responseData, 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('done', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('active', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        request = {
            'orderId': id,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privateGetOrdersOrderId(self.extend(request, params))
        responseData = response['data']
        return self.parse_order(responseData, market)

    def parse_order(self, order, market=None):
        #
        #   {"id": "5c35c02703aa673ceec2a168",
        #     "symbol": "BTC-USDT",
        #     "opType": "DEAL",
        #     "type": "limit",
        #     "side": "buy",
        #     "price": "10",
        #     "size": "2",
        #     "funds": "0",
        #     "dealFunds": "0.166",
        #     "dealSize": "2",
        #     "fee": "0",
        #     "feeCurrency": "USDT",
        #     "stp": "",
        #     "stop": "",
        #     "stopTriggered": False,
        #     "stopPrice": "0",
        #     "timeInForce": "GTC",
        #     "postOnly": False,
        #     "hidden": False,
        #     "iceberge": False,
        #     "visibleSize": "0",
        #     "cancelAfter": 0,
        #     "channel": "IOS",
        #     "clientOid": "",
        #     "remark": "",
        #     "tags": "",
        #     "isActive": False,
        #     "cancelExist": False,
        #     "createdAt": 1547026471000}
        #
        symbol = None
        marketId = self.safe_string(order, 'symbol')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                baseId, quoteId = marketId.split('-')
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
            market = self.safe_value(self.markets_by_id, marketId)
        if symbol is None:
            if market is not None:
                symbol = market['symbol']
        orderId = self.safe_string(order, 'id')
        type = self.safe_string(order, 'type')
        timestamp = self.safe_string(order, 'createdAt')
        datetime = self.iso8601(timestamp)
        price = self.safe_float(order, 'price')
        side = self.safe_string(order, 'side')
        feeCurrencyId = self.safe_string(order, 'feeCurrency')
        feeCurrency = self.common_currency_code(feeCurrencyId)
        fee = self.safe_float(order, 'fee')
        amount = self.safe_float(order, 'size')
        filled = self.safe_float(order, 'dealSize')
        remaining = amount - filled
        # bool
        status = 'open' if order['isActive'] else 'closed'
        fees = {
            'currency': feeCurrency,
            'cost': fee,
        }
        return {
            'id': orderId,
            'symbol': symbol,
            'type': type,
            'side': side,
            'amount': amount,
            'price': price,
            'filled': filled,
            'remaining': remaining,
            'timestamp': timestamp,
            'datetime': datetime,
            'fee': fees,
            'status': status,
            'info': order,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetFills(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = self.safe_value(data, 'items', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startAt'] = int(math.floor(since / 1000))
        if limit is not None:
            request['pageSize'] = limit
        response = self.publicGetMarketHistories(self.extend(request, params))
        #     {
        #         "code": "200000",
        #         "data": [
        #             {
        #                 "sequence": "1548764654235",
        #                 "side": "sell",
        #                 "size":"0.6841354",
        #                 "price":"0.03202",
        #                 "time":1548848575203567174
        #             }
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'data', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "sequence": "1548764654235",
        #         "side": "sell",
        #         "size":"0.6841354",
        #         "price":"0.03202",
        #         "time":1548848575203567174
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "symbol":"BTC-USDT",
        #         "tradeId":"5c35c02709e4f67d5266954e",
        #         "orderId":"5c35c02703aa673ceec2a168",
        #         "counterOrderId":"5c1ab46003aa676e487fa8e3",
        #         "side":"buy",
        #         "liquidity":"taker",
        #         "forceTaker":true,
        #         "price":"0.083",
        #         "size":"0.8424304",
        #         "funds":"0.0699217232",
        #         "fee":"0",
        #         "feeRate":"0",
        #         "feeCurrency":"USDT",
        #         "stop":"",
        #         "type":"limit",
        #         "createdAt":1547026472000
        #     }
        #
        symbol = None
        marketId = self.safe_string(trade, 'symbol')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                baseId, quoteId = marketId.split('-')
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
            market = self.safe_value(self.markets_by_id, marketId)
        if symbol is None:
            if market is not None:
                symbol = market['symbol']
        id = self.safe_string(trade, 'tradeId')
        if id is not None:
            id = str(id)
        orderId = self.safe_string(trade, 'orderId')
        amount = self.safe_float(trade, 'size')
        timestamp = self.safe_integer(trade, 'time')
        if timestamp is not None:
            timestamp = int(timestamp / 1000000)
        else:
            timestamp = self.safe_integer(trade, 'createdAt')
        price = self.safe_float(trade, 'price')
        side = self.safe_string(trade, 'side')
        fee = {
            'cost': self.safe_float(trade, 'fee'),
            'rate': self.safe_float(trade, 'feeRate'),
            'feeCurrency': self.safe_string(trade, 'feeCurrency'),
        }
        type = self.safe_string(trade, 'type')
        cost = self.safe_float(trade, 'funds')
        if amount is not None:
            if price is not None:
                cost = amount * price
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        self.check_address(address)
        currency = self.currencyId(code)
        request = {
            'currency': currency,
            'address': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostWithdrawal(self.extend(request, params))
        #
        # {"withdrawalId": "5bffb63303aa675e8bbe18f9"}
        #
        responseData = response['data']
        return {
            'id': self.safe_string(responseData, 'withdrawalId'),
            'info': responseData,
        }

    def parse_transaction_status(self, status):
        statuses = {
            'SUCCESS': 'ok',
            'PROCESSING': 'ok',
            'FAILURE': 'failed',
        }
        return self.safe_string(statuses, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # Deposits
        #   {"address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
        #     "memo": "5c247c8a03aa677cea2a251d",
        #     "amount": 1,
        #     "fee": 0.0001,
        #     "currency": "KCS",
        #     "isInner": False,
        #     "walletTxId": "5bbb57386d99522d9f954c5a@test004",
        #     "status": "SUCCESS",
        #     "createdAt": 1544178843000,
        #     "updatedAt": 1544178891000}
        # Withdrawals
        #   {"id": "5c2dc64e03aa675aa263f1ac",
        #     "address": "0x5bedb060b8eb8d823e2414d82acce78d38be7fe9",
        #     "memo": "",
        #     "currency": "ETH",
        #     "amount": 1.0000000,
        #     "fee": 0.0100000,
        #     "walletTxId": "3e2414d82acce78d38be7fe9",
        #     "isInner": False,
        #     "status": "FAILURE",
        #     "createdAt": 1546503758000,
        #     "updatedAt": 1546504603000}
        #
        code = None
        currencyId = self.safe_string(transaction, 'currency')
        currency = self.safe_value(self.currencies_by_id, currencyId)
        if currency is not None:
            code = currency['code']
        else:
            code = self.common_currency_code(currencyId)
        address = self.safe_string(transaction, 'address')
        amount = self.safe_float(transaction, 'amount')
        txid = self.safe_string(transaction, 'walletTxId')
        type = txid is 'withdrawal' if None else 'deposit'
        rawStatus = self.safe_string(transaction, 'status')
        status = self.parse_transaction_status(rawStatus)
        fees = {
            'cost': self.safe_float(transaction, 'fee'),
        }
        if fees['cost'] is not None and amount is not None:
            fees['rate'] = fees['cost'] / amount
        tag = self.safe_string(transaction, 'memo')
        timestamp = self.safe_integer_2(transaction, 'updatedAt', 'createdAt')
        datetime = self.iso8601(timestamp)
        return {
            'address': address,
            'tag': tag,
            'currency': code,
            'amount': amount,
            'txid': txid,
            'type': type,
            'status': status,
            'fee': fees,
            'timestamp': timestamp,
            'datetime': datetime,
            'info': transaction,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetDeposits(self.extend(request, params))
        #
        # paginated
        # {code: '200000',
        #   data:
        #    {totalNum: 0,
        #      totalPage: 0,
        #      pageSize: 10,
        #      currentPage: 1,
        #      items: [...]
        #     }}
        #
        responseData = response['data']['items']
        return self.parseTransactions(responseData, currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetWithdrawals(self.extend(request, params))
        #
        # paginated
        # {code: '200000',
        #   data:
        #    {totalNum: 0,
        #      totalPage: 0,
        #      pageSize: 10,
        #      currentPage: 1,
        #      items: [...]} }
        #
        responseData = response['data']['items']
        return self.parseTransactions(responseData, currency, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        request = {
            'type': 'trade',
        }
        response = self.privateGetAccounts(self.extend(request, params))
        responseData = response['data']
        result = {'info': responseData}
        for i in range(0, len(responseData)):
            entry = responseData[i]
            currencyId = entry['currency']
            code = self.common_currency_code(currencyId)
            account = {}
            account['total'] = self.safe_float(entry, 'balance', 0)
            account['free'] = self.safe_float(entry, 'available', 0)
            account['used'] = self.safe_float(entry, 'holds', 0)
            result[code] = account
        return self.parse_balance(result)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        #
        # the v2 URL is https://openapi-v2.kucoin.com/api/v1/endpoint
        #                                †                 ↑
        #
        endpoint = '/api/' + self.options['version'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        endpart = ''
        headers = headers is not headers if None else {}
        if query:
            if method != 'GET':
                body = self.json(query)
                endpart = body
                headers['Content-Type'] = 'application/json'
            else:
                endpoint += '?' + self.urlencode(query)
        url = self.urls['api'][api] + endpoint
        if api == 'private':
            self.check_required_credentials()
            timestamp = str(self.nonce())
            headers = self.extend({
                'KC-API-KEY': self.apiKey,
                'KC-API-TIMESTAMP': timestamp,
                'KC-API-PASSPHRASE': self.password,
            }, headers)
            payload = timestamp + method + endpoint + endpart
            headers['KC-API-SIGN'] = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if not response:
            return
        #
        # bad
        # {"code":"400100","msg":"validation.createOrder.clientOidIsRequired"}
        # good
        # {code: '200000',
        #   data: {...},}
        #
        errorCode = self.safe_string(response, 'code')
        if errorCode in self.exceptions:
            Exception = self.exceptions[errorCode]
            message = self.safe_string(response, 'msg', '')
            raise Exception(self.id + ' ' + message)
