from flask import Flask

print(__name__)

app = Flask(__name__)

"""
stores = [{
  'name': 'My Wonderful Store',
  'items': [{
    'name': 'My Item',
    'price': 15.99
  }]
}]
"""

app.config['POPULATE_EXCEPTIONS'] = True

app.config['API_TITLE'] = 'Stores Rest Api'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
