#!/usr/bin/env python
# *-* encoding:utf8 *-*
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib


"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
"""


def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]
    return data
    
    
def get_price(symbol): 
    return __request(symbol, 'l1')


def get_change(symbol):
    return __request(symbol, 'c1')
    
    
def get_volume(symbol): 
    return __request(symbol, 'v')


def get_avg_daily_volume(symbol): 
    return __request(symbol, 'a2')
    
    
def get_stock_exchange(symbol): 
    return __request(symbol, 'x')
    
    
def get_market_cap(symbol):
    return __request(symbol, 'j1')
   
   
def get_book_value(symbol):
    return __request(symbol, 'b4')


def get_ebitda(symbol): 
    return __request(symbol, 'j4')
    
    
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')


def get_dividend_yield(symbol): 
    return __request(symbol, 'y')
    
    
def get_earnings_per_share(symbol): 
    return __request(symbol, 'e')


def get_52_week_high(symbol): 
    return __request(symbol, 'k')
    
    
def get_52_week_low(symbol): 
    return __request(symbol, 'j')


def get_50day_moving_avg(symbol): 
    return __request(symbol, 'm3')
    
    
def get_200day_moving_avg(symbol): 
    return __request(symbol, 'm4')
    
    
def get_price_earnings_ratio(symbol): 
    return __request(symbol, 'r')


def get_price_earnings_growth_ratio(symbol): 
    return __request(symbol, 'r5')


def get_price_sales_ratio(symbol): 
    return __request(symbol, 'p5')
    
    
def get_price_book_ratio(symbol): 
    return __request(symbol, 'p6')
       
       
def get_short_ratio(symbol): 
    return __request(symbol, 's7')
    
    
def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data


def get_hist_data(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    lines = urllib.urlopen(url).readlines()
    if len(lines) < 2 : return []
    #Date,Open,High,Low,Close,Volume,AdjClose
    firstline = lines[0]
    firstline = firstline.strip()
    tt = firstline.split(',')
    if string.lower(tt) != 'date':
        return []
    data = []
    for i,line in enumerate(lines):
        if i < 1 : continue
        line = line.strip()
        tt = line.split(',')
        if len(tt) < 7 : continue
    # end for  为完待续
    return data
        


def save_hist(symbol, start_date, end_date,fname='out.txt'):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    contens = urllib.urlopen(url).read()
    f = open(fname,'w')
    f.write(contens)
    f.close()


if __name__ == '__main__':
    print '=========================='
    # DJIA 道琼斯工业指数从 1928-10-01 开始 当日收盘240.01
    #data = get_historical_prices('DJIA','19280101','19281031')
    # ^GSPC 标准普尔指数 S&P 500 Futures Index ER 
    # ^IXIC NASDAQ 综合指数
    # ^N225 日经指数
    # ^HSI  香港恒生指数
    # http://finance.yahoo.com/q?s=%5EN225&ql=0
    # 在上述网站 lookup 输入^即可看到很多的指数!
    # 外汇汇率 http://www.dukascopy.com/swiss/chinese/marketwatch/historical/
    save_hist('^GdSPC','20130101','20130131','out.txt')
    #print get_hist_content('^DJI','20131101','20131130')
