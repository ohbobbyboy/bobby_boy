#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import config
import subprocess
from ofd import OFDProvider


def edit(filename):
    process = subprocess.Popen([config.edit_cmdline, filename])


def make(items,
         categories,
         filename,
         datetime,
         receipt_sum,
         calculated_sum,
         payment_method):

    with open(filename, 'wb') as csvfile:
        report = csv.writer(csvfile, delimiter=';',
                            lineterminator="\r\n", quotechar='"')

        report.writerow(["#", "", "Импорт данных в Drebedengi"])
        report.writerow(["#", "", "Строки с # являются служебными,",
                         "при импорте", "будут удалены"])
        report.writerow(["#", "Категории:"])
        for category in categories:
            report.writerow(["#", "", category])

        report.writerow(["#"])
        report.writerow(["#"])
        report.writerow(["# Сумма", "Валюта", "Категория", "Кошелёк",
                         "Время", "Комментарий", "Пользователь", "Группа"])
        for name, summa in items:
            report.writerow([summa, config.currency_name, config.category_name,
                             payment_method, datetime, name, "", ""])

        report.writerow(["# Сумма", calculated_sum])
        report.writerow(["# По чеку", receipt_sum])


def clear(filename):
    rows = []

    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = [row for row in reader]

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', skipinitialspace=True,
                            quoting=csv.QUOTE_NONNUMERIC)  # QUOTE_MINIMAL vs QUOTE_NONNUMERIC

        for row in rows:
            if not row[0].startswith("#"):
                # удаляем неразрывные пробелы в названиях категорий
                row[2] = row[2].strip(' ')
                writer.writerow(row)
