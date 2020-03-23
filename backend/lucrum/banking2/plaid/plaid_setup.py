import base64
import os
import datetime
import plaid
import json
import time
from flask import Flask, Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from api_keys import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY

PLAID_ENV = 'development'
PLAID_PRODUCTS = 'auth,transactions'
PLAID_COUNTRY_CODES = 'GB'
PLAID_OAUTH_REDIRECT_URI = ''
PLAID_OAUTH_NONCE = ''

plaid_setup = Blueprint('plaid', __name__, url_prefix='/plaid_setup', template_folder='templates')

client = plaid.Client(client_id=PLAID_CLIENT_ID,
						secret=PLAID_SECRET,
						public_key=PLAID_PUBLIC_KEY,
						environment=PLAID_ENV,
						api_version='2019-05-29')


@plaid_setup.route('/')
def index():
	return render_template(
		'index.ejs',
		plaid_public_key=PLAID_PUBLIC_KEY,
		plaid_environment=PLAID_ENV,
		plaid_products=PLAID_PRODUCTS,
		plaid_country_codes=PLAID_COUNTRY_CODES,
		plaid_oauth_redirect_uri=PLAID_OAUTH_REDIRECT_URI,
		plaid_oauth_nonce=PLAID_OAUTH_NONCE,
	)


# This is an endpoint defined for the OAuth flow to redirect to.
@plaid_setup.route('/oauth-response.html')
def oauth_response():
	return render_template(
		'oauth-response.ejs',
		plaid_public_key=PLAID_PUBLIC_KEY,
		plaid_environment=PLAID_ENV,
		plaid_products=PLAID_PRODUCTS,
		plaid_country_codes=PLAID_COUNTRY_CODES,
		plaid_oauth_nonce=PLAID_OAUTH_NONCE,
	)


# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_token is only relevant for the UK Payment Initiation product.
# We store the payment_token in memory - in production, store it in a secure
# persistent data store.
payment_token = None
payment_id = None


# Exchange token flow - exchange a Link public_token for
# an API access_token
# https://plaid.com/docs/#exchange-token-flow
@plaid_setup.route('/get_access_token', methods=['POST'])
def get_access_token():
	global access_token
	public_token = request.form['public_token']
	print("PUBLIC TOKEN", public_token)
	try:
		exchange_response = client.Item.public_token.exchange(public_token)
	except plaid.errors.PlaidError as e:
		# return jsonify(format_error(e))
		print(e)

	# pretty_print_response(exchange_response)
	access_token = exchange_response['access_token']
	print("ACCESS TOKEN", access_token)

	from lucrum.models.account.account_connection import AccountConnectionUser
	from lucrum.database import db
	from lucrum.models.account.account_connection import ConnectionType
	db.session.add(AccountConnectionUser(ConnectionType.PLAID, "", access_token))
	db.session.commit()

	return jsonify(exchange_response)
