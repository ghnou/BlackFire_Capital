from datetime import datetime, timedelta
import cProfile, pstats, io
import pandas as pd
import numpy as np
import calendar


principal_processor = 16
secondary_processor = 5
type_consensus = 'consensus'
type_price_target = 'price_target'
CurrenciesExchangeRatesDBName = 'currency'
StocksMarketDataInfosDBName = 'stocks_infos'

PRINCIPAL_PROCESSOR = 16
SECONDARY_PROCESSOR = 5

TYPE_CONSENSUS = 'consensus'
TYPE_PRICE_TARGET = 'price_target'

CURRENCIES_EXCHANGE_RATES_DB_NAME = 'currency'
CURRENCIES_EXCHANGE_RATES_DB_COL_NAME = 'exchg_rates'

STOCKS_MARKET_DATA_DB_NAME = 'stocks'
STOCKS_MARKET_DATA_INFO_DB_COL_NAME = 'stocks_infos'
SUMMARY_DB_COL_NAME = 'summary'
M_SUMMARY_DB_COL_NAME = 'm_summary'
STOCKS_MARKET_FORECASTS_INFO_DB_COL_NAME = 'forecast_info'

SECTORS_MARKET_DATA_DB_NAME = 'sector'
NAICS = 'naics'
SECTORS_MARKET_DATA_INFO_DB_COL_NAME = 'info'
SECTORS_MARKET_DATA_MAPPING_DB_COL_NAME = 'mapping'

ECONOMICS_ZONES_DB_NAME = 'economics_zones'
ECONOMICS_ZONES_DB_COL_NAME = 'infos'

IO_SUPPLY = 'supply'
IO_DEMAND = 'demand'

COUNTRY_ZONE_AND_EXCHG = [['canada','CAN','CAD','7'], ['united states','USA','USD','11','12','14','17'],
           ['austria', 'AUT', 'EUR', '150', '273'],
           ['belgium', 'BEL', 'EUR', '132', '150', '161', '188', '285', '294'],
           ['denmark', 'DNK', 'DKK', '305', '144'],
           ['finland', 'FIN', 'EUR', '167', '286'],
           ['france', 'FRA', 'EUR', '286', '294', '121', '150', '190', '199', '205', '206', '216', '217', '231'],
           ['germany', 'DEU', 'EUR', '115', '123', '148', '149', '154', '163','165','171','212','257'],
           ['ireland', 'IRL', 'EUR', '150', '172', '173'],
           ['israel', 'ISR', 'ILS', '150', '151', '262', '286'],
           ['italy', 'ITA', 'EUR', '119', '150', '152','160','209','218','230','240','265','267','272','286'],
           ['netherlands', 'NLD', 'EUR', '104', '150', '286','294'],
           ['norway', 'NOR', 'NOK', '224','286'],
           ['portugal', 'PRT', 'EUR', '192', '234'],
           ['spain', 'ESP', 'EUR', '270', '286', '112', '117', '150', '201'],
           ['sweden', 'SWE', 'SEK', '256', '305'],
           ['switzerland', 'CHE', 'CHF', '113', '116','151','159','186','220','254','280'],
           ['united kingdom', 'GBR', 'GBP', '150', '162', '189', '194', '226'],
           ['australia', 'AUS', 'AUD', '101', '106', '126', '169', '207', '232'],
           ['hong kong', 'HKG', 'HKD', '170'],
           ['japan', 'JPN', 'JPY', '153', '156','183','213','227','244','264','293','296'],
           ['new zealand', 'NZL', 'NZD', '108', '225', '277'],
           ['singapore', 'SGP', 'SGD', '251'],
           ['brazil', 'BRA', 'BRL', '238','243'],
           ['chile', 'CHL', 'CLP', '242'],
           ['colombia', 'COL', 'COP', '118'],
           ['mexico', 'MEX', 'MXN', '208'],
           ['peru', 'PER', 'PEN', '191'],
           ['czech republic', 'CZE', 'CZK', '235'],
           ['egypt', 'EGY', 'EGP', '136', '299'],
           ['greece', 'GRC', 'EUR', '107'],
           ['hungary', 'HUN', 'HUF', '134'],
           ['poland', 'POL', 'PLN', '276'],
           ['qatar', 'QAT', 'QAR', '315'],
           ['russia', 'RUS', 'RUB', '211', '224', '255', '275'],
           ['south africa', 'ZAF', 'ZAR', '177'],
           ['turkey', 'TUR', 'TRY', '174'],
           ['united arab emirates', 'ARE', 'AED', '318','323','331'],
           ['china', 'CHN', 'CNY', '249', '250'],
           ['india', 'IND', 'INR', '120', '137', '147', '200', '219'],
           ['indonesia', 'IDN', 'IDR', '175', '258'],
           ['korea', 'KOR', 'KRW', '248', '298'],
           ['malaysia', 'MYS', 'MYR', '304', '181'],
           ['pakistan', 'PAK', 'PKR', '178'],
           ['philippines', 'PHL', 'PHP', '202' ,'203'],
           ['taiwan', 'TWN', 'TWD', '245', '260', '303'],
           ['thailand', 'THA', 'THB', '110']]


