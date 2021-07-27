#!/usr/bin/env python3
import webbrowser
import requests
import json  # for prety json output of transactions

# stuff needed to get use API of SEB
# information about registered app in sandbox enviroment
GLOBAL_CLIENT_SECRET = "VEgtGle6ZT53ylOg4bgv"  # apps client secret
GLOBAL_REDIRECT_URL = "https://example.com/"
GLOBAL_CLIENT_ID = "1lRpPVFcNNJiRM3mYd2z"

# means key to get access token
GLOBAL_ACCESS_CODE = "KURJ12M0mYE4G0EiZuuytneY1UOHW8"

# The associated scopes requested with the authorization grant.
GLOBAL_REQUEST_SCOPE = ["psd2_accounts", "psd2_payments"]

GLOBAL_SANDBOX_ID = "9311219589"

# for whom will be shown all transactions of specific client
GLOBAL_CARD_CLIENT_ID = "301019000264028"


def get_request():
    """ opens URL of SEB API where need to enter sandbox api and press button 'submit'.
    As result redirects into GLOBAL_REDIRECT_URL with additional parameter in URL.
    In that URL need to copy string part of URL after  'code='
    this part is 'acces code' to request authorization token
    """

    url = "https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/authorize"
    query_params = {"response_type": "code",
                    "redirect_uri": GLOBAL_REDIRECT_URL,
                    "scope": GLOBAL_REQUEST_SCOPE,
                    "client_id": GLOBAL_CLIENT_ID
                    }
    #output of request is htmp page but here only need URL
    r = requests.get(url, params=query_params)

    if r.status_code == 200:
        print(r.url)
        webbrowser.open(r.url)
    else:
        print("wrong request URL to autification to seb bank")


def get_access_token():
    """thru POST requests gets access token to API

    :returns html page"""

    query_header = {"grant_type": "authorization_code",
                    "code": GLOBAL_ACCESS_CODE,
                    "scope": GLOBAL_REQUEST_SCOPE,
                    "client_id": GLOBAL_CLIENT_ID,
                    "client_secret": GLOBAL_CLIENT_SECRET,
                    "redirect_uri": GLOBAL_REDIRECT_URL
                    }

    r = requests.post("https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/token", data=query_header)
    print(r.text)
    if r.status_code == 200:
        return r.json()["access_token"]
    else:
        return None


def show_all_transactions(access_token: str, card_transaction_id: str):
    """shows all transactions of specific person"""
    # TODO show only for specific person data not all transactions

    query_headers = {'Authorization': 'Bearer ' + access_token,
                     "Accept": "application/json",
                     "Content-Type": "application/json"
                     }

    query_params = {"dateFrom": " ",
                    "dateTo": " ",
                    "bookingStatus": " "
                    }

    print(query_headers)
    r = requests.get(
        f"https://api-sandbox.sebgroup.com/ais/v1/identified2/branded-card-accounts/{card_transaction_id}/transactions",
        headers=query_headers, params=query_params)
    print(r.url)
    print(r.status_code)
    print(r.raise_for_status())
    print(r.headers)
    print(r.text)

    if r.status_code == 200:

        # Just print pretty json file
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        print("Something went wrong with request")


def main():
    print("Hello World of SEB API!")
    get_request()

    # TODO some code  aka loop to get from user as promt code geted from page redirected before

    # access_token = "9UHBGmgHJlTUyZ1esNJv"  #
    get_access_token()
    # show_all_transactions(access_token, "301019000264028")


if __name__ == "__main__":
    print("Show all transactions from SEB bank API")
    main()
