#!/usr/bin/python
# -*- coding: utf-8 -*-
import qr
import os
import sys
import config
import argparse
import drebedengi
import report
from ofd import OFDProvider


# создаём необходимые директории если отсутствуют
def init():
    if not os.path.exists(config.receipt_dir):
        os.makedirs(config.receipt_dir)
    if not os.path.exists(config.report_dir):
        os.makedirs(config.report_dir)


# resend - разрешение повторно передавать данные по чеку, который уже сохранен
def recognize(resend, receipt_text):

    ofd_receipt = OFDProvider(resend).detect(receipt_text)

    if not ofd_receipt is bool:
        items = ofd_receipt.get_items()
        if items:
            return ofd_receipt
    elif ofd_receipt:
        kkt = raw_input("Enter `PH KKT`: ")
        inn = raw_input("Enter `INN`: ")
        ofd_receipt = OFDProvider(resend).detect(receipt_text,kkt,inn)

        if not ofd_receipt is bool:
            items = ofd_receipt.get_items()
            if items:
                return ofd_receipt
    return False


init()

if len(sys.argv) > 1 and sys.argv[1] == "--text":
    # распознаём из введённого текста
    receipt = recognize(config.already_recognized_send,
                        raw_input("Enter content from QR: "))
else:
    receipt = recognize(config.already_recognized_send,
                        qr.get_content_with_gui())

if receipt:
    report_name = receipt.get_csv_file_name()
    dreb_session = drebedengi.Drebedengi(config.username, config.password)
    if not dreb_session.logged_in():
        print("Auth is not successful!")
        sys.exit(-1)

    categories = dreb_session.get_categories()

    report.make(receipt.items,
                categories,
                report_name,
                receipt.dreb_time,
                receipt.raw_sum,
                receipt.total_sum)

    report.edit(report_name)

    raw_input("Press Enter to export report to Drebedengi...")

    report.clear(report_name)

    dreb_session.send_csv(report_name)

else:
    print("Receipt search failed!")
