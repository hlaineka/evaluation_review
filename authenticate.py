from pyoauth2 import Client
import json
import requests

CLIENT_ID = '07a6112fbad61e27ee654e5c492e2d0d5f93cd8a8429221491a56d059596bdcf'
client_secret_file = open("client_secred.txt", "r")
CLIENT_SECRET = client_secret_file.read()
print (CLIENT_SECRET)
REDIRECT_URL = 'https://github.com/hlaineka/evaluation_review'

client = Client(CLIENT_ID, CLIENT_SECRET,
                site='https://api.intra.42.fr',
                authorize_url='https://api.intra.42.fr/oauth/authorize',
                token_url='https://api.intra.42.fr/oauth/token/')

print ('-' * 80)
authorize_url = client.auth_code.authorize_url(redirect_uri=REDIRECT_URL)
print ('Go to the following link in your browser:')
print (authorize_url)

code = input('Enter the verification code and hit ENTER when you\'re done:')
code = code.strip()
access_token = client.auth_code.get_token(code, redirect_uri=REDIRECT_URL)
print ('token', access_token.headers)

print ('-' * 80)
print ('get user info')
ret = access_token.get('/v2/scale_teams')
print(ret.headers)