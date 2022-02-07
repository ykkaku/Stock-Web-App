from flask_pymongo import PyMongo
import pymysql
import requests
from bs4 import BeautifulSoup

# Mongo database connector
mongo = PyMongo()

# Define functions to connect to Google cloud MySQL

# Our instance connection name
db_connection_name = 'stock-project-294701:us-central1:stock-database'

# NOTE: must be running Cloud SQL Proxy on your local machine for this to work!


def open_connection():
    unix_socket = f'/cloudsql/{db_connection_name}'
    try:
        # if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='PApOEaPbJNOM62p1',
            db='stockdb',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor

        )
        return conn
    except pymysql.MySQLError as e:
        print("EXCEPTION")
        print(e)


def get_companies(limit):
    conn = open_connection()
    with conn.cursor() as cursor:
        q = f'SELECT * FROM CompanyInformation LIMIT {limit};'
        result = cursor.execute(q)
        companies = cursor.fetchall()
        if result > 0:
            # got_c = jsonify(companies)
            got_c = companies  # a list of dictionaries
        else:
            got_c = 'Nothing in DB'
    conn.close()
    return got_c

def get_company_name_sector(symbol):
    conn = open_connection()
    with conn.cursor() as cursor:
        q = f"""
        SELECT name, sector FROM CompanyInformation
        WHERE symbol = '{symbol}'
        LIMIT 1;
        """
        result = cursor.execute(q)
        company = cursor.fetchall()
        if result > 0:
            # got_c = jsonify(companies)
            results = company[0]
        else:
            results = 'Nothing in DB'
    conn.close()
    return results   ## dictionary 

def get_prices(symbol, limit):
    conn = open_connection()
    with conn.cursor() as cursor:
        q = f"""
            SELECT *
            FROM {symbol}
            ORDER BY date DESC
            LIMIT {limit};
        """
        result = cursor.execute(q)
        prices = cursor.fetchall()
        if result > 0:
            got_p = prices
        else:
            got_p = 'Nothing in DB'
    conn.close()
    return got_p


def search_by_date(symbol, date):
    conn = open_connection()
    with conn.cursor() as cursor:
        q = f"""
            SELECT *
            FROM {symbol}
            WHERE date = '{date}';
        """
        result = cursor.execute(q)
        prices = cursor.fetchall()
        if result > 0:
            got_p = prices
        else:
            got_p = []
    conn.close()
    return got_p


def get_current_close_price(symbol):
    newlist = []
    newdict = dict()
    url = 'https://finance.yahoo.com/quote/'
    finalurl = url + symbol + '?p=' + symbol + '&.tsrc=fin-srch'
    r = requests.get(finalurl)
    soup = BeautifulSoup(r.content, 'lxml')
    stockprice = soup.find_all('div', {"My(6px) Pos(r) smartphone_Mt(6px)"})[
        0].find('span', {'class': "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    newdict['name'] = symbol
    newdict['price'] = stockprice
    newlist.append(newdict)
    return newlist[0]['price']


def get_agg_prices(industry):
    # `industry` argument should be a table name
    conn = open_connection()
    with conn.cursor() as cursor:
        q = f"""
            SELECT *
            FROM {industry};
        """
        result = cursor.execute(q)
        prices = cursor.fetchall()
        if result > 0:
            got_p = prices
        else:
            got_p = []
    conn.close()
    return got_p

if __name__ == "__main__":
    print("Test db connection to MySQL")
    # print(get_companies(limit=15))
    print(get_company_name_sector('A'))

    # prices = get_prices('A', 10)
    # for p in prices:
    #     print(p)
    #     print(type(p))

    # print(search_by_date('AAPL', '2020-11-02'))

    # print(get_current_close_price('AAPL'))
