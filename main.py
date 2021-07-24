#!/usr/bin/env python3

import requests
import json #for prety json output of transactions

# stuff needed to get use API of SEB
GLOBAL_CLIENT_SECRET = "VEgtGle6ZT53ylOg4bgv"
GLOBAL_REDIRECT_URL = "https://example.com/"
GLOBAL_CLIENT_ID = "1lRpPVFcNNJiRM3mYd2z"
GLOBAL_CODE = "KURJ12M0mYE4G0EiZuuytneY1UOHW8"

# for whom will be shown all transactions
GLOBAL_CARD_CLIENT_ID = "301019000264028"


def get_request():
    """ Rest GET request to BANK API to get back as response
    html page where need to enter SANDBOX KAY"""

    url = "https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/authorize"
    query_params = {"response_type": "code",
                    "redirect_uri": GLOBAL_REDIRECT_URL,
                    "scope": ["psd2_accounts", "psd2_payments"],
                    "client_id": GLOBAL_CLIENT_ID
                    }
    r = requests.get(url, params=query_params)
    print(r.text)
    print(r.url)


def get_access_token() -> str:
    """thru POST requests gets access token to API

    :returns html page"""

    header = {"grant_type": "authorization_code",
              "code": GLOBAL_CODE,
              "scope": ["psd2_accounts", "psd2_payments"],
              "client_id": GLOBAL_CLIENT_ID,
              "client_secret": GLOBAL_CLIENT_SECRET,
              "redirect_uri": GLOBAL_REDIRECT_URL
              }

    r = requests.post("https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/token", data=header)
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
                    "bookingStatus": " "
                    }

    print(query_headers)
    r = requests.get(
        f"https://api-sandbox.sebgroup.com/ais/v1/identified2/branded-card-accounts/{card_transaction_id}/transactions",
        headers=query_headers, params=query_params)
    print(r.url)
    print(r.status_code)
    print(r.headers)
    print(r.text)
    if r.status_code == 200:

        #Just print pretty json file
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        print("Something went wrong with request")


def main():
    print("Hello World of SEB API!")
    # get_request()
    access_token = "YGXp22lHsNK20tSUDWGK"  # get_access_token()
    show_all_transactions(access_token, "301019000264028")


if __name__ == "__main__":
    print("Show all transactions of from SEB bank API")
    main()
