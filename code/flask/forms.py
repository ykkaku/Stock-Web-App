from wtforms import Form, StringField, validators, DateField

class SymSearchForm(Form):
    symbol = StringField('Symbol', render_kw={"placeholder": "Enter a stock symbol"})

class DateSearchForm(Form):
    date = DateField('Date', render_kw={"placeholder": "Enter a date"})