def GenerateMonthlyTab(start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    tab = []
    b = False
    for yr in range(start_year, end_year + 1):

        for month in range(1, 13):
            t = str(month)
            if month < 10:
                t = '0'+ str(month)

            date = str(yr) + '-' + t
            if date == start_date:
                b = True
            if b:
                tab.append(date)
            if date == end_date:
                break
    return tab


def GenerateDailyTab(start_date, end_date):
    tab_day = [0, 1, 2, 3, 4]
    timedelta(days=1)
    pos = 0
    tab = [[start_date]]
    to_append = []

    while start_date != end_date:
        pos += 1
        start_date = start_date + timedelta(days=1)
        if pos%7 in tab_day:
            to_append.append(start_date)
            tab.append(to_append)
            to_append = []
        else:
            to_append.append(start_date)

    return tab


def GenerateWorkingDailyTab(start_date, end_date):

    tab_day = [0, 1, 2, 3, 4]
    start = False
    cal = calendar.Calendar()
    tab_date_to_add = []
    print(start_date)
    for yr in range(start_date.year, end_date.year + 1):
        for month in range(1, 13):
            list_mo = list(cal.itermonthdays(yr, month))
            print(list_mo)
            pos = 0
            for day in list_mo:

                if day != 0:
                    if start:
                        if day != 0 and pos%7 in tab_day:
                            tab_date_to_add.append(datetime(yr,month,day,16,0,0,0))
                    if datetime(yr, month, day,16,0,0,0) == start_date:
                        if day != 0 and pos%7 in tab_day:
                            tab_date_to_add.append(datetime(yr,month,day,16,0,0,0))
                        start = True

                    if datetime(yr, month, day,16,0,0,0) == end_date:
                        return tab_date_to_add

                pos += 1


def TestNoneValue(value, v):
    if value is None or np.isnan(value) == True:
        value = v
    return value


def GetListOfAllCusip(tabOfDictStockID):
    t = []
    for infos in tabOfDictStockID:

        if infos['isin'] != None:
            if infos['isin'][0:2] != 'US' and infos['isin'][0:2] != 'CA':
                t.append(infos['isin'])
            else:
                t.append(infos['cusip'])
        elif infos['cusip'] != None:
            t.append(infos['cusip'])

    return t


def GetMeanValueOfPriceRecommendationAgregation(date, cursor, type):
    number = 0
    n_ = 0
    value = 0
    recom = 0
    var = 0

    if type == type_price_target:
        for v in cursor:

            number += 1
            value += v['price_usd']
            act_date = v['date_activate'][:7]
            act_date = act_date[:6] if act_date[-1] == 'J' else act_date

            if act_date != date:
                n_ += 1
                var += float(v['variation'])

        if number != 0:
            var = 0 if n_ == 0 else var / n_
            return {'price_usd': value / number, 'variation': var, 'number': number, 'num_var': n_}
        else:
            return None
    elif type == type_consensus:
        for v in cursor:

            act_date = v['date_activate'][:7]
            act_date = act_date[:6] if act_date[-1] == 'J' else act_date

            number += 1
            recom += float(v['recom'])
            if act_date != date:
                n_ += 1
                var += float(v['variation'])
        try:
            r = var / n_
        except ZeroDivisionError:
            r = None

        if number != 0:
            return {'recom': recom / number, 'variation': r, 'number': number, 'num_var': n_}
        else:
            return None


def GetMeanValueOfSectorAgregation(cursor):


    price_stocks = cursor['stocks']
    n_stocks = 0
    # """{'price_usd', 'n_stocks', 'csho', 'vol', 'ret', 'curr'}"""
    # {'price_usd': value / number, 'variation': var, 'number': number, 'num_var': n_}
    # {'recom': recom / number, 'variation': r, 'number': number, 'num_var': n_}

    entete = ['price_usd', 'csho', 'vol', 'recom', 'recom_var', 'recom_n',
              'recom_n_var', 'price_target', 'price_target_var', 'price_target_n',
              'price_target_n_var', 'price_target_ret']

    tab_value = []

    for value in price_stocks:
        pt = value['price_target']
        consensus = value['consensus']
        t = [value['price_usd'], value['csho'], value['vol'], consensus['recom'],
             consensus['variation'], consensus['number'], consensus['num_var'],
             pt['price_usd'], pt['variation'], pt['number'], pt['num_var'],
             pt['ret']]

        tab_value.append(t)

    tab_value = pd.DataFrame(tab_value, index=None, columns=entete)

    # price

    mask = (np.isnan(tab_value['price_usd']) == False) & (np.isnan(tab_value['csho']) == False)
    t = tab_value[mask]
    try:
        csho = sum(t['csho'])
        price = sum(t['price_usd'] * t['csho']) / csho
    except ZeroDivisionError:
        csho = None
        price = None
    except TypeError:
        csho = None
        price = None

    mask = (np.isnan(tab_value['vol']) == False)
    t = tab_value[mask]
    vol = sum(t['vol'])
    n_stocks = tab_value.shape[0]

    # price target

    mask = (np.isnan(tab_value['price_target']) == False) & (np.isnan(tab_value['csho']) == False)
    t = tab_value[mask]
    csho_pt = sum(t['csho'])
    price_target = sum(t['price_target'] * t['csho']) / csho_pt
    n_pt = t.shape[0]

    mask = (np.isnan(tab_value['price_target_var']) == False) & (np.isnan(tab_value['price_target_n_var']) == False)
    t = tab_value[mask]
    pt_n_var = sum(t['price_target_n_var'])
    pt_var = sum(t['price_target_n_var']*t['price_target_var'])/pt_n_var

    try:
        ret = -1 + price_target/price
    except ZeroDivisionError:
        ret = None
    except TypeError:
        ret = None

    price_target_tab = {'price_usd': price_target, 'chso': csho_pt, 'number':n_pt,
                        'num_var': pt_n_var, 'variation': pt_var, 'ret': ret}

    #consensus

    mask = (np.isnan(tab_value['recom']) == False) & (np.isnan(tab_value['recom_n']) == False)
    t = tab_value[mask]
    cs_n = sum(t['recom_n'])
    cs = sum(t['recom'] * t['recom_n']) / cs_n

    mask = (np.isnan(tab_value['recom_var']) == False) & (np.isnan(tab_value['recom_n_var']) == False)
    t = tab_value[mask]
    cs_n_var = sum(t['recom_n_var'])
    cs_var = sum(t['recom_var'] * t['csho']) / cs_n_var

    consensus_tab = {'recom': cs, 'number': cs_n, 'num_var': cs_n_var, 'variation': cs_var}

    if n_stocks != 0:
        tab_value = [{'price_usd': price, 'csho': csho, 'vol': vol,
                      'n_stocks': n_stocks, 'consensus': consensus_tab,
                      'price_target': price_target_tab}]
    else:
        tab_value = []

    price_naics = cursor['naics']

    entete = ['price_usd', 'csho', 'vol', 'n_stocks', 'recom', 'recom_var', 'recom_n',
              'recom_n_var', 'price_target', 'price_target_var', 'price_target_n',
              'price_target_n_var', 'price_target_ret', 'csho_pt']

    for value in price_naics:
        """{'price_usd', 'n_stocks', 'csho', 'vol', 'ret', 'curr', 'price_target, 'consensus'}"""
        pt = value['price_target']
        consensus = value['consensus']

        t = [value['price_usd'], value['csho'], value['vol'],value['n_stocks'],
             consensus['recom'],consensus['variation'], consensus['number'],
             consensus['num_var'],
             pt['price_usd'], pt['variation'], pt['number'], pt['num_var'],
             pt['ret'], pt['csho']]
        tab_value.append(t)


def SetBackupOfDataBase(description):

    backup("GhislainPougomNoubissie", "BlackFireCapitalIncFromBottomToTheTop", "/var/backups/mongo/",
           attached_directory_path="/home/pougomg/Bureau/BlackFireCapitalBackup/",custom_prefix=description,
           silent=True)


def RestoreBackupOfdataBase(fileName):

    restore("GhislainPougomNoubissie", "BlackFireCapitalIncFromBottomToTheTop", "/var/backups/mongo/"+fileName+".tbz")


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner