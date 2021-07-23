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
    r = requests.get('https://api.github.com/events')
    print(r.status_code)
    print()


if __name__ == "__main__":
    main()
