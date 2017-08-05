#!/usr/bin/python
# -*- coding: utf-8 -*-
import qr
import os
import sys
import config
import argparse
import report
from ofd import OFDProvider
from drebedengi import Drebedengi


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

parser = argparse.ArgumentParser(description='Import receipts data from OFD to Drebedengi')
parser.add_argument('--text', help='take receipt data from string')
parser.add_argument('--noediting', action='store_false', help='disable manual report editing')
args = parser.parse_args()

init()

if not args.text is None:
    # распознаём из введённого текста
    receipt = recognize(config.already_recognized_send, args.text)
else:
    receipt = recognize(config.already_recognized_send,
                        qr.get_content_with_gui())

if receipt:
    report_name = receipt.get_csv_file_name()
    dreb_session = Drebedengi(config.username, config.password)
    if not dreb_session.logged_in():
        print("Auth is not successful!")
        sys.exit(-1)

    categories = dreb_session.get_categories()

    sms_saved_receipt = dreb_session.search(receipt.dreb_time, receipt.raw_sum)

    if sms_saved_receipt:
        receipt.payment_method = sms_saved_receipt['payment_method']

    report.make(receipt.items,
                categories,
                report_name,
                receipt.dreb_time,
                receipt.raw_sum,
                receipt.total_sum,
                receipt.payment_method)

    if args.noediting:
        report.edit(report_name)

    raw_input("Press Enter to export report to Drebedengi...")

    report.clear(report_name)

    import_result = dreb_session.send_csv(report_name)

    if import_result and sms_saved_receipt:
        dreb_session.delete_item(sms_saved_receipt['id'])

else:
    print("Receipt search failed!")
