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
GLOBAL_ACCESS_CODE = "VZsOs1RFYcynKqKMTAL2nvns83cy5I"

# The associated scopes requested with the authorization grant.
GLOBAL_REQUEST_SCOPE = ["psd2_accounts", "psd2_payments"]

GLOBAL_SANDBOX_ID = "9311219589"

# for whom will be shown all transactions of specific client
GLOBAL_CARD_CLIENT_ID = "301019000264028"

GLOBAL_TIMEOUT_PERIOD = 3  # in seconds


def get_request():
    """ opens URL of SEB API where need to enter sandbox api and press button 'submit'.
    As result redirects into GLOBAL_REDIRECT_URL with additional parameter in URL.
    In that URL need to copy string part of URL after  'code='
    this part is 'acces code' to request access_token
    """

    url = "https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/authorize"
    query_params = {"response_type": "code",
                    "redirect_uri": GLOBAL_REDIRECT_URL,
                    "scope": GLOBAL_REQUEST_SCOPE,
                    "client_id": GLOBAL_CLIENT_ID
                    }
    # output of request is htmp page but here only need URL
    r = requests.get(url, params=query_params, timeout=GLOBAL_TIMEOUT_PERIOD)

    try:
        r = requests.get(url, params=query_params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    webbrowser.open(r.url)


def get_access_token(access_code: str) -> str:
    """ REST request to bank API where input param is access_code
    on succesions of request returns json file what contains tokens
    if not colapses the programme

    :returns access_token in string format"""

    query_header = {"grant_type": "authorization_code",
                    "code": access_code,
                    "scope": GLOBAL_REQUEST_SCOPE,
                    "client_id": GLOBAL_CLIENT_ID,
                    "client_secret": GLOBAL_CLIENT_SECRET,
                    "redirect_uri": GLOBAL_REDIRECT_URL
                    }

    try:
        r = requests.post("https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/token", data=query_header,
                          timeout=GLOBAL_TIMEOUT_PERIOD)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("word is cruel place and to it I say goodbye, probably bad access_code  was entered")
        raise SystemExit(err)
    print("got access_token")
    return r.json()["access_token"]


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

    try:
        r = requests.get(
            f"https://api-sandbox.sebgroup.com/ais/v1/identified2/branded-card-accounts/{card_transaction_id}/transactions",
            headers=query_headers, params=query_params, timeout=GLOBAL_TIMEOUT_PERIOD)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    # Just print pretty json file
    print(json.dumps(r.json(), indent=4, sort_keys=True))


def main():
    print("Hello World of SEB API!")
    get_request()

    # TODO some code  aka loop to get from user as promt code geted from page redirected before

    # access_token = "9UHBGmgHJlTUyZ1esNJv"  #
    get_access_token(GLOBAL_ACCESS_CODE)
    # show_all_transactions(access_token, "301019000264028")


if __name__ == "__main__":
    print("Show all transactions from SEB bank API")
    main()
