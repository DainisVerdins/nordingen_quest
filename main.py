#!/usr/bin/env python3

import requests


def post_request():
    """ Rest POST request to BANK API to get back as response
    json file what contains acces token"""
    pass


def get_request() -> str:
    """Rest GET Call for authification to BANK API

    :returns html page"""
    pass


def main():
    print("Hello World of SEB API!")
    url = "https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/authorize"
    query_params = {'response_type': 'code',
                    'redirect_uri': 'https://example.com/',
                    'scope': ['psd2_accounts', 'psd2_payments'],
                    'client_id': '1lRpPVFcNNJiRM3mYd2z'
                    }
    r = requests.get(url, params=query_params)
    print(r.text)
    print(r.status_code)
    print()


if __name__ == "__main__":
    main()
