#!/usr/bin/env python3

import requests

GLOBAL_CLIENT_SECRET = "VEgtGle6ZT53ylOg4bgv"
GLOBAL_REDIRECT_URL = "https://example.com/"
GLOBAL_CLIENT_ID = "1lRpPVFcNNJiRM3mYd2z"
GLOBAL_CODE = "KURJ12M0mYE4G0EiZuuytneY1UOHW8"


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
    # print(r.headers)
    # jsonfile = r.json()
    if r.status_code == 200:
        return r.json()["access_token"]
    else:
        return None


def show_all_transactions(access_token: str):
    """shows all transactions of specific person"""
    # TODO show only for specific person data

    header = {"Authorization": f"bearer {access_token}"}
    print(f"Bearer {access_token}")
    r = requests.get(
        "https://api-sandbox.sebgroup.com/ais/v1/identified2/branded-card-accounts/:accountId/transactions",
        data=header)
    print(r.url)
    print(r.status_code)
    print(r.headers)
    # r.json()

    pass


def main():
    print("Hello World of SEB API!")
    #get_request()
    access_token = "YGXp22lHsNK20tSUDWGK" #get_access_token()
    show_all_transactions(access_token)


if __name__ == "__main__":
    main()
