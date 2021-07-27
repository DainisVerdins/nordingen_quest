#!/usr/bin/env python3
import webbrowser
import requests
import json  # for prety json output of transactions
import sys  # to force close programme

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


def open_code_webpage():
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

    try:
        # output of request is htmp page but here only need URL
        r = requests.get(url, params=query_params, timeout=GLOBAL_TIMEOUT_PERIOD)

        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    # open web browser and in new tab go into this url
    print("STEP 1/3 done open url in webbrowser")
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

    print("STEP 2/3 done, got access_token")
    return r.json()["access_token"]


def get_all_transactions(access_token: str, card_transaction_id: str):
    """shows all transactions of specific person by GET request
    :param access_token - to acces API
    :param card_transaction_id whose transactions will be shows
    :return json"""

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

    print("STEP 3/3 done, got list of transactions")

    return json.dumps(r.json())


def main():
    print("Gets out from SEB API SANDBOX all  transactions")
    print("This is done by three steps")
    print(f"STEP 1 - if you continue script will open your web browser in new tab webpage and in input field enter "
          f"sandbox ID this one -> '{GLOBAL_SANDBOX_ID}' and press submit ")
    print("STEP 2 - ENTER Authorization code redirected from earlier request in promt")
    print("STEP 3 - if previous steps are passed you will see dumped json in console with transactions")

    while True:
        i = input("any text entered means quit from programme (or Enter to continue): ")
        if not i:
            break
        sys.exit(0)

    open_code_webpage()
    print("input ENTER Authorization code redirected from earlier request in promt, code without 'code='")
    code = str(input())

    i = 3
    while len(code) > 30:
        if i == 0:
            sys.exit(0)
        print(
            f"error, length of code must be 30 symbols, try again , you have {i} trys left otherwise quit")
        code = str(input())
        i -= 1

    access_token = get_access_token(code)
    transactions = get_all_transactions(access_token, GLOBAL_CARD_CLIENT_ID)
    print(transactions)


if __name__ == "__main__":
    print("Show all transactions from SEB bank API")
    main()
