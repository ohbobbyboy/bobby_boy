#!/usr/bin/python
# -*- coding: utf-8 -*-
import suds.client as client
import config
import datetime
import requests
from bs4 import BeautifulSoup
from config import username, password, api_key

wsdl_url = "http://www.drebedengi.ru/soap/dd.wsdl"
http_login_url = "https://www.drebedengi.ru/?module=v2_start&action=login"
http_csv_send_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateImport&action=csv_submit"
http_csv_confirm_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateImport&action=confirm"

currency_list = []  # не используется
default_currency_id = ""


category_list = []
default_category_id = ""

# print(session)


def soap_login():
    session = client.Client(wsdl_url)

    currency_request = session.service.getCurrencyList(
        api_key, username, password)

    currency_list = {item["item"][1][1].encode(
        'utf-8'): item["item"][0][1] for item in currency_request}  # справочник валют - name: id
    default_currency = currency_list[config.currency_name]

    category_request = session.service.getCategoryList(
        api_key, username, password)

    # справочник категорий трат - name: id
    category_list = {item["item"][4][1].encode(
        'utf-8'): item["item"][0][1] for item in category_request}

    # for item in category_list:
    #     print(item.decode('utf-8'))

    operational_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Drebedengi:
    session = None
    categories = []

    def __init__(self, user, password):
        session = requests.Session()

        data = {
            "o": "",
            "email": user,
            "password": password,
            "ssl": "on"
        }
        # session.headers.update({
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # })

        login = session.post(http_login_url, data)
        soup = BeautifulSoup(login.content, 'html.parser')
        categories = [option.text.encode(
            'utf-8') for option in soup.find(id="add_w_category_id").find_all("option")]

        self.categories = categories[1:]
        self.session = session

    def logged_in(self):
        return self.session != None

    def get_categories(self):
        return self.categories

    def send_csv(self, filename):
        data = {
            'imp_fmt': 'imp_in_fmt',
            'csvFile': (filename,
                        open(filename, 'rb'),
                        'text/csv')

        }
        r = self.session.post(http_csv_send_url, files=data)
        print(r.status_code)
        self.session.post(http_csv_confirm_url)
        print(r.status_code)
