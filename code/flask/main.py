from flask import Blueprint, render_template, Flask, request, make_response, redirect, url_for
from pymysql import ProgrammingError
from .extensions import mongo, open_connection, get_companies, get_company_name_sector, get_prices, search_by_date, get_current_close_price, get_agg_prices
from .forms import SymSearchForm, DateSearchForm

main = Blueprint('main', __name__)

## Main Page
@main.route('/', methods=['GET','POST'])
def index():

    ## define MongoDB collection
    news_col = mongo.db.articles
    mdb_results = news_col.find().limit(15).sort("dt", -1)
    sql_results = get_companies(limit=20)  ## a list of dicts

    ## Search feature
    form = SymSearchForm(request.form)
    if request.method == 'POST':
        sym_query = form.symbol.data
        return redirect(url_for('.show', sym=sym_query))

    return render_template('index.html', mdb_results=mdb_results, sql_results=sql_results, form=form)


## Page template to show company stock info
@main.route('/<sym>', methods=['GET', 'POST'])
def show(sym):

    ## SQL results for the company
    price_results = get_prices(symbol=sym, limit=40)  ## a list of dicts
    ## Mongo results
    news_col = mongo.db.articles
    mdb_results = news_col.find({ "Symbol": sym }).limit(15).sort("dt", -1)
    
    ## Search feature
    form = DateSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        dt_query = form.date.data
        dt_query_str = str(dt_query)
        ## Search MySQL db for prices on a given date
        price_res = search_by_date(symbol=sym, date=dt_query)  ## a list of dicts
        ## Search MongoDB for news on a given dt
        news_res = news_col.find({"Symbol": sym, "dt": dt_query_str}).limit(15).sort("dt", -1)  ## this is a cursor
        new_res_list = list(news_res)

        return render_template('search_results.html', sym=sym, form=form, price_results=price_res, news_results=news_res, news_res_list=new_res_list) 

    ## Show current price
    current_price = get_current_close_price(sym)
    ## Get full company name
    name_sector = get_company_name_sector(sym)
    c_name = name_sector['name']
    s_name = name_sector['sector']
    ind_link0 = "Industry_" + s_name.replace(" ", "_")
    ind_link = f"/spark/{ind_link0}"
    return render_template('page.html', symbol=sym, price_results=price_results, mdb_results=mdb_results, form=form, current_price=current_price, c_name=c_name, industry=s_name, ind_link=ind_link)


## Page template to show Spark agg info
@main.route('/spark/<industry>', methods=['GET', 'POST'])
def show_spark(industry):
    ## Spark results
    ind_results = get_agg_prices(industry=industry)
    industry_name = " ".join(industry.split('_')[1:])
    return render_template('industry_page.html', industry=industry, industry_name=industry_name, price_results=ind_results)


## Page not found
@main.errorhandler(404)
def not_found():
    return make_response(render_template("404.html"), 404)


## If stock table is not found, return error page
@main.errorhandler(ProgrammingError)
def handle_error(e):
    return '<h1>Table not found!</h1>', 400